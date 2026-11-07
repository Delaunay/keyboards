// Kailh Choc hotswap socket, soldered on the back.
// Pad 1 is the column, pad 2 is the diode.
module.exports = {
    params: {
        designator: 'HS',
        from: undefined,
        to: undefined
    },
    body: p => `
      (module Kailh_Choc_Hotswap (layer B.Cu) (tedit 5DD50112)
      ${p.at}

      (fp_text reference "${p.ref}" (at 2.5 -9.2 ${p.r}) (layer B.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))
      (fp_text value "Kailh_Choc_Hotswap" (at 2.5 -9.2 ${p.r}) (layer B.Fab) hide (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))

      (fp_line (start -4.8 -7.5) (end 9.8 -7.5) (layer B.SilkS) (width 0.12))
      (fp_line (start 9.8 -7.5) (end 9.8 -2.2) (layer B.SilkS) (width 0.12))
      (fp_line (start 9.8 -2.2) (end -4.8 -2.2) (layer B.SilkS) (width 0.12))
      (fp_line (start -4.8 -2.2) (end -4.8 -7.5) (layer B.SilkS) (width 0.12))

      (pad "" np_thru_hole circle (at 5 -3.75) (size 3 3) (drill 3) (layers *.Cu *.Mask))
      (pad "" np_thru_hole circle (at 0 -5.95) (size 3 3) (drill 3) (layers *.Cu *.Mask))
      (pad 1 smd rect (at -3.275 -5.95 ${p.r}) (size 2.6 2.6) (layers B.Cu B.Paste B.Mask) ${p.from})
      (pad 2 smd rect (at 8.275 -3.75 ${p.r}) (size 2.6 2.6) (layers B.Cu B.Paste B.Mask) ${p.to})

      ${''/* column via on the key centerline, just clear of the stem */}
      (pad 1 thru_hole circle (at 0 -3.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu) ${p.from})
      ${''/* back-side link from the column pad to that via */}
      (pad 1 smd rect (at -3.275 -4.575 ${p.r}) (size 0.5 2.75) (layers B.Cu) ${p.from})
      (pad 1 smd rect (at -1.6375 -3.2 ${p.r}) (size 3.275 0.5) (layers B.Cu) ${p.from})
      )
    `
}