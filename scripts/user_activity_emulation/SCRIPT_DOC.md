# User Activity Emulation — Script Documentation

This document holds detailed documentation for the T-BUG User Activity Emulation script. Use it only on machines you own or are authorized to test.
Main project information (hardware, development, assembly) remains in the primary `README.md`.
This page is for script *usage*, *installation*, *testing*, *troubleshooting*, and *limitations* details.

> **Legal / Safety note — read first**
>
> The scripts in this directory may perform sensitive actions. Use them **only** on systems you own or where you have explicit written permission to test. Misuse may be unlawful. The project authors disclaim liability for misuse.

---

## Table of contents

- [Purpose & scope](#purpose--scope)
- [Files required](#files-required)
- [Installation](#installation)
- [How it works (high level)](#how-it-works-high-level)
- [Script Sequence Overview](#script-sequence-overview)
- [LED states / UX](#led-states--ux)
- [Testing procedure (safe)](#testing-procedure-safe)
- [Troubleshooting & common fixes](#troubleshooting--common-fixes)
- [Limitations & notes](#limitations--notes)

### Purpose & scope

- **Purpose:** Simulate simple, human-like user activity (mouse movement, occasional clicks and keystrokes) to prevent idle lock / screen-saver / sleep for testing or convenience.
- **Scope:** Lightweight, non-invasive emulation intended for single-user test machines (not for bypassing corporate security or attacking systems).
- **Mode:** Single-button toggle (capacitive touch) with visual feedback via onboard RGB Neopixel.

### Files required

Place these files in the CIRCUITPY root:

- `main.py` — CircuitPython script for T-BUG (RP2040) implementing the user activity emulation behavior.
- `boot.py` — *optional* (only copy if you want CIRCUITPY hidden after deployment).
- `lib/` — required CircuitPython libraries (e.g., `adafruit_hid`, `neopixel`) placed in `CIRCUITPY/lib/`.

> [!NOTE]
> This script runs entirely on the device and does not require any host-side scripts.

### Installation

1. Mount the CIRCUITPY drive (follow the main README Development section).
2. Copy `main.py` to the root of CIRCUITPY.
3. Copy the `lib/` dependencies into `CIRCUITPY/lib/`.
4. (Optional) Add `boot.py` if you want to hide the CIRCUITPY drive on next boot.
5. Safely eject and reinsert the device. The device will run `main.py` automatically.

### How it works (high level)

1. On boot, `main.py` initializes the capacitive touch input, the Neopixel, and the HID interfaces.
2. The device stays in **IDLE** state until the touch sensor toggles the emulation ON.
3. When active, the script loops through small stages that emulate human activity:
   - move mouse cursor in a smooth circular/oscillating motion,
   - perform a left mouse click after a configurable delay,
   - occasionally send a keystroke (Shift or Caps Lock) to keep the session alive.
4. The touch sensor toggles the emulation ON/OFF. LED color reflects the current stage so you can quickly see what it is doing.

### Script Sequence Overview

When the user enables the script:

1. **Mouse Movement Stage:**
   The mouse cursor begins moving in a circular pattern to simulate user interaction.
2. **Left Click Execution:**
   After a specific delay, a left-click is performed.
3. **Cursor Position Randomization:**
   The mouse pointer is moved to random screen coordinates, then the process repeats.
4. **Keystroke Injection Stage:**
   Periodically, the entire mouse emulation sequence is paused, and either a Shift keystroke or Caps Lock keystroke is sent to the host machine.

> [!NOTE]
> The script tracks the last key sent, and alternates between Shift and Caps Lock to avoid repetition.

5. **Resume Loop:** After the keystroke is sent, the script resumes its normal operation starting from the mouse movement stage.

> [!NOTE]
> A delay is added after each stage to make the emulated user activity feel natural and human-like.

If you wish to modify the default behaviour of the “User Activity Emulation” script, you can edit the Python code accordingly.
The script is available in the T-BUG GitHub repository. For details on editing the code and uploading it to your T-BUG device, refer to the Development section of the primary `README.md`.

### LED states / UX

The RGB LED indicates current state/stage:

| Stage                        | Colour |
| :--------------------------: | :----: |
| Idle / Not running           | Red    |
| Mouse movement emulation     | Green  |
| Mouse left click stage       | Pink   |
| Keystroke injection (Shift)  | Yellow |
| Keystroke injection (Caps)   | Orange |

(Colors correspond to values set in `main.py` and can be changed there.)

### Testing procedure (safe)

1. Use a test machine you control.
2. Ensure `CIRCUITPY` is visible and `main.py` is present.
3. Plug in T-BUG. Confirm LED shows **Red** (Idle).
4. Tap the touch pad once. LED should change to **Green** and the mouse should begin moving slowly.
5. Observe that after the configured movement period a left-click occurs (cursor may move slightly).
6. After the configured keystroke interval, a Shift or Caps Lock keystroke is sent — verify this by opening a text editor and observing that no actual characters are inserted (Shift/Caps Lock toggles modifier state only).
7. Tap the touch pad again to stop; LED should return to **Red**.

### Troubleshooting & common fixes

**Problem A — Device appears to do nothing**
- Confirm `CIRCUITPY` has `main.py` and required `lib/` packages.
- Check serial output (Thonny) for errors at boot (missing libraries often throw `ImportError`).
- Ensure the touch sensor wiring/pad is correctly connected (GPIO15 by default) and not always triggered.

**Problem B — HID actions type into the wrong window / no effect**
- The HID events act on whatever window is focused on the host. Open a simple text editor or move the mouse to the desktop to observe movement.
- Some apps or OS settings can suppress simulated input (e.g., secure kiosks, RDP sessions). Test on a local desktop.

**Problem C — Movements are too fast / unnatural**
- Edit timing constants in `main.py` (delays between steps, movement step size) to make movement more human-like.

**Problem D — Keystroke behavior undesirable**
- The script alternates Shift and Caps Lock to avoid repeated identical inputs. If Caps Lock toggling is problematic, change the keystroke to an innocuous key (e.g., F15 — if not used on the host) or remove keystroke stage.

**Problem E — LED not changing color**
- Make sure `neopixel` library is present and the LED gpio pin assignment matches the hardware. If the LED remains off, check power/wiring.

### Limitations & notes

- **Not a security bypass:** this script only simulates basic user activity; it cannot bypass lock screens that require explicit authentication, nor can it defeat corporate endpoint protections.

- **Focus-dependent:** HID input is delivered to the currently focused application on the host. It will not target hidden windows or applications that block synthetic input.

- **Platform differences:** behavior may vary across OS versions and desktop environments.

- **Ethics & legality:** use only on machines you own or are explicitly authorized to test. Do not use to circumvent workplace policies.