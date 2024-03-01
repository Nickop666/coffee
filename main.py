main.py

import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coffee App")
        self.setGeometry(100, 100, 600, 400)

        self.db = sqlite3.connect("coffee.sqlite")
        self.cursor = self.db.cursor()

        self.create_table_view()
        self.create_add_edit_form()
        self.show()

    def create_table_view(self):
        self.table_view = QtWidgets.QTableView()
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "Name", "Roast Level", "Ground/Whole Bean", "Flavor Description", "Price", "Volume"])
        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()

        self.cursor.execute("SELECT * FROM coffee")
        for row in self.cursor.fetchall():
            self.model.appendRow([QtWidgets.QStandardItem(str(row[0])),
                                 QtWidgets.QStandardItem(row[1]),
                                 QtWidgets.QStandardItem(row[2]),
                                 QtWidgets.QStandardItem(row[3]),
                                 QtWidgets.QStandardItem(row[4]),
                                 QtWidgets.QStandardItem(str(row[5])),
                                 QtWidgets.QStandardItem(str(row[6]))])

        self.setCentralWidget(self.table_view)

    def create_add_edit_form(self):
        self.add_edit_form = QtWidgets.QDialog()
        self.add_edit_form.setWindowTitle("Add/Edit Coffee")
        self.add_edit_form.setGeometry(100, 100, 300, 200)

        self.form_layout = QtWidgets.QFormLayout()
        self.add_edit_form.setLayout(self.form_layout)

        self.name_label = QtWidgets.QLabel("Name:")
        self.name_edit = QtWidgets.QLineEdit()
        self.form_layout.addRow(self.name_label, self.name_edit)

        self.roast_level_label = QtWidgets.QLabel("Roast Level:")
        self.roast_level_combo = QtWidgets.QComboBox()
        self.roast_level_combo.addItems(["Light", "Medium", "Dark"])
        self.form_layout.addRow(self.roast_level_label, self.roast_level_combo)

        self.ground_whole_bean_label = QtWidgets.QLabel("Ground/Whole Bean:")
        self.ground_whole_bean_combo = QtWidgets.QComboBox()
        self.ground_whole_bean_combo.addItems(["Ground", "Whole Bean"])
        self.form_layout.addRow(self.ground_whole_bean_label, self.ground_whole_bean_combo)

        self.flavor_description_label = QtWidgets.QLabel("Flavor Description:")
        self.flavor_description_edit = QtWidgets.QTextEdit()
        self.form_layout.addRow(self.flavor_description_label, self.flavor_description_edit)

        self.price_label = QtWidgets.QLabel("Price:")
        self.price_edit = QtWidgets.QDoubleSpinBox()
        self.price_edit.setRange(0.01, 1000.00)
        self.price_edit.setSingleStep(0.01)
        self.form_layout.addRow(self.price_label, self.price_edit)

        self.volume_label = QtWidgets.QLabel("Volume:")
        self.volume_spinbox = QtWidgets.QSpinBox()
        self.volume_spinbox.setRange(1, 100)
        self.form_layout.addRow(self.volume_label, self.volume_spinbox)

        self.add_button = QtWidgets.QPushButton("Add")
        self.add_button.clicked.connect(self.add_coffee)
        self.edit_button = QtWidgets.QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_coffee)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.add_edit_form.close)

        self.button_box = QtWidgets.QDialogButtonBox()
        self.button_box.addButton(self.add_button, QtWidgets.QDialogButtonBox.ActionRole)
        self.button_box.addButton(self.edit_button, QtWidgets.QDialogButtonBox.ActionRole)
        self.button_box.addButton(self.cancel_button, QtWidgets.QDialogButtonBox.RejectRole)
        self.form_layout.addRow(self.button_box)

    def add_coffee(self):
        name = self.name_edit.text()
        roast_level = self.roast_level_combo.currentText()
        ground_whole_bean = self.ground_whole_bean_combo.currentText()
        flavor_description = self.flavor_description_edit.toPlainText()
        price = self.price_edit.value()
        volume = self.volume_spinbox.value()

        self.cursor.execute("INSERT INTO coffee (name, roast_level, ground_whole_bean, flavor_description, price, volume) VALUES (?, ?, ?, ?, ?, ?)",
                            (name, roast_level, ground_whole_bean, flavor_description, price, volume))
        self.db.commit()

        self.update_table_view()
        self.add_edit_form.close()

    def edit_coffee(self):
        selected_row = self.table_view.selectedIndexes()[0].row()
        coffee_id = self.model.item(selected_row, 0).text()

        name = self.name_edit.text()
        roast_level = self.roast_level_combo.currentText()
        ground_whole_bean = self.ground_whole_bean_combo.currentText()
        flavor_description = self.flavor_description_edit.toPlainText()
        price = self.price_edit.value()
        volume = self.volume_spinbox.value()

        self.cursor.execute("UPDATE coffee SET name=?, roast_level=?, ground_whole_bean=?, flavor_description=?, price=?, volume=? WHERE id=?",
                            (name, roast_level, ground_whole_bean, flavor_description, price, volume, coffee_id))
        self.db.commit()

        self.update_table_view()
        self.add_edit_form.close()

    def update_table_view(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["ID", "Name", "Roast Level", "Ground/Whole Bean", "Flavor Description", "Price", "Volume"])

        self.cursor.execute("SELECT * FROM coffee")
        for row in self.cursor.fetchall():
            self.model.appendRow([QtWidgets.QStandardItem(str(row[0])),
                                 QtWidgets.QStandardItem(row[1]),
                                 QtWidgets.QStandardItem(row[2]),
                                 QtWidgets.QStandardItem(row[3]),
                                 QtWidgets.QStandardItem(row[4]),
                                 QtWidgets.QStandardItem(str(row[5])),
                                 QtWidgets.QStandardItem(str(row[6]))])

        self.table_view.resizeColumnsToContents()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    coffee_app = CoffeeApp()
    sys.exit(app.exec_())
