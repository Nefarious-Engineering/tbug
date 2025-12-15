import storage
import usb_cdc
import usb_hid

# Optional: keep REPL console, disable data serial
usb_cdc.enable(console=True, data=False)

# Enable HID devices (keyboard/mouse)
usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE))
