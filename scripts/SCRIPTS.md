# Scripts Guide

This document holds the scripts index, short descriptions, and information related to development and contribution. 
Detailed per-script documentation lives inside each script folder (`scripts/<script-name>/SCRIPT_DOC.md`).
Main project information (hardware, development, assembly) remains in the primary `README.md`. 

> **Legal / Safety note — read first**
>
> The scripts in this directory may perform sensitive actions. Use them **only** on systems you own or where you have explicit written permission to test. Misuse may be unlawful. The project authors disclaim liability for misuse.

---

## Table of contents

- [How scripts are organized](#how-scripts-are-organized)
- [Script Index](#script-index)
- [How to add a new script (developer guide)](#how-to-add-a-new-script-developer-guide)
- [Contribution checklist & PR template](#contribution-checklist--pr-template)

## How scripts are organized
```python
/ tbug (repo root)
├─ development_resources/
│ ├─ circuitpython_firmware  # Contains the main firmware
│ ├─ circuitpython_libraries # Required libraries for this project
│ └─ factory_reset/          # Contains the firmware to reset T-BUG device
├─ images/                   # Contains Project Images
├─ scripts/                  # repo folder with example scripts
│ └─ SCRIPTS.md              # this file
│ └─ <script_name>/
│ ├─ assets/                 # optional (script example images, etc)
│ ├─ main.py                 # CircuitPython script for T-BUG (RP2040)
│ ├─ boot.py                 # Controls early boot behavior of T-BUG
│ ├─ additional script files # optional, if required
│ └─ SCRIPT_DOC.md           # Detailed Script documentation (usage, troubleshooting, limitations, etc.)
│ └─ manifest.yml            # metadata (name, version, author, license)
└─ .gitignore
└─ LICENSE                   # Project Open Source License
└─ README.md                 # Project Main Documentation
```

## Script Index

### User Activity Emulation Script
- **Location:** `scripts/user_activity_emulation/`
- **Purpose:** Simulates mouse movement, occasional clicks and keystrokes to prevent idle/sleep.
- **Documentation:** [User Activity Emulation Script](./user_activity_emulation/SCRIPT_DOC.md) — full usage, installation, safe testing, troubleshooting.

### Fetch Wi-Fi Credentials Script
- **Location:** `scripts/fetch_wifi_credentials/`
- **Purpose:** Two-stage, touch-driven script that extracts locally stored Windows SSID/key pairs (via `netsh`) and saves them to the Desktop.
- **Documentation:** [Fetch Wi-Fi Credentials Script](./fetch_wifi_credentials/SCRIPT_DOC.md) — full usage, installation, safe testing, troubleshooting, and notes about UAC/admin limitations.

## How to add a new script (developer guide)
```python
scripts/
 └─ my-script/
    ├─ main.py              # CircuitPython script for T-BUG (RP2040)
    ├─ boot.py              # Controls early boot behavior of T-BUG
    ├─ assets/              # optional (script example images, etc)
    ├─ additional files     # optional (.ps1, .bat, .sh) files used on host
    ├─ SCRIPT_DOC.md        # Detailed Script documentation (usage, troubleshooting, limitations, etc.)
    └─ manifest.yml         # metadata (name, version, author, license)
```

1. Create a new folder in `scripts/` with your `<script_name>`
2. Add `main.py` with your CircuitPython code
3. Add any required assets or host-side scripts
4. Write a detailed or short `SCRIPT_DOC.md` for usage instructions, limitations, etc.
5. Create a `manifest.yml` with metadata:
    ```yaml
    name: fetch-wifi
    title: Fetch Wi-Fi Credentials
    version: 1.0
    author: Your Name
    description: "Two-stage script to gather locally-saved SSIDs and keys (authorized testing only)."
    requires:
      - adafruit_hid
      - neopixel
    license: GPL-3.0
    ```
6. Contents of `SCRIPT_DOC.md` should include:
    - Short purpose
    - Files (list)
    - Installation steps (copy to CIRCUITPY, test steps)
    - Troubleshooting
    - Safety note

## Contribution checklist & PR template
When submitting a script PR:
  - Include `manifest.yml`.
  - Add a `SCRIPT_DOC.md` inside the `<script_name>` folder explaining setup and testing steps, etc.
  - Include only necessary files; do not include large binaries.
  - Test on a non-production, authorized Windows machine.
  - Add a short note about potential UAC/admin requirements if any.
  - Add license header or reference (same license as project)

Summary:
- Script name:
- Purpose:
- Files added:
- How I tested (two sentences):
- Potential security/privilege notes:

Checklist:
- [ ] `manifest.yml` included
- [ ] `SCRIPT_DOC.md` included
- [ ] Tested locally on Windows or Linux (non-production system)