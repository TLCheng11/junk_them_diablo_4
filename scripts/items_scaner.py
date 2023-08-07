from PIL import ImageGrab
import pygetwindow as gw
import pytesseract
import pyautogui
import random
import time

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
            item_data = item_data.replace("\n", " ")
            print(item_data)
            if "Critical Strike Chance" in item_data:
                print("x" * 10)
            print("=" * 30)
            time.sleep(0.2 + time_lag)

            # mark item as junk (testing feature)
            # pyautogui.press("space")
            # time.sleep(0.2 + time_lag)

            # move mouse horizontally untill it reach last slot on the row
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