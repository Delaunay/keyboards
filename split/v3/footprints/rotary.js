// EC11 rotary encoder.
// The three pins on one side are A, common, B. Common is the center pin (C).
// The two pins on the other side are the push switch.
// On the mirrored half the part is turned 180 so the signal pins still face the keys.

module.exports = {
    params: {
        designator: 'ROT',
        from: undefined,
        to: undefined,
        A: undefined,
        B: undefined,
        C: undefined
    },
    body: p => {
        const rot = p.point.meta.mirrored ? p.r + 180 : p.r
        return `
        (module rotary_encoder (layer F.Cu) (tedit 603326DE)

            (at ${p.x} ${p.y} ${rot})
        
            ${'' /* footprint reference */}
            (fp_text reference "${p.ref}" (at 0 0.5) (layer F.SilkS) 
                ${p.ref_hide} (effects (font (size 1 1) (thickness 0.15))))
            (fp_text value "" (at 0 8.89) (layer F.Fab)
                (effects (font (size 1 1) (thickness 0.15))))

            ${''/* component outline */}
            (fp_line (start -0.62 -0.04) (end 0.38 -0.04) (layer F.SilkS) (width 0.12))
            (fp_line (start -0.12 -0.54) (end -0.12 0.46) (layer F.SilkS) (width 0.12))
            (fp_line (start 5.98 3.26) (end 5.98 5.86) (layer F.SilkS) (width 0.12))
            (fp_line (start 5.98 -1.34) (end 5.98 1.26) (layer F.SilkS) (width 0.12))
            (fp_line (start 5.98 -5.94) (end 5.98 -3.34) (layer F.SilkS) (width 0.12))
            (fp_line (start -3.12 -0.04) (end 2.88 -0.04) (layer F.Fab) (width 0.12))
            (fp_line (start -0.12 -3.04) (end -0.12 2.96) (layer F.Fab) (width 0.12))
            (fp_line (start -7.32 -4.14) (end -7.62 -3.84) (layer F.SilkS) (width 0.12))
            (fp_line (start -7.92 -4.14) (end -7.32 -4.14) (layer F.SilkS) (width 0.12))
            (fp_line (start -7.62 -3.84) (end -7.92 -4.14) (layer F.SilkS) (width 0.12))
            (fp_line (start -6.22 -5.84) (end -6.22 5.86) (layer F.SilkS) (width 0.12))
            (fp_line (start -2.12 -5.84) (end -6.22 -5.84) (layer F.SilkS) (width 0.12))
            (fp_line (start -2.12 5.86) (end -6.22 5.86) (layer F.SilkS) (width 0.12))
            (fp_line (start 5.98 5.86) (end 1.88 5.86) (layer F.SilkS) (width 0.12))
            (fp_line (start 1.88 -5.94) (end 5.98 -5.94) (layer F.SilkS) (width 0.12))
            (fp_line (start -6.12 -4.74) (end -5.12 -5.84) (layer F.Fab) (width 0.12))
            (fp_line (start -6.12 5.76) (end -6.12 -4.74) (layer F.Fab) (width 0.12))
            (fp_line (start 5.88 5.76) (end -6.12 5.76) (layer F.Fab) (width 0.12))
            (fp_line (start 5.88 -5.84) (end 5.88 5.76) (layer F.Fab) (width 0.12))
            (fp_line (start -5.12 -5.84) (end 5.88 -5.84) (layer F.Fab) (width 0.12))
            (fp_line (start -8.87 -6.89) (end 7.88 -6.89) (layer F.CrtYd) (width 0.05))
            (fp_line (start -8.87 -6.89) (end -8.87 6.81) (layer F.CrtYd) (width 0.05))
            (fp_line (start 7.88 6.81) (end 7.88 -6.89) (layer F.CrtYd) (width 0.05))
            (fp_line (start 7.88 6.81) (end -8.87 6.81) (layer F.CrtYd) (width 0.05))
            (fp_circle (center -0.12 -0.04) (end 2.88 -0.04) (layer F.SilkS) (width 0.12))
            (fp_circle (center -0.12 -0.04) (end 2.88 -0.04) (layer F.Fab) (width 0.12))

            ${''/* pin names */}
            (pad A thru_hole rect (at -7.62 -2.54 ${p.r}) (size 2 2) (drill 1) (layers *.Cu *.Mask) ${p.A})
            (pad C thru_hole circle (at -7.62 -0.04) (size 2 2) (drill 1) (layers *.Cu *.Mask) ${p.C})
            (pad B thru_hole circle (at -7.62 2.46) (size 2 2) (drill 1) (layers *.Cu *.Mask) ${p.B})
            (pad 1 thru_hole circle (at 6.88 -2.54) (size 1.5 1.5) (drill 1) (layers *.Cu *.Mask) ${p.from})
            (pad 2 thru_hole circle (at 6.88 2.46) (size 1.5 1.5) (drill 1) (layers *.Cu *.Mask) ${p.to})

            ${''/* Legs */}
            (pad "" thru_hole rect (at -0.12 -5.64 ${p.r}) (size 3.2 2) (drill oval 2.8 1.5) (layers *.Cu *.Mask))
            (pad "" thru_hole rect (at -0.12 5.56 ${p.r})  (size 3.2 2) (drill oval 2.8 1.5) (layers *.Cu *.Mask))
        )
    `
    }
}
