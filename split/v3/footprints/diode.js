// SOD-123 on the back only. The cathode (the bar) is pad 1.
module.exports = {
    params: {
        designator: 'D',
        from: undefined,
        to: undefined
    },
    body: p => `
    (module Diode_SMD_B (layer B.Cu) (tedit 5B24D78E)
        ${p.at}
        (fp_text reference "${p.ref}" (at 0 1.8 ${p.r}) (layer B.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))
        (fp_text value "" (at 0 0) (layer B.SilkS) hide (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))
        (fp_line (start 0.25 0) (end 0.75 0) (layer B.SilkS) (width 0.1))
        (fp_line (start 0.25 0.4) (end -0.35 0) (layer B.SilkS) (width 0.1))
        (fp_line (start 0.25 -0.4) (end 0.25 0.4) (layer B.SilkS) (width 0.1))
        (fp_line (start -0.35 0) (end 0.25 -0.4) (layer B.SilkS) (width 0.1))
        (fp_line (start -0.35 0) (end -0.35 0.55) (layer B.SilkS) (width 0.1))
        (fp_line (start -0.35 0) (end -0.35 -0.55) (layer B.SilkS) (width 0.1))
        (fp_line (start -0.75 0) (end -0.35 0) (layer B.SilkS) (width 0.1))
        (pad 1 smd rect (at -1.65 0 ${p.r}) (size 0.9 1.2) (layers B.Cu B.Paste B.Mask) ${p.to})
        (pad 2 smd rect (at 1.65 0 ${p.r}) (size 0.9 1.2) (layers B.Cu B.Paste B.Mask) ${p.from})
    )
    `
}