import pyautogui
import time
import pygetwindow as gw
import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def start_scan(x=1295, y=760):
    cursor_speed = 0.5
    pyautogui.moveTo(x, y, 0.5)
    time.sleep(0.2)

    for row in range(3):
        for col in range(11):
            pyautogui.leftClick()
            time.sleep(0.3)
            pyautogui.leftClick()
            time.sleep(0.2)
            item_data = scan_item_attr(col, x)
            print(item_data)
            print("=" * 30)
            time.sleep(0.2)
            pyautogui.press("space")
            time.sleep(0.2)
            if col  < 10:
                pyautogui.moveRel(55, 0, 0.2)
                time.sleep(0.2)
                x += 55
        x -= 550
        y += 85
        pyautogui.moveTo(x, y, 0.5)
        time.sleep(0.2)


def scan_item_attr(col, x):
    # init window size and tooltip size and direction
    window_size = pyautogui.size()
    tooltip_offset = 40 if 2 <= col <= 3 else -430
    tooltop_width = 390

    # define tooltip area
    top = 0
    bottom = window_size.height
    left = x + tooltip_offset
    right = left + tooltop_width

    # scan tooltips
    window_content = ImageGrab.grab(bbox=(left, top, right, bottom))
    extracted_text = pytesseract.image_to_string(window_content)

    return extracted_text

if __name__ == "__main__":
    time.sleep(5)
    start_scan()
    
    