import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QScrollArea)

from views.SignUpWindow import screen_size
from views.SpecificCarWindow import SpecificCarWindow
from models.Cars import Cars
from models.Car import Car

class CarList(QWidget):
    def __init__(self):
        super().__init__()

        self.window_layout = SpecificCarWindow()

        # Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True) # Scroll Area which contains the widgets
        self.scroll.setFixedSize(int(screen_size.width() * .6), int(screen_size.height() * .75))

        self.cars = Cars()
        self.list_of_cars = self.cars.get_all_cars()

    def make_car_list(self, rental_period=[]):
        list_layout = QGridLayout()  # Layout of the cars
        car_list = QWidget()  # Widget that contains the collection of the cars
        for i in range(self.cars.get_num_cars()):
            if self.check_available_cars(i, rental_period):
                car_object = self.make_car_object(i)
                list_layout.addWidget(car_object, int(i / 3), i % 3)

        car_list.setLayout(list_layout)
        self.scroll.setWidget(car_list)

        return self.scroll

    def check_available_cars(self, i, rental_period):
        for date in self.list_of_cars[i]['rental_dates']:
            if date in rental_period:
                return False
        return True

    def make_car_object(self, i):
        car_button = QPushButton('')
        if self.list_of_cars[i]['type'] == "SUV":
            icon = QtGui.QIcon('ui/images/suv_icon.png')
        elif self.list_of_cars[i]['type'] == "Van":
            icon = QtGui.QIcon('ui/images/van_icon.png')
        else:
            icon = QtGui.QIcon('ui/images/sedan_icon.png')
        car_button.setIcon(icon)
        car_button.setIconSize(QtCore.QSize(200, 200))
        car_button.setFixedSize(200, 200)
        car_button.clicked.connect(lambda : self.car_window(i))

        return car_button

    def car_window(self, i):
        self.window_layout.set_pixmap(self.list_of_cars[i]['type'])

        self.window_layout.license_plate_label.setText("License plate number: " + self.list_of_cars[i]['license_plate'])
        self.window_layout.type_label.setText("Type: " + self.list_of_cars[i]['type'])
        self.window_layout.curr_rental_location_label.setText("Location: " + self.list_of_cars[i]['curr_rental_location'])
        self.window_layout.mileage_label.setText("Mileage: " + self.list_of_cars[i]['mileage'])
        self.window_layout.cost_per_day_label.setText("Cost Per Day: " + self.list_of_cars[i]['cost_per_day'])
        self.window_layout.cost_per_mile_label.setText("Cost Per Mile: " + self.list_of_cars[i]['cost_per_mile'])

        self.window_layout.show()

