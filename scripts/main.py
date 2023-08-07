import pyautogui

from items_scaner import start_scan

if __name__ == "__main__":
    time.sleep(3)
    window_size = pyautogui.size()
    start_scan(window_size)
    
    