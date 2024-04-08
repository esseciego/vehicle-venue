import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (Qt, pyqtSignal,)
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QListWidget, QVBoxLayout)

class CarIcon(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        self.car_icon = QPushButton('Car')
        #icon = QtGui.QIcon('car_icon.png')
        #self.car_icon.setIcon(icon)
        #self.car_icon.setIconSize(QtCore.QSize(200, 200))
        #self.car_icon.setFixedSize(200, 200)

        self.layout.addWidget(self.car_icon, 0, 0)
