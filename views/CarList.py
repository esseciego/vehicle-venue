import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (Qt, pyqtSignal, QDate)
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
        self.scroll.setFixedSize(int(screen_size.width() * .58), int(screen_size.height() * .75))

        self.cars = Cars()
        self.list_of_cars = self.cars.get_all_cars()

    def make_car_list(self, start_date=QDate.currentDate(), end_date=QDate.currentDate().addDays(1), rental_period=[]):
        list_layout = QGridLayout()  # Layout of the cars
        car_list = QWidget()  # Widget that contains the collection of the cars
        for i in range(self.cars.get_num_cars()):
            if self.check_available_cars(i, rental_period):
                car_object = self.make_car_object(i)
                list_layout.addWidget(car_object, int(i / 3), i % 3)

        car_list.setLayout(list_layout)
        self.scroll.setWidget(car_list)
        self.window_layout.set_dates(start_date, end_date)

        return self.scroll

    def check_available_cars(self, i, rental_period):
        if rental_period:
            for date in self.list_of_cars[i]['rental_dates']:
                start_date = QDate.fromString(date[0], Qt.DateFormat.ISODate)
                end_date = QDate.fromString(date[1], Qt.DateFormat.ISODate)

                if rental_period[0] <= start_date <= rental_period[1]:
                    return False
                if rental_period[0] <= end_date <= rental_period[1]:
                    return False

                if start_date <= rental_period[0] <= end_date:
                    return False
                if start_date <= rental_period[1] <= end_date:
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

        self.window_layout.license_plate = self.list_of_cars[i]['license_plate']
        self.window_layout.rental_dates = self.list_of_cars[i]['rental_dates']
        self.window_layout.data_label.setText("License plate number: " + self.list_of_cars[i]['license_plate']
                                                       + "\n\nType: " + self.list_of_cars[i]['type']
                                                       + "\n\nLocation: " + self.list_of_cars[i]['curr_rental_location']
                                                       + "\n\nMileage: " + self.list_of_cars[i]['mileage']
                                                       + "\n\nCost Per Day: " + self.list_of_cars[i]['cost_per_day']
                                                       + "\n\nCost Per Mile: " + self.list_of_cars[i]['cost_per_mile'])

        self.window_layout.show()

