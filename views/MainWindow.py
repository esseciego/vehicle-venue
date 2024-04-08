import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QScrollArea)


from views.LogInWindow import LogInWindow
from views.SignUpWindow import SignUpWindow
from views.SignUpWindow import screen_size
from models.Accounts import Accounts
from helpers.EnvVariables import EnvVariables
from views.CarList import CarList

class MainWindow(QWidget):
    # Basically the home page just a stand in
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setRowMinimumHeight(0, 50)
        self.layout.setRowMinimumHeight(1, 50)
        self.layout.setColumnMinimumWidth(0, int(screen_size.width() / 10))
        self.layout.setColumnMinimumWidth(2, int(screen_size.width() / 3) * 2)
        self.layout.setContentsMargins(50, 25, 50, 100)

        self.setWindowTitle("Home Page")
        self.setLayout(self.layout)

        self.resize(screen_size)

        self.account = Accounts()

        #Car collection list
        self.cars = CarList()
        self.car_list = self.cars.make_car_list()
        self.layout.addWidget(self.car_list, 2, 2)
        self.car_list.hide()

        # Welcomes to home page
        self.welcome_label = QLabel("Welcome to the VehicleVenue")
        self.welcome_label.setProperty("class", "heading")
        self.layout.addWidget(self.welcome_label, 2, 2, Qt.AlignmentFlag.AlignCenter)

        self.user_name_label = QLabel("Guest")
        self.user_name_label.setProperty("class", "heading")
        self.layout.addWidget(self.user_name_label, 0, 0, 0, 0, Qt.AlignmentFlag.AlignTop)

        #Tab that goes to the car list
        self.collection_tab = QPushButton("Car Collection")
        self.collection_tab.setFlat(True)
        self.collection_tab.clicked.connect(self.car_collection)
        self.layout.addWidget(self.collection_tab, 1, 0, Qt.AlignmentFlag.AlignRight)

        #Tab that goes to the home page
        self.home_tab = QPushButton("Home")
        self.home_tab.setFlat(True)
        self.home_tab.clicked.connect(self.home_page)
        self.layout.addWidget(self.home_tab, 1, 0, Qt.AlignmentFlag.AlignLeft)

        # Sign Up button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        self.layout.addWidget(sign_up_button, 1, 3)

        # Log In button
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.login_window)
        self.layout.addWidget(self.login_button, 1, 4)
        
        # Log Out button
        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button, 1, 4)


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

    def car_collection(self):
        self.welcome_label.hide()
        self.car_list.show()

    def home_page(self):
        self.car_list.hide()
        self.welcome_label.show()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
