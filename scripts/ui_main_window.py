import pyautogui
import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets
import threading

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # init main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Connect the close event to a custom function
        MainWindow.closeEvent = self.on_close_event

        # init class variables
        self.init_var()

        # add widgets
        self.add_group_inventory()
        self.add_btn_start_scan()
        self.add_btn_abort_scan()

        # add central widget, menubar and status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    # function to init class variables
    def init_var(self):
        self.scanning_inventory = False

    # all functions for widgets

    # group_inventory
    # container
    def add_group_inventory(self):
        self.group_inventory = QtWidgets.QGroupBox(self.centralwidget)
        self.group_inventory.setGeometry(QtCore.QRect(10, 370, 390, 180))
        self.group_inventory.setObjectName("group_inventory")

        # rows
        self.verticalLayoutWidget = QtWidgets.QWidget(self.group_inventory)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 390, 170))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_inventory = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_inventory.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_inventory.setSpacing(5)
        self.verticalLayout_inventory.setObjectName("verticalLayout_inventory")

        # colums
        self.horizontalLayout_inventory_row_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_inventory_row_1.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_inventory_row_1.setObjectName("horizontalLayout_inventory_row_1")
        self.horizontalLayout_inventory_row_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_inventory_row_2.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_inventory_row_2.setObjectName("horizontalLayout_inventory_row_2")
        self.horizontalLayout_inventory_row_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_inventory_row_3.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_inventory_row_3.setObjectName("horizontalLayout_inventory_row_3")

        # array to hold button objects
        self.inventory_btns = [[None] * 11 for _ in range(3)]
        for row in range(3):
            if row == 0:
                curr_row = self.horizontalLayout_inventory_row_1
            elif row == 1:
                curr_row = self.horizontalLayout_inventory_row_2
            else:
                curr_row = self.horizontalLayout_inventory_row_3
            for col in range(11):
                self.inventory_btns[row][col] = QtWidgets.QPushButton(self.verticalLayoutWidget)
                curr_btn = self.inventory_btns[row][col]
                # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                # sizePolicy.setHorizontalStretch(0)
                # sizePolicy.setVerticalStretch(0)
                # sizePolicy.setHeightForWidth(curr_btn.sizePolicy().hasHeightForWidth())
                # curr_btn.setSizePolicy(sizePolicy)
                curr_btn.setMaximumSize(QtCore.QSize(30, 50))
                # curr_btn.setCheckable(True)
                # curr_btn.setChecked(False)
                curr_btn.setObjectName("btn_inventory_" + str(row * 11 + col + 1).zfill(2))
                curr_row.addWidget(curr_btn)
            self.verticalLayout_inventory.addLayout(curr_row)

    # btn_start_scan
    def add_btn_start_scan(self):
        self.btn_start_scan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start_scan.setGeometry(QtCore.QRect(430, 510, 150, 40))
        self.btn_start_scan.setObjectName("btn_start_scan")
        self.btn_start_scan.clicked.connect(self.on_click_btn_start_scan)

    def on_click_btn_start_scan(self):
        self.scanning_inventory = True

        # Start the scanning process in a separate thread
        scan_thread = threading.Thread(target=self.start_scan_thread)
        scan_thread.start()

    def start_scan_thread(self):
        window_size = pyautogui.size()
        start_scan(window_size, inventory_slot_to_check, self)

    # btn_abort_scan
    def add_btn_abort_scan(self):
        self.btn_abort_scan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_abort_scan.setGeometry(QtCore.QRect(630, 510, 150, 40))
        self.btn_abort_scan.setObjectName("btn_abort_scan")
        self.btn_abort_scan.clicked.connect(self.on_click_btn_abort_scan)
        # self.shortcut_abort_scan = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_A), self.centralwidget)
        # self.shortcut_abort_scan.activated.connect(self.on_click_btn_abort_scan)

        # Register the Ctrl+A hotkey
        keyboard.add_hotkey("ctrl+a", self.on_click_btn_abort_scan)

    def on_click_btn_abort_scan(self):
        print(self.scanning_inventory)
        self.scanning_inventory = False
        print(self.scanning_inventory)

    # Unhook all hotkeys before closing the window
    def on_close_event(self, event):
        keyboard.unhook_all()
        event.accept()
    
    # retranslateUi
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.group_inventory.setTitle(_translate("MainWindow", "Inventory Slots"))
        for row in range(3):
            for col in range(11):
                curr_num = str(row * 11 + col + 1).zfill(2)
                self.inventory_btns[row][col].setText(_translate("MainWindow", curr_num))
        self.btn_start_scan.setText(_translate("MainWindow", "Start"))
        self.btn_abort_scan.setText(_translate("MainWindow", "Abort Ctrl+A"))

def open_ui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
