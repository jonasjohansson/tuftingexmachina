import time
import board
import touchio
import random
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_circuitplayground import cp

# Initialize the keyboard and NeoPixels
kbd = Keyboard(usb_hid.devices)
cp.pixels.brightness = 0.2

# Debounce settings and time to pause between loops
debounce_delay = 0.1  # seconds

# Initialize touch inputs and their thresholds and key groups
touch_inputs = {
    "A1": {
        "touch": touchio.TouchIn(board.A1),
        "threshold": 250,
        "keys": [Keycode.A, Keycode.B, Keycode.C],
        "pixel_index": 0,
    },
    "A2": {
        "touch": touchio.TouchIn(board.A2),
        "threshold": 250,
        "keys": [Keycode.D, Keycode.E, Keycode.F],
        "pixel_index": 1,
    },
    "A3": {
        "touch": touchio.TouchIn(board.A3),
        "threshold": 250,
        "keys": [Keycode.G, Keycode.H, Keycode.I],
        "pixel_index": 2,
    },
    "A4": {
        "touch": touchio.TouchIn(board.A4),
        "threshold": 250,
        "keys": [Keycode.J, Keycode.K, Keycode.L],
        "pixel_index": 3,
    },
    "A5": {
        "touch": touchio.TouchIn(board.A5),
        "threshold": 250,
        "keys": [Keycode.M, Keycode.N, Keycode.O],
        "pixel_index": 4,
    },
    "A6": {
        "touch": touchio.TouchIn(board.A6),
        "threshold": 250,
        "keys": [Keycode.P, Keycode.Q, Keycode.R],
        "pixel_index": 5,
    },
    "TX": {
        "touch": touchio.TouchIn(board.TX),
        "threshold": 250,
        "keys": [Keycode.S, Keycode.T, Keycode.U],
        "pixel_index": 6,
    },
}

# Initialize state dictionaries
last_touched_time = {key: 0 for key in touch_inputs}
previously_touched = {key: False for key in touch_inputs}


def debounce_and_press_logic(key, touch_data):
    current_time = time.monotonic()
    touch_value = touch_data["touch"].raw_value

    if touch_value > touch_data["threshold"] and not previously_touched[key]:
        if current_time - last_touched_time[key] > debounce_delay:
            last_touched_time[key] = current_time
            previously_touched[key] = True

            # Send a random keypress from the corresponding key group
            kbd.send(random.choice(touch_data["keys"]))
            # kbd.send(touch_data["keys"][0])

            # Light up the corresponding NeoPixel
            pixel_index = touch_data["pixel_index"]
            cp.pixels[pixel_index] = (
                0,
                255,
                0,
            )  # Set to green (you can adjust the color)

    elif touch_value <= touch_data["threshold"] and previously_touched[key]:
        # Turn off the NeoPixel when the touch is released
        pixel_index = touch_data["pixel_index"]
        cp.pixels[pixel_index] = (0, 0, 0)  # Turn off the pixel
        previously_touched[key] = False


while True:
    if cp.switch:
        for key, touch_data in touch_inputs.items():
            # print(f"{key}: {touch_data['touch'].raw_value}")oornliik
            debounce_and_press_logic(key, touch_data)

    time.sleep(0.1)
