import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QDialog, QLineEdit, QFormLayout, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from pymongo import MongoClient
from bson import ObjectId
from helpers.EnvVariables import EnvVariables

class EditCarWindow(QDialog):
    def __init__(self, car_data, parent=None):
        super().__init__(parent)
        self.car_data = car_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit Car")
        layout = QFormLayout(self)

        self.license_plate_edit = QLineEdit(self.car_data.get('license_plate', ''))
        self.type_edit = QLineEdit(self.car_data.get('type', ''))
        self.location_edit = QLineEdit(self.car_data.get('curr_rental_location', ''))
        self.mileage_edit = QLineEdit(str(self.car_data.get('mileage', '')))
        self.cost_day_edit = QLineEdit(str(self.car_data.get('cost_per_day', '')))
        self.cost_mile_edit = QLineEdit(str(self.car_data.get('cost_per_mile', '')))
        self.status_edit = QLineEdit(self.car_data.get('curr_car_status', ''))

        layout.addRow("License Plate:", self.license_plate_edit)
        layout.addRow("Type:", self.type_edit)
        layout.addRow("Location:", self.location_edit)
        layout.addRow("Mileage:", self.mileage_edit)
        layout.addRow("Cost per Day:", self.cost_day_edit)
        layout.addRow("Cost per Mile:", self.cost_mile_edit)
        layout.addRow("Status:", self.status_edit)

        buttonBox = QDialogButtonBox()
        save_button = buttonBox.addButton("Save Changes", QDialogButtonBox.ButtonRole.AcceptRole)
        save_button.clicked.connect(self.accept)
        cancel_button = buttonBox.addButton(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.clicked.connect(self.reject)
        layout.addRow(buttonBox)

    def accept(self):
        client = MongoClient('mongodb+srv://tears_user:sobbing.emoji@carrental.fiinqnj.mongodb.net/?retryWrites=true&w=majority&appName=CarRental')
        db = client['car_rental_data']
        cars_collection = db['cars']
        updated_data = {
            'license_plate': self.license_plate_edit.text(),
            'type': self.type_edit.text(),
            'curr_rental_location': self.location_edit.text(),
            'mileage': float(self.mileage_edit.text()),
            'cost_per_day': float(self.cost_day_edit.text()),
            'cost_per_mile': float(self.cost_mile_edit.text()),
            'curr_car_status': self.status_edit.text()
        }
        cars_collection.update_one({'_id': ObjectId(self.car_data['_id'])}, {'$set': updated_data})
        super().accept()

class CarMgmtWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.env_vars = EnvVariables()  # Environment variables instance
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Car Management")
        self.layout = QVBoxLayout(self)
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.populate_table_button = QPushButton("Car List")
        self.populate_table_button.clicked.connect(self.populate_table)
        self.layout.addWidget(self.populate_table_button)
        self.back_to_main_button = QPushButton("Back to Main Menu")
        self.back_to_main_button.clicked.connect(self.close)
        self.layout.addWidget(self.back_to_main_button)
        app = QApplication.instance()
        screen = app.primaryScreen()
        self.resize(int(screen.size().width() / 2), int(screen.size().height() / 2))
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)

    def populate_table(self):
        current_city = self.env_vars.get_city()  # Get the city from the environment variables
        client = MongoClient('mongodb+srv://tears_user:sobbing.emoji@carrental.fiinqnj.mongodb.net/?retryWrites=true&w=majority&appName=CarRental')
        db = client['car_rental_data']
        cars_collection = db['cars']
        cars = list(cars_collection.find({"curr_rental_location": current_city}))  # Filter by city
        self.table_widget.setRowCount(len(cars))
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels([
            "License Plate", "Type", "Current Rental Location",
            "Mileage", "Cost Per Day", "Cost Per Mile", "Current Car Status"
        ])
        for row, car in enumerate(cars):
            self.table_widget.setItem(row, 0, QTableWidgetItem(car['license_plate']))
            self.table_widget.setItem(row, 1, QTableWidgetItem(car['type']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(car['curr_rental_location']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(car['mileage'])))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(car['cost_per_day'])))
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(car['cost_per_mile'])))
            self.table_widget.setItem(row, 6, QTableWidgetItem(car['curr_car_status']))
            self.table_widget.item(row, 0).setData(Qt.ItemDataRole.UserRole, str(car['_id']))

    def on_cell_double_clicked(self, row, column):
        car_data = {self.table_widget.horizontalHeaderItem(i).text().lower().replace(" ", "_"): self.table_widget.item(row, i).text() for i in range(self.table_widget.columnCount())}
        car_data['_id'] = self.table_widget.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.open_edit_car_window(car_data)

    def open_edit_car_window(self, car_data):
        edit_dialog = EditCarWindow(car_data, self)
        if edit_dialog.exec() == QDialog.DialogCode.Accepted:
            self.populate_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarMgmtWindow()
    window.show()
    sys.exit(app.exec())

