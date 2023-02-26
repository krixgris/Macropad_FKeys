from adafruit_macropad import MacroPad

import displayio
import rainbowio
import os
import time

FKEY_OFFSET = 0x3A
MACROPAD_SLEEP_KEYS = 60
MACROPAD_BRIGHTNESS = 0.2

macropad = MacroPad(rotation=90)
macropad.pixels.brightness = MACROPAD_BRIGHTNESS

macropad_sleep_keys = False
screensaving = False
screensaver_group = displayio.Group()

loop_start_time = 0
loop_last_action = time.monotonic()

text_lines = macropad.display_text(title="Keypad", title_scale=1, text_scale=2)
text_lines.show()

for key in range(4):
	macropad.pixels[key] = (0, 0, 20+key*2)
for key in range(4,8):
	macropad.pixels[key] = (0, 20+key*2, 0)
for key in range(8,12):
	macropad.pixels[key] = (20+key*2, 0, 0)

last_position = 0
print("Ready")
while True:
	loop_start_time = time.monotonic()
	if key_event := macropad.keys.events.get():
		if key_event.pressed:
			loop_last_action = time.monotonic()
			key = key_event.key_number
			text_lines[1].text = f"F{key+1}"
			macropad.keyboard.send(key+FKEY_OFFSET)
			macropad.keyboard.release_all()
		if key_event.released:
			text_lines[1].text = ""

	macropad.encoder_switch_debounced.update()

	if macropad.encoder_switch_debounced.pressed:
		loop_last_action = time.monotonic()
		macropad.mouse.click(macropad.Mouse.RIGHT_BUTTON)
		text_lines[1].text = "RMB"
	if macropad.encoder_switch_debounced.released:
		loop_last_action = time.monotonic()
		text_lines[1].text = ""

	current_position = macropad.encoder

	if macropad.encoder > last_position:
		loop_last_action = time.monotonic()
		macropad.mouse.move(x=+5)
		last_position = current_position

	if macropad.encoder < last_position:
		loop_last_action = time.monotonic()
		macropad.mouse.move(x=-5)
		last_position = current_position

	# screen saver
	if(not screensaving and loop_start_time-loop_last_action>MACROPAD_SLEEP_KEYS):
		screensaving = True
		macropad.pixels.brightness = 0
		macropad_sleep_keys = True
		macropad.display.refresh()
		macropad.display.show(screensaver_group)

	elif(screensaving and macropad_sleep_keys and loop_start_time-loop_last_action<MACROPAD_SLEEP_KEYS):
		screensaving = False
		macropad.pixels.brightness = MACROPAD_BRIGHTNESS
		macropad_sleep_keys = False
		macropad.display.refresh()
		text_lines.show()
