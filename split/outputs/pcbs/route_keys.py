"""
route_keys.py - local routing for Ergogen reversible MX hot-swap keys.

For every diode:  joins each SMD pad to the through-hole on the same net,
                  on the SMD pad's own copper layer.
For every switch: joins each mirrored pad pair (one pad on F.Cu, one on B.Cu)
                  with a bus parallel to the line between the two pads,
                  offset past the pin holes, with one via to change layers.

Run from KiCad's PCB editor: Tools > Scripting Console, then
    exec(open(r"C:/path/to/route_keys.py").read())

Rerunning is safe: everything the script adds goes into a group named
"route_keys", and each run first deletes the previous run's group.
When you're happy with the result, ungroup it (right-click > Grouping > Ungroup)
before routing by hand, so clicking a track doesn't select the whole group.
Run the DRC afterwards and tune the settings below if anything is flagged.
"""
import math
import pcbnew

# ---------------- settings (mm) ----------------
TRACK_WIDTH = 0.25
VIA_DIAMETER = 0.6
VIA_DRILL = 0.3
INNER_BUS = 7.1    # distance from switch center to the bus of the inner pad pair
OUTER_BUS = 7.9    # same for the outer pad pair (must be farther than INNER_BUS)
OUTER_STEP = 0.5     # sideways step out of the outer pads before going to the bus (0 = straight)
VIA_IN_MIDDLE = True  # True: vias near the key center; False: vias at the end of each bus
MIDDLE_VIA_OFFSET = 1.0  # the two middle vias sit this far on either side of center
SWITCH_PREFIX = "S"  # reference prefix of switch footprints
DIODE_PREFIX = "D"   # reference prefix of diode footprints
# -----------------------------------------------

GROUP_NAME = "route_keys"  # everything the script adds goes in this group

board = pcbnew.GetBoard()
mm = pcbnew.FromMM

# Remove whatever a previous run added, so the script can be rerun safely.
for old in list(board.Groups()):
    if old.GetName() == GROUP_NAME:
        items = list(old.GetItems())
        old.RemoveAll()
        board.Remove(old)
        for item in items:
            board.Remove(item)

group = pcbnew.PCB_GROUP(board)
group.SetName(GROUP_NAME)
board.Add(group)


def xy(item):
    p = item.GetPosition()
    return (float(p.x), float(p.y))


def point(x, y):
    return pcbnew.VECTOR2I(int(round(x)), int(round(y)))


def layer_of(pad):
    return pcbnew.F_Cu if pad.IsOnLayer(pcbnew.F_Cu) else pcbnew.B_Cu


def add_path(pts, layer, net):
    """Add a chain of track segments through the given points."""
    for a, b in zip(pts, pts[1:]):
        if math.dist(a, b) < 1:  # skip zero-length segments (units: nm)
            continue
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(point(*a))
        t.SetEnd(point(*b))
        t.SetWidth(mm(TRACK_WIDTH))
        t.SetLayer(layer)
        t.SetNet(net)
        board.Add(t)
        group.AddItem(t)


def add_via(p, net):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(point(*p))
    v.SetDrill(mm(VIA_DRILL))
    try:
        v.SetWidth(mm(VIA_DIAMETER))
    except TypeError:  # newer KiCad versions set the width per layer
        v.SetWidth(pcbnew.F_Cu, mm(VIA_DIAMETER))
    v.SetNet(net)
    board.Add(v)
    group.AddItem(v)


def route_diode(fp):
    pads = [p for p in fp.Pads() if p.GetNetCode() > 0]
    holes = [p for p in pads if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH]
    smds = [p for p in pads if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD]
    for s in smds:
        for h in holes:
            if h.GetNetCode() == s.GetNetCode():
                add_path([xy(s), xy(h)], layer_of(s), s.GetNet())
                break


def route_switch(fp):
    c = xy(fp)

    # Group the socket pads by net: expect two pairs of mirrored pads.
    by_net = {}
    for p in fp.Pads():
        if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD and p.GetNetCode() > 0:
            by_net.setdefault(p.GetNetCode(), []).append(p)
    pairs = [v for v in by_net.values() if len(v) == 2]
    if len(pairs) != 2:
        print(f"Skipped {fp.GetReference()}: expected 2 mirrored pad pairs")
        return False

    # Local frame taken from the pads themselves, so angled keys just work:
    # u runs along the line between mirrored pads, n is perpendicular to it
    # and points from the switch center toward the pads.
    a, b = (xy(p) for p in pairs[0])
    ux, uy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(ux, uy)
    u = (ux / length, uy / length)
    n = (-u[1], u[0])
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    if (mid[0] - c[0]) * n[0] + (mid[1] - c[1]) * n[1] < 0:
        n = (-n[0], -n[1])

    def local(p):
        dx, dy = p[0] - c[0], p[1] - c[1]
        return (dx * u[0] + dy * u[1], dx * n[0] + dy * n[1])

    def world(s, t):
        return (c[0] + u[0] * s + n[0] * t, c[1] + u[1] * s + n[1] * t)

    # Sort each pair left -> right, then the pairs inner -> outer.
    pairs = [sorted(pr, key=lambda p: local(xy(p))[0]) for pr in pairs]
    pairs.sort(key=lambda pr: abs(local(xy(pr[0]))[0]))
    inner, outer = pairs

    off = mm(MIDDLE_VIA_OFFSET)
    for pair, bus, step, mid_s in ((inner, mm(INNER_BUS), 0, -off),
                                   (outer, mm(OUTER_BUS), mm(OUTER_STEP), off)):
        left, right = pair
        ls, lt = local(xy(left))
        rs, rt = local(xy(right))
        xl, xr = ls - step, rs + step
        vs = mid_s if VIA_IN_MIDDLE else xr  # where along the bus the via goes

        first = [world(*q) for q in [(ls, lt), (xl, lt), (xl, bus), (vs, bus)]]
        second = [world(*q) for q in [(vs, bus), (xr, bus), (xr, rt), (rs, rt)]]
        net = left.GetNet()

        if layer_of(left) == layer_of(right):  # non-reversible footprint
            add_path(first + second[1:], layer_of(left), net)
        else:
            add_path(first, layer_of(left), net)
            add_via(world(vs, bus), net)
            add_path(second, layer_of(right), net)
    return True


switches = diodes = 0
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref.startswith(DIODE_PREFIX):
        route_diode(fp)
        diodes += 1
    elif ref.startswith(SWITCH_PREFIX):
        if route_switch(fp):
            switches += 1

pcbnew.Refresh()
print(f"Routed {switches} switches and {diodes} diodes.")