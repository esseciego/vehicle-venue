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
                car_object = self.make_car_object(self.list_of_cars, i)
                self.list_layout.addWidget(car_object, int(i / 3), i % 3)

            self.car_list.setLayout(self.list_layout)

            # Scroll Area Properties
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.scroll.setWidgetResizable(True)
            self.scroll.setWidget(self.car_list)
            self.scroll.setFixedSize(int(screen_size.width() / 3) * 2, int(screen_size.height() / 3) * 2)

            return self.scroll

    def make_car_object(self, car_l, i):
        car_object = QPushButton('')
        icon = QtGui.QIcon('ui/images/car_icon.png')
        car_object.setIcon(icon)
        car_object.setIconSize(QtCore.QSize(200, 200))
        car_object.setFixedSize(200, 200)
        car_object.clicked.connect(lambda : self.CarWindow(car_object, i))
        return car_object

    def CarWindow(self, car_object, i):
        self.window_layout.show()

