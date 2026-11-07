// M3 clearance hole. Non-plated, so a metal screw does not short the board.
// Drill is 3.2 mm. The silk ring is the 6 mm screw head.
module.exports = {
    params: {
        designator: 'H'
    },
    body: p => `
    (module M3 (layer F.Cu) (tedit 5B24D78E)
      ${p.at}
      (fp_text reference "${p.ref}" (at 0 -4.2) (layer F.SilkS) ${p.ref_hide} (effects (font (size 1 1) (thickness 0.15))))
      (fp_text value "M3" (at 0 0) (layer F.Fab) hide (effects (font (size 1 1) (thickness 0.15))))
      (fp_circle (center 0 0) (end 3 0) (layer F.SilkS) (width 0.12))
      (fp_circle (center 0 0) (end 3 0) (layer B.SilkS) (width 0.12))
      (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers *.Cu *.Mask))
    )
    `
}
