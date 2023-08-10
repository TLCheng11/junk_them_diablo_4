from PyQt5 import QtCore, QtGui, QtWidgets
import pyautogui
import keyboard
import threading

from item_attr_list import ITEM_ATTR_LIST
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
        self.add_groupBox_items()
        self.add_groupBox_classes()
        self.add_groupBox_inventory()
        self.add_groupBox_attributes()
        self.add_btn_start_scan()
        self.add_btn_abort_scan()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    # function to init class variables
    def init_var(self):
        # for abort operation
        self.scanning_inventory = False

        # for groupBox_items
        self.items_names = [
            ["Helm", "Chest", "Gloves", "Pants", "Boots"],
            ["Amulet", "Ring", "1-Hand", "2-Hand", "Off-H"],
        ]
        self.curr_item = ("", -1, -1)

        # for groupBox_classes
        self.classes_names = ["All", "Barb", "Druid", "Necro", "Rogue", "Sorc"]
        self.curr_class = ("All", 0)

        # for groupBox_attributes
        self.curr_item_full_text = {
            "": "Please select an item above",
            "Helm": "Helm",
            "Chest": "Chest",
            "Gloves": "Gloves",
            "Pants": "Pants",
            "Boots": "Boots",
            "Amulet": "Amulet",
            "Ring": "Ring",
            "1-Hand": "One-Handed Weapon",
            "2-Hand": "Two-Handed Weapon",
            "Off-H": "Off Hand",
        }

        self.curr_class_full_text = {
            "All": "All Classes",
            "Barb": "Barbarian",
            "Druid": "Druid",
            "Necro": "Necromancer",
            "Rogue": "Rogue",
            "Sorc": "Sorcerer",
        }

        # for groupBox_inventory
        self.inventory_slot_to_check = inventory_slot_to_check[:]

    # ----- all functions for widgets -----
    # - menu -
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

    # - groupBox_items -
    def add_groupBox_items(self):
        self.groupBox_items = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_items.setGeometry(QtCore.QRect(10, 10, 390, 140))
        self.groupBox_items.setObjectName("groupBox_items")

        self.verticalLayoutWidget_items = QtWidgets.QWidget(self.groupBox_items)
        self.verticalLayoutWidget_items.setGeometry(QtCore.QRect(10, 15, 370, 120))
        self.verticalLayoutWidget_items.setObjectName("verticalLayoutWidget_items")
        self.verticalLayout_items = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_items)
        self.verticalLayout_items.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_items.setObjectName("verticalLayout_items")

        # array to hold button objects
        self.items_btns = [[None] * 5 for _ in range(2)]

        for row in range(2):
            # create horizontal layout for each row
            curr_row = QtWidgets.QHBoxLayout()
            curr_row.setObjectName("horizontalLayout_items_row_" + str(row + 1))

            for col in range(5):
                self.items_btns[row][col] = QtWidgets.QPushButton(self.verticalLayoutWidget_items)
                curr_btn = self.items_btns[row][col]
                curr_btn.setMaximumSize(QtCore.QSize(50, 50))
                curr_btn.setObjectName("btn_items_" + self.items_names[row][col].replace("-", "_"))
                if self.items_names[row][col] == self.curr_item[0]:
                    curr_btn.setStyleSheet("border: 2px solid yellow")
                curr_btn.clicked.connect(self.on_click_btn_items)
                curr_row.addWidget(curr_btn)
            self.verticalLayout_items.addLayout(curr_row)

    def on_click_btn_items(self):
        curr_btn = self.centralwidget.sender()
        if curr_btn:
            item_name = curr_btn.text()

            # if the btn was selected before, change its color to deflaut, clear curr_item
            if item_name == self.curr_item[0]:
                curr_btn.setStyleSheet("")
                self.curr_item = ("", -1, -1)
            else:
                # find the row and col index of the btn
                idx = (self.items_names[0] + self.items_names[1]).index(item_name)
                row = idx // 5
                col = idx % 5

                # if other items was selected before, reset color of previous btn to deflaut
                if self.curr_item[0]:
                    last_item_btn = self.items_btns[self.curr_item[1]][self.curr_item[2]]
                    last_item_btn.setStyleSheet("")
                
                # set curr_item to the item of the btn and change btn color to green
                curr_btn.setStyleSheet("border: 2px solid yellow")
                self.curr_item = (item_name, row, col)

            self.update_label_text(self.label_curr_item, self.curr_item_full_text[self.curr_item[0]])
            self.update_comboBox_items(self.comboBox_attributes)

    # - groupBox_classes -
    def add_groupBox_classes(self):
        self.groupBox_classes = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_classes.setGeometry(QtCore.QRect(10, 160, 390, 80))
        self.groupBox_classes.setObjectName("groupBox_classes")

        self.horizontalLayoutWidget_classes = QtWidgets.QWidget(self.groupBox_classes)
        self.horizontalLayoutWidget_classes.setGeometry(QtCore.QRect(10, 15, 370, 60))
        self.horizontalLayoutWidget_classes.setObjectName("horizontalLayoutWidget_classes")
        self.horizontalLayout_classes = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_classes)
        self.horizontalLayout_classes.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_classes.setObjectName("horizontalLayout_classes")

        # array to hold button objects
        self.classes_btns = [None] * len(self.classes_names)

        for col in range(len(self.classes_names)):
            self.classes_btns[col] = QtWidgets.QPushButton(self.horizontalLayoutWidget_classes)
            curr_btn = self.classes_btns[col]
            curr_btn.setMaximumSize(QtCore.QSize(50, 50))
            curr_btn.setObjectName("btn_classes_" + self.classes_names[col])
            if self.classes_names[col] == self.curr_class[0]:
                curr_btn.setStyleSheet("border: 2px solid yellow")
            curr_btn.clicked.connect(self.on_click_btn_classes)
            self.horizontalLayout_classes.addWidget(curr_btn)

    def on_click_btn_classes(self):
        curr_btn = self.centralwidget.sender()
        if curr_btn:
            class_name = curr_btn.text()

            # if the btn was selected before, change its color to deflaut, clear curr_item
            if class_name == self.curr_class[0]:
                # don't need to do anything if all is selected again
                if class_name == "All":
                    return
                curr_btn.setStyleSheet("")

                # set selected item to All as default
                self.classes_btns[0].setStyleSheet("border: 2px solid yellow")
                self.curr_class = ("All", 0)
            else:
                # find the index of the btn
                idx = self.classes_names.index(class_name)

                # if other items was selected before, reset color of previous btn to deflaut
                last_class_btn = self.classes_btns[self.curr_class[1]]
                last_class_btn.setStyleSheet("")
                
                # set curr_class to the item of the btn and change btn color to green
                curr_btn.setStyleSheet("border: 2px solid yellow")
                self.curr_class = (class_name, idx)
            
            self.update_label_text(self.label_curr_class, self.curr_class_full_text[self.curr_class[0]])
            self.update_comboBox_items(self.comboBox_attributes)

    # - groupBox_attributes -
    def add_groupBox_attributes(self):
        self.groupBox_attributes = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_attributes.setGeometry(QtCore.QRect(10, 270, 390, 80))
        self.groupBox_attributes.setObjectName("groupBox_attributes")

        self.label_curr_item = QtWidgets.QLabel(self.groupBox_attributes)
        self.label_curr_item.setGeometry(QtCore.QRect(10, 22, 150, 16))
        self.label_curr_item.setObjectName("label_curr_item")

        self.label_curr_class = QtWidgets.QLabel(self.groupBox_attributes)
        self.label_curr_class.setGeometry(QtCore.QRect(170, 22, 100, 16))
        self.label_curr_class.setObjectName("label_curr_class")

        self.btn_add_attr = QtWidgets.QPushButton(self.groupBox_attributes)
        self.btn_add_attr.setGeometry(QtCore.QRect(305, 20, 75, 20))
        self.btn_add_attr.setObjectName("btn_add_attr")

        self.comboBox_attributes = QtWidgets.QComboBox(self.groupBox_attributes)
        self.comboBox_attributes.setGeometry(QtCore.QRect(10, 45, 320, 21))
        self.comboBox_attributes.setObjectName("comboBox_attributes")

        self.doubleSpinBox_attributes = QtWidgets.QDoubleSpinBox(self.groupBox_attributes)
        self.doubleSpinBox_attributes.setGeometry(QtCore.QRect(340, 45, 40, 21))
        self.doubleSpinBox_attributes.setDecimals(1)
        self.doubleSpinBox_attributes.setSingleStep(0.1)
        self.doubleSpinBox_attributes.setMaximum(0)
        self.doubleSpinBox_attributes.setObjectName("doubleSpinBox_attributes")

    def update_label_text(self, label, text):
        _translate = QtCore.QCoreApplication.translate
        label.setText(_translate("MainWindow", text))

    def update_comboBox_items(self, comboBox):
        # clean up box 
        comboBox.clear()

        # only add attibutes to the box if an item is selected
        if self.curr_item[0]:
            item_name = self.curr_item_full_text[self.curr_item[0]]
            class_name = self.curr_class_full_text[self.curr_class[0]]
            for attr in ITEM_ATTR_LIST[item_name][class_name]:
                comboBox.addItem(attr)

    # - groupBox_inventory -
    def add_groupBox_inventory(self):
        self.groupBox_inventory = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_inventory.setGeometry(QtCore.QRect(10, 370, 390, 180))
        self.groupBox_inventory.setObjectName("groupBox_inventory")

        # rows
        self.verticalLayoutWidget_inventory = QtWidgets.QWidget(self.groupBox_inventory)
        self.verticalLayoutWidget_inventory.setGeometry(QtCore.QRect(0, 10, 390, 170))
        self.verticalLayoutWidget_inventory.setObjectName("verticalLayoutWidget_inventory")
        self.verticalLayout_inventory = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_inventory)
        self.verticalLayout_inventory.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_inventory.setSpacing(5)
        self.verticalLayout_inventory.setObjectName("verticalLayout_inventory")

        # array to hold button objects
        self.inventory_btns = [[None] * 11 for _ in range(3)]
        for row in range(3):
            # create horizontal layout for each row
            curr_row = QtWidgets.QHBoxLayout()
            curr_row.setContentsMargins(0, -1, 0, 0)
            curr_row.setSpacing(5)
            curr_row.setObjectName("horizontalLayout_inventory_row_" + str(row + 1))

            for col in range(11):
                self.inventory_btns[row][col] = QtWidgets.QPushButton(self.verticalLayoutWidget_inventory)
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

    # - start and abort btn -
    # btn_start_scan
    def add_btn_start_scan(self):
        self.btn_start_scan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start_scan.setGeometry(QtCore.QRect(430, 510, 150, 40))
        self.btn_start_scan.setObjectName("btn_start_scan")
        self.btn_start_scan.clicked.connect(self.on_click_btn_start_scan)

        # Register the Left Shift+X hotkey
        keyboard.add_hotkey("left shift + x", self.on_click_btn_start_scan)

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

        # Register the Ctrl+X hotkey
        keyboard.add_hotkey("ctrl + x", self.on_click_btn_abort_scan)

    def on_click_btn_abort_scan(self):
        self.scanning_inventory = False

    # - helper -
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

        # items
        self.groupBox_items.setTitle(_translate("MainWindow", "Items"))
        for row in range(len(self.items_btns)):
            for col in range(len(self.items_btns[row])):
                self.items_btns[row][col].setText(_translate("MainWindow", self.items_names[row][col]))

        # classes
        self.groupBox_classes.setTitle(_translate("MainWindow", "Classes"))
        for col in range(len(self.classes_btns)):
            self.classes_btns[col].setText(_translate("MainWindow", self.classes_names[col]))

        # attributes
        self.groupBox_attributes.setTitle(_translate("MainWindow", "Attributes"))
        self.label_curr_item.setText(_translate("MainWindow", self.curr_item_full_text[self.curr_item[0]]))
        self.label_curr_class.setText(_translate("MainWindow", self.curr_class_full_text[self.curr_class[0]]))
        self.btn_add_attr.setText(_translate("MainWindow", "Add Attr"))

        # inventory
        self.groupBox_inventory.setTitle(_translate("MainWindow", "Inventory Slots"))
        for row in range(3):
            for col in range(11):
                curr_num = str(row * 11 + col + 1).zfill(2)
                self.inventory_btns[row][col].setText(_translate("MainWindow", curr_num))

        # start / abort btn
        self.btn_start_scan.setText(_translate("MainWindow", "Start (Left Shift + X)"))
        self.btn_abort_scan.setText(_translate("MainWindow", "Abort (Ctrl + X)"))

def open_ui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
