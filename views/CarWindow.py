import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from pymongo import MongoClient
from bson import ObjectId

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
        self.populate_table_button = QPushButton("Load Cars")
        self.populate_table_button.clicked.connect(self.populate_table)
        self.layout.addWidget(self.populate_table_button)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarWindow()
    window.show()
    sys.exit(app.exec())
