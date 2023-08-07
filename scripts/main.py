import pyautogui
from items_scaner import start_scan

inventory_slot_to_check = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
]

if __name__ == "__main__":
    window_size = pyautogui.size()
    start_scan(window_size, inventory_slot_to_check)
    
    