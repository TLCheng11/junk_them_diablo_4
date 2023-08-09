import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

from items_scaner import start_scan

inventory_slot_to_check = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
]
# for testing
# inventory_slot_to_check = [
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

class UIMainWindow(QMainWindow):
    def __init__(self):
        super(UIMainWindow, self).__init__()
        self.setGeometry(1970, 50, 400, 400)
        self.setWindowTitle("Junk Them!!!")
        self.init_ui()

    def init_ui(self):
        self.scan_button = QPushButton("start scan", self)
        self.scan_button.move(100, 100)
        self.scan_button.resize(200, 200)
        self.scan_button.clicked.connect(self.on_click_scan_button)

    # use to update components size
    def update(self, component):
        component.adjustSize()

    def on_button_click(self):
        self.label.setText("Hello, " + self.entry.text())
        self.update(self.label)

    def on_click_scan_button(self):
        window_size = pyautogui.size()
        start_scan(window_size, inventory_slot_to_check)

def open_ui():
    app = QApplication(sys.argv)
    window = UIMainWindow()
    window.show()

    sys.exit(app.exec_())
