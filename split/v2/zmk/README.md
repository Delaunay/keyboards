# Split v2 ZMK firmware

Wireless split firmware for the keyboard in `split/v2`. The dongle is a Seeed Studio XIAO BLE (nRF52840) and is the USB central. Each half is a nice!nano v2 peripheral, so neither half talks to the computer on its own.

The shield is written for the PCB as built: 6 columns, 5 rows, 4 thumb keys, and an EC11 encoder whose push switch sits on its own matrix row. Diodes point from column to row. The right half is this board mirrored, with its columns listed inner-to-outer so the keymap still reads left to right.

## Build

This folder is the ZMK config for split v2. Another keyboard gets the same files under its own directory, plus a job in `.github/workflows/build.yml`.

GitHub only runs workflow files stored at the repository root, so `.github/workflows/build.yml` stays there and calls `.github/workflows/zmk.yml` with `keyboard_dir: split/v2/zmk`. That job copies `config/` into its own west workspace. ZMK's shared workflow cannot do that for a nested folder: `west init -l split/v2/zmk/config` creates the workspace inside `split/v2/zmk`, and the next step runs `west update` from the repository root, where no workspace exists.

The workflow builds five UF2 files:

| Artifact | Flash onto |
|---|---|
| `splitv2_dongle` | the XIAO BLE dongle |
| `splitv2_left` | the left nice!nano |
| `splitv2_right` | the right nice!nano |
| `splitv2_dongle_settings_reset` | the XIAO BLE, once, before the first real flash |
| `splitv2_settings_reset` | each nice!nano, once, before the first real flash |

`west.yml` pins ZMK v0.3, so the dongle board is `seeeduino_xiao_ble` and the halves are `nice_nano_v2`. Newer ZMK renamed those to `xiao_ble//zmk` and `nice_nano//zmk`. A settings-reset UF2 is built for each board, because the two boards do not share a flash layout.

## First flash

1. Double-tap reset on a board so it shows up as a USB drive. On the XIAO BLE the button is the small one beside the USB-C port.
2. Copy `splitv2_dongle_settings_reset` to the XIAO, and `splitv2_settings_reset` to each nice!nano. Wait for the board to reboot. This clears old Bluetooth bonds.
3. Flash `splitv2_dongle` to the XIAO, and `splitv2_left` and `splitv2_right` to the halves.
4. Power the halves. They pair to the dongle by themselves.
5. Plug the dongle into the computer. It is the keyboard.

Later keymap edits only need the dongle reflashed. Pin or matrix changes need all three boards.

Hold the top-left key and tap the key under F1 to unlock [ZMK Studio](https://zmk.studio/) over USB. After Studio saves a keymap, further edits to `splitv2.keymap` are ignored until Studio's "Restore stock settings".

## Layout

Base layer, left then right:

```
Esc  F1 F2 F3 F4 F5          F6 F7 F8 F9 F10 F11
`    1  2  3  4  5           6  7  8  9  0   -
Tab  Q  W  E  R  T           Y  U  I  O  P   Bksp
Ctrl A  S  D  F  G           H  J  K  L  ;   '
Shft Z  X  C  V  B           N  M  ,  .  /   Shft
       Ctrl Alt Space Gui    Enter Space Alt Ctrl
```

`Esc` is a layer-tap: tap for Escape, hold for the system layer. Both `Space` thumbs are layer-taps: tap for Space, hold the left one for Nav and the right one for Symbols. The left knob is volume, and its push is mute. The right knob is page up and page down, and its push is play/pause.

Hold the left `Space` for arrows and a numpad. Hold the right `Space` for symbols. Backspace stays on the key after `P`.

System layer, while holding the top-left key:

| Key | Action |
|---|---|
| F1 | unlock ZMK Studio |
| backtick | clear Bluetooth bonds on the dongle |
| 1 through 5 | Bluetooth profiles 0 through 4 |
| 6 | USB output |
| 7 | BLE output |
| right Shift | dongle bootloader |

To put a half into the bootloader, double-tap its reset button. The bootloader key only resets the dongle, because that is where the keymap runs.

## Power

The AAA holder on the PCB is tied to the nice!nano RAW / VDDH pad. That pad is the LiPo input. A single AAA cell is below the voltage the nice!nano expects there, and the onboard charger is for a lithium battery. Power each half with a LiPo on the battery pads.

## If a side feels backwards

The right knob's A and B pins are swapped in `splitv2_right.overlay` so clockwise matches the left knob. If the right knob goes the wrong way, swap those two `gpios` lines back.

A 30-detent encoder is set to `steps = <120>` and 30 triggers per turn. If one click does nothing, or fires twice, try `steps` of 60 or 80 in `splitv2.dtsi`.
