import pyautogui
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

        # init class variables
        self.init_var()

        # add widgets
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

    # function for widgets
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
        self.shortcut_abort_scan = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_A), self.centralwidget)
        self.shortcut_abort_scan.activated.connect(self.on_click_btn_abort_scan)

    def on_click_btn_abort_scan(self):
        print(self.scanning_inventory)
        self.scanning_inventory = False
        print(self.scanning_inventory)
    
    # retranslateUi
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
