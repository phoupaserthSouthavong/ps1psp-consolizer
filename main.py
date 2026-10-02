from machine import Pin
import time

from ps1controller_library import (
    PS2X,
    PSB_SELECT,
    PSB_START,
    PSB_PAD_UP,
    PSB_PAD_DOWN,
    PSB_PAD_LEFT,
    PSB_PAD_RIGHT,
    PSB_L1,
    PSB_R1,
    PSB_TRIANGLE,
    PSB_CIRCLE,
    PSB_CROSS,
    PSB_SQUARE,
)

# =========================================================
# PS2 CONTROLLER
# =========================================================

PS2_DAT = 0
PS2_CMD = 1
PS2_ATT = 2
PS2_CLK = 3

ps2 = PS2X(
    clk=PS2_CLK,
    cmd=PS2_CMD,
    att=PS2_ATT,
    dat=PS2_DAT
)


# =========================================================
# PSP BUTTON GPIO
# =========================================================
#
# PSP button lines are active LOW.
#
# Released = High-Z / INPUT
# Pressed  = OUTPUT LOW
#
# =========================================================

PSP_UP       = 15
PSP_DOWN     = 13
PSP_LEFT     = 14
PSP_RIGHT    = 16

PSP_L1       = 17
PSP_R1       = 7

PSP_CROSS    = 4
PSP_CIRCLE   = 5
PSP_TRIANGLE = 6
PSP_SQUARE   = 8

PSP_START    = 9
PSP_SELECT   = 10

PSP_DISPLAY  = 11
PSP_HOME     = 12


# =========================================================
# PSP PIN OBJECTS
# =========================================================

psp_pins = {
    "UP":       Pin(PSP_UP, Pin.IN),
    "DOWN":     Pin(PSP_DOWN, Pin.IN),
    "LEFT":     Pin(PSP_LEFT, Pin.IN),
    "RIGHT":    Pin(PSP_RIGHT, Pin.IN),

    "L1":       Pin(PSP_L1, Pin.IN),
    "R1":       Pin(PSP_R1, Pin.IN),

    "CROSS":    Pin(PSP_CROSS, Pin.IN),
    "CIRCLE":   Pin(PSP_CIRCLE, Pin.IN),
    "TRIANGLE": Pin(PSP_TRIANGLE, Pin.IN),
    "SQUARE":   Pin(PSP_SQUARE, Pin.IN),

    "START":    Pin(PSP_START, Pin.IN),
    "SELECT":   Pin(PSP_SELECT, Pin.IN),

    "DISPLAY":  Pin(PSP_DISPLAY, Pin.IN),
    "HOME":     Pin(PSP_HOME, Pin.IN),
}


# =========================================================
# PRESS / RELEASE
# =========================================================

def press_pin(name):
    """
    กดปุ่ม PSP
    GPIO -> OUTPUT LOW
    """
    pin = psp_pins[name]
    pin.init(Pin.OUT)
    pin.value(0)


def release_pin(name):
    """
    ปล่อยปุ่ม PSP
    GPIO -> High-Z
    """
    pin = psp_pins[name]
    pin.init(Pin.IN)


# =========================================================
# RELEASE ALL PSP BUTTONS
# =========================================================

def release_all():
    for name in psp_pins:
        release_pin(name)


# =========================================================
# MAIN BUTTON MAPPING
# =========================================================

BUTTON_MAP = {
    "UP":       (PSB_PAD_UP, PSP_UP),
    "DOWN":     (PSB_PAD_DOWN, PSP_DOWN),
    "LEFT":     (PSB_PAD_LEFT, PSP_LEFT),
    "RIGHT":    (PSB_PAD_RIGHT, PSP_RIGHT),

    "L1":       (PSB_L1, PSP_L1),
    "R1":       (PSB_R1, PSP_R1),

    "CROSS":    (PSB_CROSS, PSP_CROSS),
    "CIRCLE":   (PSB_CIRCLE, PSP_CIRCLE),
    "TRIANGLE": (PSB_TRIANGLE, PSP_TRIANGLE),
    "SQUARE":   (PSB_SQUARE, PSP_SQUARE),

    "START":    (PSB_START, PSP_START),
    "SELECT":   (PSB_SELECT, PSP_SELECT),
}


# =========================================================
# UPDATE PSP BUTTONS
# =========================================================

def update_buttons():

    for name, (ps2_button, psp_pin) in BUTTON_MAP.items():

        if ps2.button(ps2_button):
            press_pin(name)
        else:
            release_pin(name)


# =========================================================
# DEBUG
# =========================================================

last_buttons = 0


def debug_buttons():

    global last_buttons

    current = ps2.buttons

    if current != last_buttons:

        print("PS2 buttons: {:04X}".format(current))

        for name, (mask, _) in BUTTON_MAP.items():

            if current & mask:
                print("  PRESS:", name)

        last_buttons = current


# =========================================================
# CONNECT PS2 CONTROLLER
# =========================================================

print()
print("==============================")
print(" PS2 -> PSP CONTROLLER")
print("==============================")
print()

release_all()

print("Connecting PS2 controller...")

while True:

    result = ps2.config_gamepad(
        pressures=False,
        rumble=False,
        analog_mode=False,
        lock_analog=False
    )

    if result == 0:
        print("PS2 controller connected!")
        break

    print("PS2 controller not found...")
    time.sleep_ms(500)


# =========================================================
# MAIN LOOP
# =========================================================

print("Mapping started.")
print()

while True:

    ps2.read_gamepad()

    update_buttons()

    debug_buttons()

    time.sleep_ms(2)