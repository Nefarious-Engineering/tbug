# Fetch Wi-Fi Credentials — Script Documentation

This document holds detailed documentation for the T-BUG Fetch Wi-Fi Credentials script. Use it only on machines you own or are authorized to test.
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
- [LED states / UX](#led-states--ux)
- [Testing procedure (safe)](#testing-procedure-safe)
- [Troubleshooting & common fixes](#troubleshooting--common-fixes)
- [Limitations & notes](#limitations--notes)

### Purpose & scope

- **Purpose:** Read saved Windows Wi-Fi profiles and write SSID / key pairs to a file.
- **Mode:** Two-stage, touch-driven. First touch performs extraction; second touch writes output to Desktop.
- **State handling:** Script stores a `state.txt` on `CIRCUITPY` to persist stage across reboots.

### Files required

Place these files in the CIRCUITPY root (same disk that shows up on Windows):

- `main.py` — CircuitPython script for T-BUG (RP2040).
- `boot.py` — Controls early boot behavior of T-BUG.
- `extract.ps1` — PowerShell script to extract profiles and write `wifi_dump.txt` and `state.txt`.
- `output.ps1` — PowerShell script to read `wifi_dump.txt` and write `WiFi_Credentials.txt` to Desktop, then clear and set state to `IDLE`.
- `reset.ps1` — Sets `state.txt` to `IDLE` in case of no WiFi data found.
- `lib/` — required CircuitPython libraries (e.g., `adafruit_hid`, `neopixel`) placed in `CIRCUITPY/lib/`.

> Note: `main.py` is the RP2040 code. The `.ps1` files are executed on the Windows host (typed by HID device into a visible PowerShell window).

### Installation

1. Copy `main.py`, `boot.py`, and the three `.ps1` files to the CIRCUITPY drive root.
2. Ensure the drive is readable by the Windows host system.
3. Reinsert the device. Watch the RP2040 serial (or LED) to confirm ready state.

### How it works (high level)

- `main.py` waits for touch. On first touch it opens a visible PowerShell window (via Win+R, `powershell`), then types commands to call `extract.ps1` from the CIRCUITPY drive.
- `extract.ps1` uses `netsh wlan show profiles` and `netsh wlan show profile name="<ssid>" key=clear` to collect SSIDs and keys, writes results to `wifi_dump.txt` on the CIRCUITPY drive and writes `WAITING` into `state.txt`.
- `main.py` detects `state.txt == WAITING` and sets its internal state to WAITING. The second touch triggers `output.ps1`.
- `output.ps1` tidies the format and writes `WiFi_Credentials.txt` on the user's Desktop, clears `wifi_dump.txt`, and sets `state.txt` back to `IDLE`.

### LED states / UX

- **Red** — IDLE / ready to start
- **Blue** — Extraction in progress
- **Yellow** — Waiting for output trigger
- **Green** — Output created and finishing

(The exact colors used are in `main.py` and can be changed there.)

### Testing procedure (safe)

1. Test first on a Windows test machine you control.
2. Plug T-BUG into machine; confirm `CIRCUITPY` is visible.
3. Open PowerShell manually and run `extract.ps1` directly from the drive to validate the PowerShell output before letting HID type it. Example: `& "E:\extract.ps1"` where `E:` is CIRCUITPY on your machine.
4. Confirm `wifi_dump.txt` appears on `CIRCUITPY`.
5. Run `output.ps1` manually and confirm `WiFi_Credentials.txt` appears on Desktop with readable lines.
6. Once `.ps1` scripts behave reliably, test `main.py` device-driven flow.

### Troubleshooting & common fixes

**Problem A — `wifi_dump.txt` is empty after extraction**
- Run `extract.ps1` manually from an elevated PowerShell and check the `netsh` output.
- Make sure the host has profiles stored and `netsh` returns the "All User Profile" lines.
- Check the regex used in the script. For robustness use `Select-String "All User Profile\s*:\s*(.+)$"` or better: parse lines defensively (see corrected example below).

**Problem B — PowerShell error: `Variable reference is not valid. ':' was not followed by a valid variable name character.`**
- Don’t build paths with `"$cp:\file"`; PowerShell treats `"$cp:"` as a variable interpolation problem. Use `Join-Path` or `${cp}:` format.
  - Good: `Join-Path "${cp}:" "wifi_dump.txt"`
  - Or use: `$script = Join-Path "${cp}:" "extract.ps1"`

**Problem C — HID typing into the wrong window (e.g., editor)**
- When using visible PowerShell, ensure PowerShell has focus before typing:
  - `main.py` must wait adequate time after launching `powershell` (increase `time.sleep()`).
  - Avoid typing too quickly — add small `sleep` between `layout.write` and `ENTER`.
- While developing, keep an eye on the host and test slowly.

**Problem D — UAC (User Account Control) prompts or denied commands**
- `netsh wlan show profile` is usually allowed for the current user without elevation; however some systems policy or protected profiles might block access.
- If a UAC prompt appears for `powershell` or some command, the HID approach cannot bypass UAC. Manual consent will be required. See Limitations below.

**Corrected patterns & safe PowerShell snippets**

Use `Join-Path` to create file paths (avoids interpolation issues):
```powershell
$cp = (Get-Volume -FileSystemLabel "CIRCUITPY").DriveLetter
if (-not $cp) { exit }

$out = Join-Path "${cp}:" "wifi_dump.txt"
$state = Join-Path "${cp}:" "state.txt"

$results = @()
(netsh wlan show profiles) |
  Select-String "All User Profile\s*:\s*(.+)$" |
  ForEach-Object {
    $match = $_.Matches[0].Groups[1].Value.Trim()
    if ($match) {
      $ssid = $match
      $profile = netsh wlan show profile name="$ssid" key=clear
      $keyLine = ($profile | Select-String "Key Content\s*:\s*(.+)$")
      if ($keyLine) {
        $results += "$ssid : $($keyLine.Matches[0].Groups[1].Value)"
      }
    }
  }

$results | Out-File -Encoding ASCII $out
Set-Content -Encoding ASCII $state "WAITING"
```
### Limitations & notes
- **UAC:** if PowerShell or a command in the script requires elevation (UAC), the HID device cannot programmatically approve UAC prompts. Manual user acceptance will be required on such hosts.

- **Protected profiles / enterprise policies:** corporate machines frequently restrict netsh access or store credentials with extra protections — scripts may fail or return nothing.

- **Cross-Windows variations:** output of netsh might vary by Windows build/language. If you target non-English hosts, adjust regex or parsing accordingly.

- **Ethics & legality:** do not run these scripts on systems you do not own or have explicit permission to test.