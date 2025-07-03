import time
import math
import board
import digitalio
import usb_hid
import neopixel
import random

from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize HID devices
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)

# Button setup (use GPIO15)
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# WS2812B LED on GPIO16
pixel = neopixel.NeoPixel(board.GP16, 1, brightness=0.3, auto_write=True)

# Simple RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 0, 127)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

def set_pixel_color(rgb):
    pixel[0] = rgb

jiggling = False
button_pressed = False
last_jiggle_time = time.monotonic()
last_center_shift = time.monotonic()
last_click_time = time.monotonic()
last_random_key_time = time.monotonic()
jiggle_interval = 0.05
click_interval = 5
center_shift_interval = 15
random_key_interval = 10
stage = "jiggle"
last_key = None

# Circle pattern parameters
angle = 0
angle_step = 0.1
amplitude = 80
center_x = 0
center_y = 0
prev_x = 0
prev_y = 0

print("Mouse Jiggler HID ready.")
set_pixel_color(RED)

while True:
    if not button.value and not button_pressed:
        jiggling = not jiggling
        button_pressed = True
        print("Jiggling started." if jiggling else "Jiggling stopped.")
        set_pixel_color(GREEN if jiggling else RED)
        stage = "jiggle"

    if button.value and button_pressed:
        button_pressed = False

    now = time.monotonic()

    if jiggling:
        if now - last_center_shift >= center_shift_interval:
            center_x = int((math.sin(now / 7) * 100))
            center_y = int((math.cos(now / 5) * 100))
            last_center_shift = now
            print("Shifting center to:", center_x, center_y)

        if stage == "jiggle":
            set_pixel_color(GREEN)
            if now - last_jiggle_time >= jiggle_interval:
                x = center_x + amplitude * math.cos(angle)
                y = center_y + amplitude * math.sin(angle)
                dx = int(x - prev_x)
                dy = int(y - prev_y)
                mouse.move(x=dx, y=dy)
                prev_x = x
                prev_y = y
                angle += angle_step
                if angle >= 2 * math.pi:
                    angle -= 2 * math.pi
                last_jiggle_time = now

            if now - last_click_time >= click_interval:
                stage = "click"
                last_click_time = now
                continue

            if now - last_random_key_time >= random_key_interval:
                if last_key == "capslock":
                    stage = "shift"
                else:
                    stage = "capslock"
                last_random_key_time = now
                continue

        elif stage == "click":
            set_pixel_color(PINK)
            print("Left click")
            mouse.click(Mouse.LEFT_BUTTON)
            time.sleep(1)
            stage = "jiggle"

        elif stage == "shift":
            set_pixel_color(YELLOW)
            print("Random Shift sent")
            keyboard.send(Keycode.SHIFT)
            last_key = "shift"
            time.sleep(2)
            stage = "jiggle"

        elif stage == "capslock":
            set_pixel_color(ORANGE)
            print("Random Caps Lock toggled")
            keyboard.send(Keycode.CAPS_LOCK)
            last_key = "capslock"
            time.sleep(2)
            stage = "jiggle"

    time.sleep(0.01)
