from PIL import ImageGrab
import pygetwindow as gw
import pytesseract
import pyautogui
import random
import time
import re

from criterias import CRITERIAS

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def start_scan(window_size, x=1295, y=760):
	# convert start position and inventory dimension with game window resolution
	x = 1920 * x / window_size.width
	y = 1080 * y / window_size.height
	inventory_slot_width = 55 * 1920 // window_size.width
	inventory_slot_height = 80 * 1080 // window_size.height

	# move to first inventory slot postion
	pyautogui.moveTo(x, y, 0.5)
	time.sleep(0.2)

	# loop through each inventory slot
	for row in range(3):
		for col in range(11):
			# create a random time lag to create different between each loop action
			time_lag = random.randint(0, 9) / 100

			# sometime the game cannot dedect mouse movement
			# need to pick up each item to make sure tooltip will showup
			pyautogui.leftClick()
			time.sleep(0.3 + time_lag)
			pyautogui.leftClick()
			time.sleep(0.2 + time_lag)

			# scan item attributes
			item_data = scan_item_attr(window_size, col, x)
			item_data = clean_data(item_data)
			time.sleep(0.2 + time_lag)

			if not check_criteria(CRITERIAS, item_data):
				# mark item as junk
				pyautogui.press("space")
				time.sleep(0.2 + time_lag)

			# move mouse horizontally until it reach last slot on the row
			if col < 10:
				pyautogui.moveRel(inventory_slot_width, 0, 0.2 + time_lag)
				time.sleep(0.2)
				x += inventory_slot_width

		# move mouse to first item on next row
		x -= inventory_slot_width * 10
		y += inventory_slot_height
		pyautogui.moveTo(x, y, 0.5)
		time.sleep(0.2)


def scan_item_attr(window_size, col, x):
	# init window size and tooltip size and direction
	left_tooltip_start = 430 * 1920 // window_size.width * -1
	right_tooltip_start = 40 * 1920 // window_size.width

	tooltip_offset = right_tooltip_start if 2 <= col <= 3 else left_tooltip_start
	tooltop_width = 390 * 1920 // window_size.width

	# define tooltip area
	top = 0
	bottom = window_size.height
	left = x + tooltip_offset
	right = left + tooltop_width

	# scan tooltips
	window_content = ImageGrab.grab(bbox=(left, top, right, bottom))
	extracted_text = pytesseract.image_to_string(window_content)

	return extracted_text

def clean_data(input_data):
	# Use regex to find all non-letter, non-number, and non-space characters
	non_letter_number_space_pattern = r'[^a-zA-Z0-9./+-:\[\]%() ]+'
	# Replace all non-letter, non-number, and non-space characters with a space
	cleaned_string = re.sub(non_letter_number_space_pattern, ' ', input_data)
	
	# Use regex to replace multiple consecutive spaces and newlines with a single space
	# The regex pattern '[\s\n]+' matches one or more consecutive whitespace characters (including spaces and newlines)
	cleaned_string = re.sub(r'[\s\n]+', ' ', cleaned_string)
	
	return cleaned_string

def check_criteria(criteria, item_data, player_class="Rogue", match_needed=3):
	class_criteria = criteria[player_class]

	# if it is legendary or unique, skip
	if "Legendary" in item_data or "Unique" in item_data:
		return True

	# find out the gear type
	for gear_type in class_criteria:
		if gear_type in item_data:
			
			for attr in class_criteria[gear_type]:
				if attr in item_data:
					match_needed -= 1
				if match_needed == 0:
					return True
			
			# return after found and checked one gear_type
			return False
	
	# if it is not a gear, skip
	return True
