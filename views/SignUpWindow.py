import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit)


class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(50)

        self.setWindowTitle("Log In")
        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

        # First Name Label
        user_name_first = QLabel("First Name")
        user_name_first.setProperty("class", "normal")
        self.layout.addWidget(user_name_first, 0, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 0, 1, 1, 2)

        # Last Name Label
        user_name_last = QLabel("Last Name")
        user_name_last.setProperty("class", "normal")
        self.layout.addWidget(user_name_last, 1, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 1, 1, 1, 2)

        # Username label
        user_name = QLabel("Username:")
        user_name.setProperty("class", "normal")
        self.layout.addWidget(user_name, 2, 0)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 2, 1, 1, 2)

        # Password Label
        user_name_first = QLabel("Password")
        user_name_first.setProperty("class", "normal")
        self.layout.addWidget(user_name_first, 3, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 3, 1, 1, 2)

        # Email Label
        user_name_first = QLabel("Email Address")
        user_name_first.setProperty("class", "normal")
        self.layout.addWidget(user_name_first, 4, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 4, 1, 1, 2)


app = QApplication(sys.argv)
screen = app.primaryScreen()
screen_size = screen.size()
