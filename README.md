# About T-BUG

**T-BUG (Tiny-Bad USB Gadget)** is an open-source penetration testing device that emulates a **HID (Human Interface Device)**—such as a keyboard or mouse—to automatically execute scripts, commands, or payloads on the host computer it’s plugged into.
It is designed for ethical hackers, programmers, electronics hobbyists, and even complete beginners who want a compact, programmable USB tool. Whether you're using it for something as simple as simulating mouse movements or as advanced as executing a sequence of commands to perform a specific task, T-BUG is adaptable to your use case.
At its core, T-BUG is powered by the **Raspberry Pi RP2040 microcontroller**, paired with **2MB of onboard flash storage**—sufficient for most automation or payloads.
T-BUG features a **built-in RGB LED** to indicate the current execution stage of the active script, and a **capacitive touch sensor/button** whose function can vary depending on the script.

We at **Nefarious Engineering** provide several plug-and-play scripts for quick use, but if you have experience with embedded systems or even just basic Python programming, you can easily write your own scripts and upload them to T-BUG.

The device runs on CircuitPython, a fork of MicroPython developed by Adafruit Industries, which makes development easy and accessible—especially for Python users.

You can find source code, sample scripts, and development resources for T-BUG on our [GitHub page](https://github.com/Nefarious-Engineering/tbug)

## Legal Disclaimer

T-BUG is intended for ethical and educational use only. Unauthorized use of this device on systems you do not own or have permission to test is illegal.

# Getting Started

The T-BUG device is designed for both technical users and complete beginners. If you've purchased a fully assembled unit or built your own using the provided files, this section helps you get started without needing to write any code.

## How to Get T-BUG

You can get T-BUG in two ways:

1. Pre-Assembled (Plug-and-Play)
   A ready-to-use T-BUG can be purchased from the Nefarious Engineering website (_coming soon_).

2. DIY / Self-Assembled
   All required files, code, case designs, and instructions are available in the [T-BUG GitHub repository](https://github.com/Nefarious-Engineering/tbug) to build and program it yourself.

## Using T-BUG Out of the Box

When you plug in a pre-assembled T-BUG, it will automatically begin executing the default script, such as:

> User Activity Emulation – prevents the system from sleeping or locking or going idle by simulating user input.

## Basic Controls

- **Touch Sensor:**
  Tap the top of the device (where the capacitive touch button is located) to toggle the script ON or OFF. This is the default behavior for the Touch button but it may vary from script to script. Refer to the [Script Descriptions](#script-descriptions) section for touch sensor behavior in each script.

- **RGB LED Indicator:**
  The built-in LED shows the current script stage. Refer to the [Script Descriptions](#script-descriptions) section for color codes and behavior.

## Want to Try a Different Script?

T-BUG currently supports only one active script at a time, defined in the main.py file. However running multiple scripts can be done using custom scripts/programs.

To change the script (no coding required):

- Follow the steps in the [Development Section](#development) to expose the CIRCUITPY drive (T-BUG's Flash Storage) and upload a new script to your T-BUG.

## Important Notes for New Users

- Do not unplug T-BUG while it's running a script to avoid unexpected behavior.
- > [!WARNING]
  > Make sure to only use T-BUG on systems you own or have permission to test.

# Script Descriptions

## User Activity Emulation Script

The **User Activity Emulation** script is a preloaded example on the T-BUG that simulates user presence on a computer (useful for preventing auto-lock or sleep mode).
Here’s how it works:

1. The capacitive touch button toggles the emulation script ON or OFF.
2. The RGB LED provides visual feedback indicating the current stage of execution using the following color codes:

   - `rgb(255,0,0)` Idle Stage (Red Colour)
   - `rgb(0,255,0)` Mouse Movement Emulation Stage (Green Colour)
   - `rgb(255,0,255)` Mouse Left Click Stage (Pink Colour)
   - `rgb(255,255,0)` Shift Keystroke Stage (Yellow Colour)
   - `rgb(255,120,0)` Caps Lock Keystroke Stage (Orange Colour)

   This allows the user to quickly identify what action is being performed just by looking at the LED.

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

If you wish to modify the default behaviour of the “User Activity Emulation” Script, you can edit the Python code accordingly.
The script is available in the T-BUG GitHub repository. For details on editing the code and uploading it to your T-BUG device, refer to the Development section of this documentation.

# Development

By default, T-BUG is configured such that its CircuitPython flash storage (CIRCUITPY) is not visible on the host computer. This is done intentionally to prevent tampering or accidental modification during normal usage. To begin developing your own scripts or modifying existing ones, follow the setup process below.

## Required Files

Download the following files from the T-BUG [GitHub repository](https://github.com/Nefarious-Engineering/tbug):

1. flash_nuke.uf2 – Formats T-BUG’s internal flash storage.

2. adafruit-circuitpython-waveshare_rp2040_zero-en_US-9.2.8.uf2 or new available – CircuitPython firmware for the RP2040 Zero board.

3. adafruit_hid library – Required for USB HID emulation (keyboard/mouse input).

4. neopixel library – Required to control the onboard RGB LED.

## Entering Bootloader Mode

1. Plug in T-BUG to your computer via USB.

2. Press and hold both the RESET and BOOT buttons.

3. While holding the BOOT button, release the RESET button.

4. Then release the BOOT button.

A new USB drive named RPI-RP2 should now appear on your computer.

## Formatting Flash (Optional but Recommended)

1. Copy the flash_nuke.uf2 file into the RPI-RP2 drive.
   This erases and reformats the internal flash.
2. The device will automatically reboot and reappear as RPI-RP2.

## Installing CircuitPython Firmware

1. Copy the CircuitPython firmware UF2 file (adafruit-circuitpython-waveshare_rp2040_zero-en_US-9.2.8.uf2) into the RPI-RP2 drive.
2. T-BUG will reboot and mount as a new USB drive named CIRCUITPY.

## Setting Up Required Libraries

1. Inside the CIRCUITPY drive, open the lib folder. If it doesn’t exist, create it manually.

2. Copy the following into the lib folder:
   - adafruit_hid/
   - neopixel.mpy

## Writing and Uploading Your Script

### Using Prebuilt Scripts (for Non-Programmers)

If you're not interested in writing your own code, you can simply use the prebuilt CircuitPython scripts provided in the [T-BUG GitHub repository](https://github.com/Nefarious-Engineering/tbug).
To use a different script:

1. Follow the steps above to install CircuitPython and set up your CIRCUITPY drive (if not done already).

2. Download script files named main.py and boot.py from the scripts/ folder in the T-BUG GitHub repository.

3. Copy both the files to the root of the CIRCUITPY drive (replace the existing main.py if any).

   > [!NOTE]
   > Copying boot.py into the CIRCUITPY drive will result in hiding the CIRCUITPY drive the next time T-BUG boots, so if you are simply trying different available T-BUG scripts then do not copy the boot.py file inside the T-BUG flash otherwise you have to perform the above mentioned steps again in order to regain access to the CIRCUITPY drive. Once you have finalized a T-BUG script then you can safely copy the boot.py file into CIRCUITPY drive.

4. Replug T-BUG. The new script will execute automatically.

This allows anyone to change T-BUG's behavior without needing to write or edit code.

### Using Custom Scripts (for Programmers)

1. In the root of the CIRCUITPY drive, create a file named main.py.
2. Write your script using CircuitPython syntax and libraries.
   To get started, you can refer to:

   - 📘 [Adafruit CircuitPython Documentation](https://docs.circuitpython.org/en/latest/README.html)

   - 💡 Example scripts on the T-BUG [GitHub repository](https://github.com/Nefarious-Engineering/tbug)

## Pin Connections

Refer to the attached GPIO connection diagram to see which pins are used for:

- RGB LED control (via Neopixel)

- Capacitive Touch Sensor/Button

This helps ensure your custom scripts interact correctly with the onboard components.

Additionally, a complete pinout diagram of the Waveshare RP2040-Zero board is included in this documentation.
This is useful if you want to connect or solder additional sensors, buttons, or peripherals to T-BUG for your own specific use case or advanced applications.

## Developer Notes

- T-BUG is compatible with many libraries from the CircuitPython ecosystem.

- Most automation and payload features use the adafruit_hid library.

- The onboard RGB LED is programmable using the neopixel library to indicate status, error states, or stages in script execution.

- You can use editors like Thonny, Mu, or VS Code for writing your scripts.

# 3D Printed Case

The T-BUG 3D printed case is designed to securely house the Waveshare RP2040-Zero board and the onboard capacitive touch sensor/button module. It is a snap-fit case, meaning no screws or glue are required to hold the RP2040-Zero board in place.

However, a small piece of double-sided tape is recommended to securely attach the capacitive touch sensor/button module/PCB to the top part of the T-BUG case.

If you plan to add additional components or sensors—such as extra buttons, displays, or external modules—you may need to redesign or modify the case to accommodate those parts.
The STL files and editable design files for the case are available in the T-BUG [GitHub repository](https://github.com/Nefarious-Engineering/tbug), allowing you to customize the enclosure using your preferred 3D modeling software.

> The default T-BUG v1 case includes cutouts for USB access, RGB LED visibility, and to access the RESET and BOOT buttons.

# Hardware Assembly

This section explains how to assemble your T-BUG device, including the required components and step-by-step soldering instructions.

## Required Hardware Components

1. Waveshare RP2040-Zero development board

2. TTP223 Capacitive Touch Sensor module

3. Thin enameled copper wires – 3 pieces (for signal and power connections)

4. Double-sided tape – to mount the touch sensor inside the case

5. 3D Printed Case (recommended) or any alternative method to secure the electronics

## Required Soldering Tools

- Soldering Iron with Fine Tip
- Solder Wire (leaded or lead-free, as per user preference)
- Desoldering Pump (optional, useful for correcting mistakes)
- Soldering Mat (optional, but recommended for safety and organization)

## Soldering & Assembly Instructions

1. Prepare the Wires

   - Roughly position the RP2040-Zero and the TTP223 module in the 3D printed case to determine exact wire length.

   - Cut three pieces of enameled copper wire.

   - Length should be enough to reach from the RP2040-Zero board to the touch sensor position outside the case.

   - Remove the enamel coating from both ends using a soldering iron or fine abrasive tool.

2. Solder Wires to Touch Sensor

   - Solder the wires to the through-hole pads of the TTP223 touch sensor:
     | TTP223 Pins |
     | ----------- |
     | VCC |
     | I/O |
     | GND |

3. Solder Wires to RP2040-Zero Board

   - Pass all three wires through the RGB LED hole in the top case. This allows correct routing to the touch sensor, which will be mounted on the top half of the case.

   - Solder the wires to the following pads on the Waveshare RP2040-Zero:
     | TTP223 Pins | RP2040-Zero Pins |
     | ----------- | ----------- |
     | VCC | 3.3V |
     | I/O | GPIO15 |
     | GND | GND |

4. Mount the Touch Sensor

   - Secure the TTP223 module to the top half of the case (over the USB Type-C Port shell) using a piece of double-sided tape.

5. Final Case Assembly

   - Place the RP2040-Zero board into the bottom half of the 3D printed case.
   - Carefully snap the top and bottom halves together, ensuring:
     - Wires are not pinched or strained
     - RGB LED visibility cutout and USB port alignment are correct

## Coming Soon: Custom T-BUG PCB

The current design uses a Waveshare RP2040-Zero board and a separate TTP223 capacitive touch sensor, but in future versions, these will be replaced by a custom-designed T-BUG PCB.

- This PCB will integrate the RP2040 microcontroller and touch sensor on a single board.

- Once finalized, the schematics, PCB files, and Gerbers will be made available on the [T-BUG GitHub repository](https://github.com/Nefarious-Engineering/tbug).
