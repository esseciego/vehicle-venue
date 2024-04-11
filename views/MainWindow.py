import sys
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, )

from views.LogInWindow import LogInWindow
from views.SignUpWindow import SignUpWindow
from views.SettingsWindow import SettingsWindow
from views.SignUpWindow import screen_size
from models.Accounts import Accounts
from helpers.EnvVariables import EnvVariables
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from views.CarWindow import CarWindow




class MainWindow(QWidget):
    # Basically the home page just a stand in
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(10)

        self.setWindowTitle("Home Page")
        self.setLayout(self.layout)

        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_size = screen.size()

        self.resize(screen_size)

        self.account = Accounts()

        # Welcomes to home page
        welcome_label = QLabel("Welcome to the VehicleVenue")
        welcome_label.setProperty("class", "heading")
        self.layout.addWidget(welcome_label, 0, 0, 3, 0, Qt.AlignmentFlag.AlignCenter)

        self.user_name_label = QLabel("Guest")
        self.user_name_label.setProperty("class", "heading")
        self.layout.addWidget(self.user_name_label, 0, 0, 0, 0, Qt.AlignmentFlag.AlignTop)

        self.car_window_button = QPushButton("Car Window")
        self.car_window_button.clicked.connect(self.open_car_window)
        self.layout.addWidget(self.car_window_button, 1, 0)

        self.car_window_instance = None  # Keep a reference to the car window

        # Sign Up button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        self.layout.addWidget(sign_up_button, 0, 3)

        # Log In button
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.login_window)
        self.layout.addWidget(self.login_button, 0, 4)

        # Log Out button
        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button, 0, 4)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.settings_window)
        self.layout.addWidget(settings_button, 0, 5)

        self.settings_window_instance = None

        self. logout_button.hide()

        self.sign_up_window = SignUpWindow()
        self.sign_up_window.window_closed.connect(self.login_check)

        self.login_window = LogInWindow()
        self.login_window.window_closed.connect(self.login_check)


    def log_in_window(self):
        self.log_in_window = LogInWindow()
        self.log_in_window.show()

    def sign_up_window(self):
        self.sign_up_window.show()


    def settings_window(self):
        if self.settings_window_instance is None or not self.settings_window_instance.isVisible():
            self.settings_window_instance = SettingsWindow()
        self.settings_window_instance.show()

    def open_car_window(self):
        # This function opens the car management window
        if self.car_window_instance is None or not self.car_window_instance.isVisible():
            self.car_window_instance = CarWindow()
        self.car_window_instance.show()

    def login_window(self):
        self.login_window.show()

    def logout(self):
        self.account.logout()
        self.login_check()
        self.user_name_label.setText("Guest")

    def login_check(self):
        #checks if a user is logged in
        #if a user is not logged in the User = NONE
        env_vars = EnvVariables()
        if env_vars.get_user() == "NONE":
            self.login_button.show()
            self.logout_button.hide()
        else:
            self.logout_button.show()
            self.login_button.hide()
            self.user_name_label.setText(env_vars.get_user())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
