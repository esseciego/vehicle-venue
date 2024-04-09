import sys
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit, QVBoxLayout)

from views.SignUpWindow import screen_size

class SpecificCarWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.SUV_pixmap = QPixmap('ui/images/car_icon.png')
        self.SUV_pixmap = self.SUV_pixmap.scaled(200, 200)
        self.label = QLabel()
        self.label.setPixmap(self.SUV_pixmap)
        self.label.setFixedSize(self.SUV_pixmap.width(), self.SUV_pixmap.height())

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)