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

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets
        self.car_list = QWidget()  # Widget that contains the collection of the cars
        self.list_layout = QGridLayout() #Layout of the cars

        self.cars = Cars()

        self.list_of_cars = self.cars.show_all_cars()

    def make_car_list(self):
            for i in range(self.cars.get_num_cars()):
                car_object = self.make_car_object(i)
                self.list_layout.addWidget(car_object, int(i / 3), i % 3)

            self.car_list.setLayout(self.list_layout)

            # Scroll Area Properties
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.scroll.setWidgetResizable(True)
            self.scroll.setWidget(self.car_list)
            self.scroll.setFixedSize(int(screen_size.width() / 3) * 2, int(screen_size.height() / 4) * 3)

            return self.scroll

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

