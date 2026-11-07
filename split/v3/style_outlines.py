"""Restyle Ergogen outline SVGs so they stay readable on a dark background."""

from pathlib import Path

HERE = Path(__file__).parent
OUTLINES = HERE / "outlines"

BG = "#1e1e1e"
STROKE = "#f5f5f5"
WIDTH = "0.7mm"


def style(svg: str) -> str:
    svg = svg.replace('stroke="#000"', f'stroke="{STROKE}"')
    svg = svg.replace("stroke:#000", f"stroke:{STROKE}")
    svg = svg.replace("0.25mm", WIDTH)
    if 'id="outline-bg"' not in svg:
        svg = svg.replace(
            "<g ",
            f'<rect id="outline-bg" width="100%" height="100%" fill="{BG}"/><g ',
            1,
        )
    return svg


def main() -> None:
    for path in sorted(OUTLINES.glob("*.svg")):
        path.write_text(style(path.read_text()))


if __name__ == "__main__":
    main()
