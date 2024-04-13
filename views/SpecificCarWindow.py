import sys
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit, QVBoxLayout, QHBoxLayout)

from views.SignUpWindow import screen_size

class SpecificCarWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reserve a Car")

        self.layout = QHBoxLayout()
        self.layout.setSpacing(60)
        self.layoutV = QVBoxLayout()

        self.car_pixmap = QPixmap()

        self.car_image = QLabel()

        self.license_plate_label = QLabel()
        self.type_label = QLabel()
        self.curr_rental_location_label = QLabel()
        self.mileage_label = QLabel()
        self.cost_per_day_label = QLabel()
        self.cost_per_mile_label = QLabel()

        self.layout.addWidget(self.car_image)

        self.layoutV.addWidget(self.license_plate_label)
        self.layoutV.addWidget(self.type_label)
        self.layoutV.addWidget(self.curr_rental_location_label)
        self.layoutV.addWidget(self.mileage_label)
        self.layoutV.addWidget(self.cost_per_day_label)
        self.layoutV.addWidget(self.cost_per_mile_label)

        self.layout.addLayout(self.layoutV)

        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

    def set_pixmap(self, type):
        if type == "SUV":
            self.car_pixmap = QPixmap('ui/images/suv_icon.png')
        elif type == "Van":
            self.car_pixmap = QPixmap('ui/images/van_icon.png')
        else:
            self.car_pixmap = QPixmap('ui/images/sedan_icon.png')

        self.car_pixmap = self.car_pixmap.scaled(200, 200)
        self.car_image.setPixmap(self.car_pixmap)
        self.car_image.setFixedSize(self.car_pixmap.width(), self.car_pixmap.height())
