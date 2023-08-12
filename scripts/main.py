import pyautogui
from items_scaner import start_scan
from ui_main_window import open_ui

if __name__ == "__main__":
    window_size = pyautogui.size()
    open_ui()
    # start_scan(window_size, inventory_slot_to_check)
    
    