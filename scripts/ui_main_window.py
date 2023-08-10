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

        # add central widget, menubar and status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.add_menu_bar(MainWindow)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        # add widgets
        self.add_group_inventory()
        self.add_btn_start_scan()
        self.add_btn_abort_scan()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    # function to init class variables
    def init_var(self):
        self.scanning_inventory = False
        self.inventory_slot_to_check = inventory_slot_to_check[:]

    # all functions for widgets

    # menu
    def add_menu_bar(self, MainWindow):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menu_action_new = QtWidgets.QAction(MainWindow)
        self.menu_action_new.setObjectName("menu_action_new")
        self.menu_action_save = QtWidgets.QAction(MainWindow)
        self.menu_action_save.setObjectName("menu_action_save")
        self.menu_action_load = QtWidgets.QAction(MainWindow)
        self.menu_action_load.setObjectName("menu_action_load")
        self.menu_action_exit = QtWidgets.QAction(MainWindow)
        self.menu_action_exit.setObjectName("menu_action_exit")

        self.menuFile.addAction(self.menu_action_new)
        self.menuFile.addAction(self.menu_action_save)
        self.menuFile.addAction(self.menu_action_load)
        self.menuFile.addAction(self.menu_action_exit)

        self.menubar.addAction(self.menuFile.menuAction())

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
                curr_btn.setMaximumSize(QtCore.QSize(30, 50))
                curr_btn.setObjectName("btn_inventory_" + str(row * 11 + col + 1).zfill(2))
                if self.inventory_slot_to_check[row][col]:
                    curr_btn.setStyleSheet("background-color: green")
                else:
                    curr_btn.setStyleSheet("background-color: red")
                curr_btn.clicked.connect(self.on_click_btn_inventory)
                curr_row.addWidget(curr_btn)
            self.verticalLayout_inventory.addLayout(curr_row)

    def on_click_btn_inventory(self):
        curr_btn = self.centralwidget.sender()
        if curr_btn:
            inventory_num = int(curr_btn.text())
            row = (inventory_num - 1) // 11
            col = (inventory_num - 1) % 11
            if self.inventory_slot_to_check[row][col]:
                self.inventory_slot_to_check[row][col] = 0
                curr_btn.setStyleSheet("background-color: red")
            else:
                self.inventory_slot_to_check[row][col] = 1
                curr_btn.setStyleSheet("background-color: green")

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
        start_scan(window_size, self.inventory_slot_to_check, self)

    # btn_abort_scan
    def add_btn_abort_scan(self):
        self.btn_abort_scan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_abort_scan.setGeometry(QtCore.QRect(630, 510, 150, 40))
        self.btn_abort_scan.setObjectName("btn_abort_scan")
        self.btn_abort_scan.clicked.connect(self.on_click_btn_abort_scan)
        # self.shortcut_abort_scan = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_A), self.centralwidget)
        # self.shortcut_abort_scan.activated.connect(self.on_click_btn_abort_scan)

        # Register the Ctrl+A hotkey
        keyboard.add_hotkey("ctrl+x", self.on_click_btn_abort_scan)

    def on_click_btn_abort_scan(self):
        self.scanning_inventory = False

    # Unhook all hotkeys before closing the window
    def on_close_event(self, event):
        keyboard.unhook_all()
        event.accept()
    
    # retranslateUi
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # menu items
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menu_action_new.setText(_translate("MainWindow", "New"))
        self.menu_action_new.setStatusTip(_translate("MainWindow", "Create new file"))
        self.menu_action_new.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.menu_action_save.setText(_translate("MainWindow", "Save"))
        self.menu_action_save.setStatusTip(_translate("MainWindow", "Save file"))
        self.menu_action_save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.menu_action_load.setText(_translate("MainWindow", "Load"))
        self.menu_action_load.setStatusTip(_translate("MainWindow", "Load file"))
        self.menu_action_load.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.menu_action_exit.setText(_translate("MainWindow", "Exit"))
        self.menu_action_exit.setStatusTip(_translate("MainWindow", "Exit Progarm"))
        self.menu_action_exit.setShortcut(_translate("MainWindow", "Ctrl+E"))

        # inventory
        self.group_inventory.setTitle(_translate("MainWindow", "Inventory Slots"))
        for row in range(3):
            for col in range(11):
                curr_num = str(row * 11 + col + 1).zfill(2)
                self.inventory_btns[row][col].setText(_translate("MainWindow", curr_num))

        # start / abort btn
        self.btn_start_scan.setText(_translate("MainWindow", "Start"))
        self.btn_abort_scan.setText(_translate("MainWindow", "Abort Ctrl+x"))

def open_ui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
