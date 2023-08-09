import pyautogui
from items_scaner import start_scan
from ui_main_window import open_ui

# inventory_slot_to_check = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
# ]
# for testing
# inventory_slot_to_check = [
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

if __name__ == "__main__":
    window_size = pyautogui.size()
    open_ui()
    # start_scan(window_size, inventory_slot_to_check)
    
    