import sys
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit)

class SpecificCarWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()

        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)