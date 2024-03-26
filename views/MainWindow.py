import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel)

from views.LogInWindow import LogInWindow
from views.SignUpWindow import SignUpWindow
from views.SignUpWindow import screen_size
from models.Accounts import Accounts


class MainWindow(QWidget):
    # Basically the home page just a stand in
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(100)

        self.setWindowTitle("Home Page")
        self.setLayout(self.layout)

        self.resize(screen_size)

        self.account = Accounts()

        # Welcomes to home page
        welcome_label = QLabel("Welcome to the VehicleVenue")
        welcome_label.setProperty("class", "heading")
        self.layout.addWidget(welcome_label, 0, 0, 3, 0, Qt.AlignmentFlag.AlignCenter)

        # Sign Up button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        self.layout.addWidget(sign_up_button, 0, 3)

        # Log In button
        login_button = QPushButton("Log In")
        login_button.clicked.connect(self.login_window)
        self.layout.addWidget(login_button, 0, 4)

        # Log Out button
        logout_button = QPushButton("Log Out")
        logout_button.clicked.connect(self.logout)
        self.layout.addWidget(logout_button, 0, 4)
        logout_button.hide()

    def login_window(self):
        self.login_window = LogInWindow()
        self.login_window.show()

    def logout(self):
        self.account.logout()

    def sign_up_window(self):
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.show()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
