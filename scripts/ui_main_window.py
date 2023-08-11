from PyQt5 import QtCore, QtGui, QtWidgets
import pyautogui
import keyboard
import threading
import json

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
        self.add_group_box_items()
        self.add_group_box_classes()
        self.add_group_box_inventory()
        self.add_group_box_attributes()
        self.add_group_box_criterias()
        self.add_btn_start_scan()
        self.add_btn_abort_scan()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    # function to init class variables
    def init_var(self):
        # for abort operation
        self.scanning_inventory = False

        # criterias for item scan
        self.criterias = {
            "Helm": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Chest": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Gloves": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Pants": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Boots": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Amulet": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Ring": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "One-Handed Weapon": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Two-Handed Weapon": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Off Hand": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
            "Shield": {
                "Matches Needed": 3,
                "Attributes Needed": {

                },
            },
        }

        # for group_box_items
        self.items_names = [
            ["Helm", "Chest", "Gloves", "Pants", "Boots"],
            ["Amulet", "Ring", "1-Hand", "2-Hand", "Off-H", "Shield"],
        ]
        self.curr_item = ("", -1, -1)

        # for group_box_classes
        self.classes_names = ["All", "Barb", "Druid", "Necro", "Rogue", "Sorc"]
        self.curr_class = ("All", 0)

        # for group_box_attributes
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
            "Shield": "Shield"
        }

        self.curr_class_full_text = {
            "All": "All Classes",
            "Barb": "Barbarian",
            "Druid": "Druid",
            "Necro": "Necromancer",
            "Rogue": "Rogue",
            "Sorc": "Sorcerer",
        }

        self.selected_attribute = ""
        self.selected_attribute_value = 0

        # for group_box_inventory
        self.inventory_slot_to_check = inventory_slot_to_check[:]

    # ----- all functions for widgets -----
    # - menu -
    def add_menu_bar(self, MainWindow):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        MainWindow.setMenuBar(self.menubar)

        self.menu_action_new = QtWidgets.QAction(MainWindow)
        self.menu_action_new.setObjectName("menu_action_new")
        self.menu_action_save = QtWidgets.QAction(MainWindow)
        self.menu_action_save.setObjectName("menu_action_save")
        self.menu_action_save.triggered.connect(self.save_data)
        self.menu_action_load = QtWidgets.QAction(MainWindow)
        self.menu_action_load.setObjectName("menu_action_load")
        self.menu_action_load.triggered.connect(self.load_data)
        self.menu_action_exit = QtWidgets.QAction(MainWindow)
        self.menu_action_exit.setObjectName("menu_action_exit")

        self.menu_file.addAction(self.menu_action_new)
        self.menu_file.addAction(self.menu_action_save)
        self.menu_file.addAction(self.menu_action_load)
        self.menu_file.addAction(self.menu_action_exit)

        self.menubar.addAction(self.menu_file.menuAction())

    def save_data(self):
        data = {
            "inventory_slot_to_check": self.inventory_slot_to_check,
            "criterias": self.criterias
        }

        default_path = "saved_criterias/"
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, "Save File", default_path, "JSON Files (*.json)")
        if filename:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

    def load_data(self):
        default_path = "saved_criterias/"
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Load File", default_path, "JSON Files (*.json)")
        if filename:
            with open(filename, "r") as f:
                data = json.load(f)
                temp_inventory = data.get("inventory_slot_to_check")
                temp_criterias = data.get("criterias")



                try:
                    self.reset_group_box_inventory(temp_inventory)
                    self.inventory_slot_to_check = data.get("inventory_slot_to_check")
                    print("Data loaded from file:")
                except Exception as e:
                    self.reset_group_box_inventory(self.inventory_slot_to_check)
                    print(e)
                    error_message = "An error occurred while loading the file!"
                    QtWidgets.QMessageBox.critical(self.centralwidget, "Error", error_message)

    # - group_box_items -
    def add_group_box_items(self):
        self.group_box_items = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_items.setGeometry(QtCore.QRect(10, 10, 390, 140))
        self.group_box_items.setObjectName("group_box_items")

        self.vertical_layout_widget_items = QtWidgets.QWidget(self.group_box_items)
        self.vertical_layout_widget_items.setGeometry(QtCore.QRect(10, 15, 370, 120))
        self.vertical_layout_widget_items.setObjectName("vertical_layout_widget_items")
        self.vertical_layout_items = QtWidgets.QVBoxLayout(self.vertical_layout_widget_items)
        self.vertical_layout_items.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_items.setObjectName("vertical_layout_items")

        # array to hold button objects
        self.items_btns = [[None] * len(self.items_names[i]) for i in range(len(self.items_names))]

        for row in range(len(self.items_btns)):
            # create horizontal layout for each row
            curr_row = QtWidgets.QHBoxLayout()
            curr_row.setObjectName("horizontal_layout_items_row_" + str(row + 1))

            for col in range(len(self.items_btns[row])):
                self.items_btns[row][col] = QtWidgets.QPushButton(self.vertical_layout_widget_items)
                curr_btn = self.items_btns[row][col]
                curr_btn.setMaximumSize(QtCore.QSize(50, 50))
                curr_btn.setObjectName("btn_items_" + self.items_names[row][col].replace("-", "_"))
                if self.items_names[row][col] == self.curr_item[0]:
                    curr_btn.setStyleSheet("border: 2px solid yellow")
                curr_btn.clicked.connect(self.on_click_btn_items)
                curr_row.addWidget(curr_btn)
            self.vertical_layout_items.addLayout(curr_row)

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
                if row == 2:
                    row = 1
                    col = 5

                # if other items was selected before, reset color of previous btn to deflaut
                if self.curr_item[0]:
                    last_item_btn = self.items_btns[self.curr_item[1]][self.curr_item[2]]
                    last_item_btn.setStyleSheet("")
                
                # set curr_item to the item of the btn and change btn color to green
                curr_btn.setStyleSheet("border: 2px solid yellow")
                self.curr_item = (item_name, row, col)

            self.update_label_text(self.label_curr_item, self.curr_item_full_text[self.curr_item[0]])
            self.update_combo_box_items(self.combo_box_attributes)

    # - group_box_classes -
    def add_group_box_classes(self):
        self.group_box_classes = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_classes.setGeometry(QtCore.QRect(10, 160, 390, 80))
        self.group_box_classes.setObjectName("group_box_classes")

        self.horizontal_layout_widget_classes = QtWidgets.QWidget(self.group_box_classes)
        self.horizontal_layout_widget_classes.setGeometry(QtCore.QRect(10, 15, 370, 60))
        self.horizontal_layout_widget_classes.setObjectName("horizontal_layout_widget_classes")
        self.horizontal_layout_classes = QtWidgets.QHBoxLayout(self.horizontal_layout_widget_classes)
        self.horizontal_layout_classes.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_classes.setObjectName("horizontal_layout_classes")

        # array to hold button objects
        self.classes_btns = [None] * len(self.classes_names)

        for col in range(len(self.classes_names)):
            self.classes_btns[col] = QtWidgets.QPushButton(self.horizontal_layout_widget_classes)
            curr_btn = self.classes_btns[col]
            curr_btn.setMaximumSize(QtCore.QSize(50, 50))
            curr_btn.setObjectName("btn_classes_" + self.classes_names[col])
            if self.classes_names[col] == self.curr_class[0]:
                curr_btn.setStyleSheet("border: 2px solid yellow")
            curr_btn.clicked.connect(self.on_click_btn_classes)
            self.horizontal_layout_classes.addWidget(curr_btn)

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
            self.update_combo_box_items(self.combo_box_attributes)

    # - group_box_attributes -
    def add_group_box_attributes(self):
        self.group_box_attributes = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_attributes.setGeometry(QtCore.QRect(10, 270, 390, 80))
        self.group_box_attributes.setObjectName("group_box_attributes")

        self.label_curr_item = QtWidgets.QLabel(self.group_box_attributes)
        self.label_curr_item.setGeometry(QtCore.QRect(10, 22, 150, 16))
        self.label_curr_item.setObjectName("label_curr_item")

        self.label_curr_class = QtWidgets.QLabel(self.group_box_attributes)
        self.label_curr_class.setGeometry(QtCore.QRect(170, 22, 100, 16))
        self.label_curr_class.setObjectName("label_curr_class")

        self.btn_add_attr = QtWidgets.QPushButton(self.group_box_attributes)
        self.btn_add_attr.setGeometry(QtCore.QRect(305, 20, 75, 20))
        self.btn_add_attr.setObjectName("btn_add_attr")
        self.btn_add_attr.clicked.connect(self.on_click_btn_add_attr)

        self.combo_box_attributes = QtWidgets.QComboBox(self.group_box_attributes)
        self.combo_box_attributes.setGeometry(QtCore.QRect(10, 45, 310, 21))
        self.combo_box_attributes.setObjectName("combo_box_attributes")
        self.combo_box_attributes.activated.connect(self.on_combo_box_attributes_selected)

        self.double_spin_box_attributes = QtWidgets.QDoubleSpinBox(self.group_box_attributes)
        self.double_spin_box_attributes.setGeometry(QtCore.QRect(330, 45, 50, 21))
        self.double_spin_box_attributes.setDecimals(1)
        self.double_spin_box_attributes.setSingleStep(0.1)
        self.double_spin_box_attributes.setMaximum(0)
        self.double_spin_box_attributes.setObjectName("double_spin_box_attributes")

    def update_label_text(self, label, text):
        _translate = QtCore.QCoreApplication.translate
        label.setText(_translate("MainWindow", text))

    def update_combo_box_items(self, combo_box):
        # clean up combo box and reset double spin box
        self.selected_attribute = ""
        self.selected_attribute_value = 0
        combo_box.clear()

        # only add attibutes to the box if an item is selected
        if self.curr_item[0]:
            item_name = self.curr_item_full_text[self.curr_item[0]]
            class_name = self.curr_class_full_text[self.curr_class[0]]
            for attr in ITEM_ATTR_LIST[item_name][class_name]:
                combo_box.addItem(attr)
            
            # automatically set selected_attribute to first item in the combo box
            self.selected_attribute = combo_box.itemText(0)
            self.update_double_spin_box_attributes_properities(item_name, class_name)
        else:
            # if no item selected, reset double spin box
            self.double_spin_box_attributes.setValue(0.0)
            self.double_spin_box_attributes.setMaximum(0.0)

    def on_combo_box_attributes_selected(self, index):
        self.selected_attribute = self.combo_box_attributes.itemText(index)
        item_name = self.curr_item_full_text[self.curr_item[0]]
        class_name = self.curr_class_full_text[self.curr_class[0]]
        self.update_double_spin_box_attributes_properities(item_name, class_name)

    def update_double_spin_box_attributes_properities(self, item_name, class_name):
        # if no attribute in combo box, reset double spin box
        if not self.selected_attribute:
            self.double_spin_box_attributes.setValue(0.0)
            self.double_spin_box_attributes.setMaximum(0.0)
            return

        # find out data of selected attribute of current class and item
        attr_data = ITEM_ATTR_LIST[item_name][class_name][self.selected_attribute]
        max_value = 999 if attr_data["max_value"] == 0 else attr_data["max_value"]
        self.double_spin_box_attributes.setSingleStep(attr_data["increment"])
        self.double_spin_box_attributes.setValue(0.0)
        self.double_spin_box_attributes.setMaximum(max_value)

    def on_click_btn_add_attr(self):
        if self.selected_attribute:
            item_name = self.curr_item_full_text[self.curr_item[0]]
            value = round(self.double_spin_box_attributes.value(), 1)
            self.criterias[item_name]["Attributes Needed"][self.selected_attribute] = value
            self.add_node_to_criterias_tree(item_name, value)

    # - group_box_inventory -
    def add_group_box_inventory(self):
        self.group_box_inventory = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_inventory.setGeometry(QtCore.QRect(10, 370, 390, 180))
        self.group_box_inventory.setObjectName("group_box_inventory")

        # rows
        self.vertical_layout_widget_inventory = QtWidgets.QWidget(self.group_box_inventory)
        self.vertical_layout_widget_inventory.setGeometry(QtCore.QRect(0, 10, 390, 170))
        self.vertical_layout_widget_inventory.setObjectName("vertical_layout_widget_inventory")
        self.vertical_layout_inventory = QtWidgets.QVBoxLayout(self.vertical_layout_widget_inventory)
        self.vertical_layout_inventory.setContentsMargins(5, 5, 5, 5)
        self.vertical_layout_inventory.setSpacing(5)
        self.vertical_layout_inventory.setObjectName("vertical_layout_inventory")

        # array to hold button objects
        self.inventory_btns = [[None] * 11 for _ in range(3)]
        for row in range(3):
            # create horizontal layout for each row
            curr_row = QtWidgets.QHBoxLayout()
            curr_row.setContentsMargins(0, -1, 0, 0)
            curr_row.setSpacing(5)
            curr_row.setObjectName("horizontal_layout_inventory_row_" + str(row + 1))

            for col in range(11):
                self.inventory_btns[row][col] = QtWidgets.QPushButton(self.vertical_layout_widget_inventory)
                curr_btn = self.inventory_btns[row][col]
                curr_btn.setMaximumSize(QtCore.QSize(30, 50))
                curr_btn.setObjectName("btn_inventory_" + str(row * 11 + col + 1).zfill(2))
                if self.inventory_slot_to_check[row][col]:
                    curr_btn.setStyleSheet("background-color: green")
                else:
                    curr_btn.setStyleSheet("background-color: red")
                curr_btn.clicked.connect(self.on_click_btn_inventory)
                curr_row.addWidget(curr_btn)
            self.vertical_layout_inventory.addLayout(curr_row)

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

    def reset_group_box_inventory(self, temp_inventory):
        for row in range(len(temp_inventory)):
            for col in range(len(temp_inventory[row])):
                curr_btn = self.inventory_btns[row][col]
                if temp_inventory[row][col]:
                    curr_btn.setStyleSheet("background-color: green")
                else:
                    curr_btn.setStyleSheet("background-color: red")

    # - group_box_criterias -
    def add_group_box_criterias(self):
        self.group_box_criterias = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_criterias.setGeometry(QtCore.QRect(410, 20, 380, 480))
        self.group_box_criterias.setObjectName("group_box_criterias")

        self.tree_widget_criterias = QtWidgets.QTreeWidget(self.group_box_criterias)
        self.tree_widget_criterias.setGeometry(QtCore.QRect(10, 20, 360, 450))
        self.tree_widget_criterias.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tree_widget_criterias.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tree_widget_criterias.setObjectName("tree_widget_criterias")
        self.tree_widget_criterias.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.tree_widget_criterias.header().setDefaultSectionSize(30)
        self.tree_widget_criterias.setColumnWidth(0, 260)

        # variable to hold all the tree node
        self.criterias_tree = {}

        for item in self.criterias:
            node = QtWidgets.QTreeWidgetItem(self.tree_widget_criterias)
            self.criterias_tree[item] = {}
            self.criterias_tree[item]["node"] = node
            self.update_criterias_tree_text(node, item)
            for key in self.criterias[item]:
                child_node = QtWidgets.QTreeWidgetItem(node)
                self.criterias_tree[item][key] = {}
                self.criterias_tree[item][key]["node"] = child_node

                if key == "Matches Needed":
                    self.update_criterias_tree_text(child_node, key, self.criterias[item][key])
                elif key == "Attributes Needed":
                    self.update_criterias_tree_text(child_node, key)
                    
                    for attr in self.criterias[item][key]:
                        grandchild_node = QtWidgets.QTreeWidgetItem(child_node)
                        self.criterias_tree[item][key][attr] = grandchild_node
                        self.update_criterias_tree_text(grandchild_node, attr, self.criterias[item][key][attr], True)

    def update_criterias_tree_text(self, node, text, value=None, delete_btn=False):
        _translate = QtCore.QCoreApplication.translate
        node.setText(0, _translate("MainWindow", text))
        if value:
            node.setText(1, _translate("MainWindow", str(value)))
        if delete_btn:
            # node.setText(2, _translate("MainWindow", "x"))
            button = QtWidgets.QPushButton("X")
            button.setFixedSize(20, 20)
            button.setStyleSheet("QPushButton { text-align: center; }")
            button.clicked.connect(lambda: self.on_click_delete_tree_item(node))
            self.tree_widget_criterias.setItemWidget(node, 2, button)
            node.setTextAlignment(2, QtCore.Qt.AlignCenter)

    def add_node_to_criterias_tree(self, item_name, value):
        parent = self.criterias_tree[item_name]["Attributes Needed"]["node"]
        parent.setExpanded(True)
        parent.parent().setExpanded(True)
        # if selected attribute not in the tree yet, create a new node
        if self.selected_attribute not in self.criterias_tree[item_name]["Attributes Needed"]:
            self.criterias_tree[item_name]["Attributes Needed"][self.selected_attribute] = QtWidgets.QTreeWidgetItem(parent)
        node = self.criterias_tree[item_name]["Attributes Needed"][self.selected_attribute]
        self.update_criterias_tree_text(node, self.selected_attribute, value, True)

    def on_click_delete_tree_item(self, node):
        # find parent and the path in criterias
        parent = node.parent()
        item = parent.parent().text(0)
        key = parent.text(0)
        attr = node.text(0)
        
        # remove the attr from criterias and the node from the tree and the widget
        self.criterias[item][key].pop(attr)
        self.criterias_tree[item][key].pop(attr)
        parent.removeChild(node)

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
        MainWindow.setWindowTitle(_translate("MainWindow", "Junk Them!"))

        # menu items
        self.menu_file.setTitle(_translate("MainWindow", "File"))
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
        self.group_box_items.setTitle(_translate("MainWindow", "Items"))
        for row in range(len(self.items_btns)):
            for col in range(len(self.items_btns[row])):
                self.items_btns[row][col].setText(_translate("MainWindow", self.items_names[row][col]))

        # classes
        self.group_box_classes.setTitle(_translate("MainWindow", "Classes"))
        for col in range(len(self.classes_btns)):
            self.classes_btns[col].setText(_translate("MainWindow", self.classes_names[col]))

        # attributes
        self.group_box_attributes.setTitle(_translate("MainWindow", "Attributes"))
        self.label_curr_item.setText(_translate("MainWindow", self.curr_item_full_text[self.curr_item[0]]))
        self.label_curr_class.setText(_translate("MainWindow", self.curr_class_full_text[self.curr_class[0]]))
        self.btn_add_attr.setText(_translate("MainWindow", "Add Attr"))

        # inventory
        self.group_box_inventory.setTitle(_translate("MainWindow", "Inventory Slots"))
        for row in range(3):
            for col in range(11):
                curr_num = str(row * 11 + col + 1).zfill(2)
                self.inventory_btns[row][col].setText(_translate("MainWindow", curr_num))

        # criterias
        self.group_box_criterias.setTitle(_translate("MainWindow", "Criterias"))
        self.tree_widget_criterias.headerItem().setText(0, _translate("MainWindow", "Attr"))
        self.tree_widget_criterias.headerItem().setText(1, _translate("MainWindow", "Value"))
        self.tree_widget_criterias.headerItem().setText(2, _translate("MainWindow", "Delete"))

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
