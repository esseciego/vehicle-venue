from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import Qt
from pymongo import MongoClient
from bson import ObjectId
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import Qt
from pymongo import MongoClient
from bson import ObjectId



class CarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.car_table = QTableWidget()
        self.car_table.setColumnCount(5)  # Adjust the number based on car attributes
        self.car_table.setHorizontalHeaderLabels(["Make", "Model", "Year", "Status", "Location"])
        layout.addWidget(self.car_table)

        self.refresh_button = QPushButton("Refresh Car List")
        self.refresh_button.clicked.connect(self.load_cars)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.setWindowTitle("Car Management")
        self.load_cars()

    def load_cars(self):
        # Connect to the database and fetch car data
        client = MongoClient('your_connection_string')
        db = client['car_rental_database']
        cars_collection = db['cars']

        cars = list(cars_collection.find())

        self.populate_table(cars)

    def populate_table(self, cars):
        self.car_table.setRowCount(len(cars))
        for row, car in enumerate(cars):
            self.car_table.setItem(row, 0, QTableWidgetItem(car.get('make', '')))
            self.car_table.setItem(row, 1, QTableWidgetItem(car.get('model', '')))
            self.car_table.setItem(row, 2, QTableWidgetItem(str(car.get('year', ''))))
            self.car_table.setItem(row, 3, QTableWidgetItem(car.get('status', '')))
            self.car_table.setItem(row, 4, QTableWidgetItem(car.get('location', '')))

            # Store the car's ObjectId in the row for later reference
            self.car_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, str(car['_id']))

        self.car_table.cellChanged.connect(self.on_cell_changed)

    def on_cell_changed(self, row, column):
        car_id_str = self.car_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        new_value = self.car_table.item(row, column).text()

        if car_id_str:
            car_id = ObjectId(car_id_str)
            # Update logic here
            print(f"Updated car {car_id} in column {column} with new value: {new_value}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarWindow()
    window.show()
    sys.exit(app.exec())

