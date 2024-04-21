import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QDialog, QLineEdit, QFormLayout, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from pymongo import MongoClient
from bson import ObjectId

class EditCarWindow(QDialog):
    def __init__(self, car_data, parent=None):
        super().__init__(parent)
        self.car_data = car_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit Car")
        layout = QFormLayout(self)
        print(f"Car data received in edit window: {self.car_data}")

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
        cancel_button = buttonBox.addButton(QDialogButtonBox.StandardButton.Cancel)

        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        layout.addRow(buttonBox)

    def accept(self):
        # Update the car data in MongoDB
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

class CarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # UI setup
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
        size = screen.size()
        self.resize(int(size.width() / 2), int(size.height() / 2))

        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)


    def populate_table(self):
        client = MongoClient('mongodb+srv://tears_user:sobbing.emoji@carrental.fiinqnj.mongodb.net/?retryWrites=true&w=majority&appName=CarRental')
        db = client['car_rental_data']
        cars_collection = db['cars']

        # Fetch cars data from MongoDB
        cars = list(cars_collection.find())

        # Set the table row count and column count
        self.table_widget.setRowCount(len(cars))
        self.table_widget.setColumnCount(7)  # Update this if you have more or fewer columns

        # Set the table headers
        self.table_widget.setHorizontalHeaderLabels([
            "License Plate", "Type", "Current Rental Location",
            "Mileage", "Cost Per Day", "Cost Per Mile", "Current Car Status"
        ])

        # Populate the table rows with car data
        for row, car in enumerate(cars):
            self.table_widget.setItem(row, 0, QTableWidgetItem(car.get('license_plate', '')))
            self.table_widget.setItem(row, 1, QTableWidgetItem(car.get('type', '')))
            self.table_widget.setItem(row, 2, QTableWidgetItem(car.get('curr_rental_location', '')))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(car.get('mileage', ''))))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(car.get('cost_per_day', ''))))
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(car.get('cost_per_mile', ''))))
            self.table_widget.setItem(row, 6, QTableWidgetItem(car.get('curr_car_status', '')))
            # Store the MongoDB document ID in the first column's hidden data
            self.table_widget.item(row, 0).setData(Qt.ItemDataRole.UserRole, str(car['_id']))

    def on_cell_double_clicked(self, row, column):
        car_data = {}
        for col in range(self.table_widget.columnCount()):
            item = self.table_widget.item(row, col)
            header = self.table_widget.horizontalHeaderItem(col).text()
            key = header.lower().replace(" ", "_")
            car_data[key] = item.text() if item else ''

        _id_item = self.table_widget.item(row, 0)
        car_data['_id'] = _id_item.data(Qt.ItemDataRole.UserRole)
        self.open_edit_car_window(car_data)

    def open_edit_car_window(self, car_data):
        edit_dialog = EditCarWindow(car_data, self)
        if edit_dialog.exec() == QDialog.DialogCode.Accepted:
            self.populate_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarWindow()
    window.show()
    sys.exit(app.exec())