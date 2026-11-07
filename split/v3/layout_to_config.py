#!/usr/bin/env python3
"""Write layout.json and rebuild config.yaml from that layout."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAYOUT_PATH = HERE / "layout.json"
KEYMAP_PATH = HERE / "keymap.json"
CONFIG_PATH = HERE / "config.yaml"

WIRED = {
    "COL_MACRO", "COL_PINKY", "COL_RING", "COL_MIDDLE", "COL_INDEX", "COL_INNER",
    "ROW_BOT", "ROW_HOME", "ROW_TOP", "ROW_NUMS", "ROW_FN", "ROW_THUMB",
}
SPARE_PINS = ["P0", "P1", "P21", "P20", "P8", "P9"]


def num(value):
    value = round(float(value), 2)
    if value == 0:
        value = 0.0
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return text or "0"


def save_keymap(layout):
    keys = layout.get("keymap")
    if not isinstance(keys, list):
        return None
    KEYMAP_PATH.write_text(json.dumps({"version": 1, "keys": keys}, indent=2) + "\n")
    return len(keys)


def save_layout(layout):
    if not isinstance(layout, dict) or "keys" not in layout:
        raise ValueError("layout json needs a keys list")
    LAYOUT_PATH.write_text(json.dumps(layout, indent=2) + "\n")
    return save_keymap(layout)


def anchor_name(keys):
    names = {key["name"] for key in keys}
    if "matrix_macro_fn" in names:
        return "matrix_macro_fn"
    fn_keys = [key for key in keys if key.get("mirror") and key.get("row") == "fn"]
    if fn_keys:
        return min(fn_keys, key=lambda key: float(key["x"]))["name"]
    if keys:
        return keys[0]["name"]
    raise ValueError("layout has no keys")


def render_points(layout):
    keys = layout.get("keys") or []
    if not keys:
        raise ValueError("layout has no keys")
    lines = [
        "points:",
        "  # Positions come from layout.json. Save JSON, then Update config.yaml,",
        "  # to replace this section. Footprints below stay as they are.",
        "  key:",
        "    spread: pitch",
        "    padding: pitch",
        "    width: cap",
        "    height: cap",
        "  zones:",
        "    matrix:",
        "      anchor:",
        "        rotate: 0",
        "      key:",
        "        spread: 0",
        "        stagger: 0",
        "        padding: 0",
        "        splay: 0",
        "      columns:",
    ]
    for key in keys:
        name = key["name"]
        lines.append(f"        {name}:")
        lines.append("          key:")
        lines.append(f"            shift: [{num(key['x'])}, {num(key['y'])}]")
        lines.append(f"            rotate: {num(key.get('r', 0))}")
        lines.append(f"            column_net: {key['column_net']}")
        lines.append(f"            name: {name}")
        if not key.get("mirror", True):
            lines.append("            asym: source")
        lines.append("          rows:")
        lines.append("            at:")
        lines.append(f"              row_net: {key['row_net']}")
    ref = anchor_name(keys)
    lines += [
        "    mcu:",
        "      # Outside the outer column. USB points off that edge.",
        "      anchor:",
        f"        ref: {ref}",
        "        shift: [-30, 0]",
        "      columns:",
        "        board:",
        "          key.name: mcu",
        "      rows:",
        "        one: {}",
        "    hardware:",
        "      # Three M3 holes and one encoder per half. A layout update keeps these.",
        "      anchor:",
        "        rotate: 0",
        "      key:",
        "        spread: 0",
        "        stagger: 0",
        "        padding: 0",
        "        splay: 0",
        "      columns:",
        "        m3_outer_top:",
        "          key:",
        "            shift: [-40, 92]",
        "            name: m3_outer_top",
        "        m3_outer_bottom:",
        "          key:",
        "            shift: [-8, -14]",
        "            name: m3_outer_bottom",
        "        m3_thumb:",
        "          key:",
        "            shift: [140, -62]",
        "            name: m3_thumb",
        "        encoder:",
        "          key:",
        "            shift: [116, 90]",
        "            name: encoder",
        "      rows:",
        "        one: {}",
    ]
    mirrored = any(key.get("mirror", True) for key in keys)
    if mirrored:
        lines.append(f"  mirror: {num(layout.get('mirrorX', 0))}")
    return "\n".join(lines) + "\n"


def extra_pins(keys):
    seen = []
    for key in keys:
        for net in (key.get("column_net"), key.get("row_net")):
            if net and net not in WIRED and net not in seen:
                seen.append(net)
    assigned = []
    unassigned = []
    for index, net in enumerate(seen):
        if index < len(SPARE_PINS):
            assigned.append((SPARE_PINS[index], net))
        else:
            unassigned.append(net)
    return assigned, unassigned


def update_pins(text, assigned):
    kept = [line for line in text.splitlines(keepends=True) if "# from layout" not in line]
    text = "".join(kept)
    needle = "          P2: COL_INNER\n"
    if needle not in text:
        raise ValueError("could not find the nice!nano column pins in config.yaml")
    extra = "".join(f"          {pin}: {net}  # from layout\n" for pin, net in assigned)
    return text.replace(needle, needle + extra, 1)


def apply_config(layout):
    keymap_count = save_layout(layout)
    points = render_points(layout)
    existing = CONFIG_PATH.read_text()
    start = existing.find("\npoints:\n")
    end = existing.find("\noutlines:\n")
    if start < 0 or end < 0:
        raise ValueError("config.yaml is missing its points or outlines section")
    updated = existing[: start + 1] + points + existing[end + 1 :]
    assigned, unassigned = extra_pins(layout.get("keys") or [])
    updated = update_pins(updated, assigned)
    CONFIG_PATH.write_text(updated)
    count = len(layout.get("keys") or [])
    message = f"Updated config.yaml from layout.json ({count} keys)."
    if keymap_count is not None:
        message += f" Wrote keymap.json ({keymap_count} keys)."
    if unassigned:
        message += " No spare MCU pin for " + ", ".join(unassigned) + "."
    return {"message": message, "keys": count, "unassigned": unassigned}


if __name__ == "__main__":
    result = apply_config(json.loads(LAYOUT_PATH.read_text()))
    print(result["message"])
