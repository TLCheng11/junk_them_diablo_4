from PIL import ImageGrab
import pygetwindow as gw
import pytesseract
import pyautogui
import random
import time
import re

from base_criterias import ALL_GEAR_TYPES, WEAPONS_LIST

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def start_scan(window_size, inventory_slot_to_check, criterias, ui, x=1295, y=760):
    # convert start position and inventory dimension with game window resolution
    x = 1920 * x // window_size.width
    y = 1080 * y // window_size.height
    inventory_slot_width = 55 * 1920 // window_size.width
    inventory_slot_height = 80 * 1080 // window_size.height

    # move to first inventory slot postion
    pyautogui.moveTo(x, y, 0.5)
    time.sleep(0.2)

    remaining_slot = 0
    for inventory_row in inventory_slot_to_check:
        remaining_slot += sum(inventory_row)

    # loop through each inventory slot
    for row in range(3):
        for col in range(11):
            if remaining_slot == 0:
                print("Done Scanning")
                return

            if not ui.scanning_inventory:
                print("Abort Scanning!")
                return

            if not check_inventory_open(window_size):
                print("Cannot find inventory!")
                print("Abort Scanning!")
                return

            print("===" * 10)
            print("inventory slot, row: ",row + 1," column:",col + 1)

            if inventory_slot_to_check[row][col]:
                remaining_slot -= 1
                # create a random time lag to create different between each loop action
                time_lag = random.randint(0, 9) / 100

                # sometime the game cannot dedect mouse movement by pyautogui
                # need to pick up each item to make sure tooltip will showup
                pyautogui.leftClick()
                time.sleep(0.01 + time_lag)
                pyautogui.leftClick()
                time.sleep(0.01 + time_lag)

                # scan item attributes
                item_data = scan_item_attr(window_size, col, x)
                item_data = clean_data(item_data)
                time.sleep(0.01 + time_lag)

                if not check_criterias(criterias, item_data):
                    # mark item as junk
                    time.sleep(0.01 + time_lag)
                    pyautogui.press("space")

            else:
                print("passed")

            # move mouse horizontally until it reach last slot on the row
            if col < 10:
                # pyautogui.moveRel(inventory_slot_width, 0, 0.1 + time_lag)
                x += inventory_slot_width
                pyautogui.moveTo(x, y, 0.1 + time_lag)
                time.sleep(0.01)

        # move mouse to first item on next row
        x -= inventory_slot_width * 10
        y += inventory_slot_height
        pyautogui.moveTo(x, y, 0.5)
        time.sleep(0.01)
    
    print("Done Scanning")
    ui.scanning_inventory = False

def scan_item_attr(window_size, col, x):
    # init window size and tooltip size and direction
    left_tooltip_start = 425 * 1920 // window_size.width * -1
    right_tooltip_start = 45 * 1920 // window_size.width

    tooltip_offset = right_tooltip_start if 2 <= col <= 3 else left_tooltip_start
    tooltop_width = 385 * 1920 // window_size.width

    # define tooltip area
    top = 0
    bottom = window_size.height
    left = x + tooltip_offset
    right = left + tooltop_width

    # scan tooltips
    return ocr_image(left, top, right, bottom)

def check_inventory_open(window_size):
    left = 1920 * 1300 // window_size.width
    right = 1920 * (1300 + 210) // window_size.width
    top = 1080 * 12 // window_size.height
    bottom = 1080 * (12 + 31) // window_size.height

    text = ocr_image(left, top, right, bottom)

    return "CHARACTER" in text

def ocr_image(left, top, right, bottom):
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

def check_criterias(criterias, item_data, player_class="Rogue"):
    # if already marked as junk, skip
    if check_marked_as_junk(item_data):
        return True

    # if it is legendary or unique, skip
    if "Legendary" in item_data or "Unique" in item_data:
        return True

    # if item is upgraded, skip
    if "Upgrades" in item_data:
        return True

    print(item_data)

    # check the gear type
    (gear_type, cutoff_index) = check_gear_type(item_data)
    if gear_type == "":
        return True

    # further trim the data to avoid weapon inherited attr
    trimmed_item_data = item_data[cutoff_index:]
    matches_needed = criterias[gear_type]["Matches Needed"]

    if matches_needed > 4:
        return False

    # if nothing need to be matched, keep item
    if not matches_needed or not len(criterias[gear_type]["Attributes Needed"]):
        return True

    # start comparing
    for attr in criterias[gear_type]["Attributes Needed"]:

        # convert [X]% in gloves and ring and weapon into regex
        if "[X]%" in attr:
            idx = attr.index("[X]%")
            prefix = attr[:idx]
            suffix = attr[idx + 4:]
            print(prefix + suffix)
            pattern = re.compile(rf'{prefix}[+]*([\d.]+)[%]*{suffix}(?! [a-zA-Z])')
        else:
            pattern = re.compile(rf'([\d.]+)[%\s]*{attr}(?! [a-zA-Z])')

        match = re.search(pattern, trimmed_item_data)
        if match and float(match.group(1)) >= criterias[gear_type]["Attributes Needed"][attr]:
            matches_needed -= 1
            print("+" + match.group(1), attr, " | matches needed:", matches_needed)
        if matches_needed == 0:
            return True

    print("===" * 10)
    return False

def check_marked_as_junk(item_data):
    pattern = re.compile(r'un\s*mark\s*as', re.IGNORECASE)
    return bool(pattern.search(item_data))

def check_gear_type(item_data):
    for gear_type in ALL_GEAR_TYPES:
        if gear_type in item_data:

            # if gear is a weapon
            try:
                if gear_type in WEAPONS_LIST:
                    # find the data index after the inherited attr
                    (weapon_inherited_attr, weapon_type) = WEAPONS_LIST[gear_type]
                    pattern = rf'([\d.]+)[%\s]*({weapon_inherited_attr})'
                    match = re.search(pattern, item_data)
                    # print(weapon_inherited_attr)
                    # print(match.group(1))
                    # print(match.group(2))
                    last_index = match.end(2)
                    print(item_data[last_index:])
                    return (weapon_type, last_index)
                else:
                    # if it is not a weapon, find the data index after the gear word
                    pattern = rf'({gear_type})'
                    match = re.search(pattern, item_data)
                    last_index = match.end()
                    return (gear_type, last_index)
            except:
                print("gear check failed")
                return ("", -1)

    # if not a gear
    return ("", -1)
