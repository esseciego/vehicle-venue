import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QScrollArea, QCalendarWidget, QVBoxLayout)


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
        self.layout.setRowMinimumHeight(0, int(screen_size.height() * .1))
        self.layout.setRowMinimumHeight(1, int(screen_size.height() * .75))
        self.layout.setColumnMinimumWidth(0, int(screen_size.width() * .15))
        self.layout.setColumnMinimumWidth(1, int(screen_size.width() * .6))
        self.layout.setColumnMinimumWidth(2, int(screen_size.width() * .15))
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(25, 30, 25, 50)

        self.calendar_layout = QVBoxLayout()

        self.setWindowTitle("Home Page")
        self.setLayout(self.layout)

        self.setFixedSize(int(screen_size.width()), int(screen_size.height() * .92))

        self.account = Accounts()

        #Car collection list
        self.cars = CarList()
        self.car_list = self.cars.make_car_list()
        self.layout.addWidget(self.car_list, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        self.car_list.hide()

        # Welcomes to home page
        self.welcome_label = QLabel("Welcome to the VehicleVenue\n\n"
                                    "Project Manager: Esse Ciego\n"
                                    "Scrum Master: Truman Moore\n"
                                    "Development Team: Austin Wing and Reid Castillo")
        self.welcome_label.setProperty("class", "heading")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.welcome_label, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.user_name_label = QLabel("Guest")
        self.user_name_label.setProperty("class", "heading")
        self.layout.addWidget(self.user_name_label, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        #Tab that goes to the car list
        self.collection_tab = QPushButton("Car Collection")
        self.collection_tab.setFlat(True)
        self.collection_tab.clicked.connect(self.car_collection)
        self.layout.addWidget(self.collection_tab, 0, 0, Qt.AlignmentFlag.AlignHCenter)

        #Tab that goes to the home page
        self.home_tab = QPushButton("Home")
        self.home_tab.setFlat(True)
        self.home_tab.clicked.connect(self.home_page)
        self.layout.addWidget(self.home_tab, 0, 0, Qt.AlignmentFlag.AlignLeft)

        # Sign Up button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        self.layout.addWidget(sign_up_button, 0, 2, Qt.AlignmentFlag.AlignLeft)
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.window_closed.connect(self.login_check)

        # Log In button
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.login_window)
        self.layout.addWidget(self.login_button, 0, 2, Qt.AlignmentFlag.AlignHCenter)
        self.login_window = LogInWindow()
        self.login_window.window_closed.connect(self.login_check)
        
        # Log Out button
        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button, 0, 2, Qt.AlignmentFlag.AlignHCenter)
        self. logout_button.hide()

        # Settings button
        self.settings_button = QPushButton("Settings")
        self.layout.addWidget(self.settings_button, 0, 2, Qt.AlignmentFlag.AlignRight)

        self.start_date_label = QLabel("Enter Start Date")
        self.calendar_layout.addWidget(self.start_date_label)

        self.start_date_calendar = QCalendarWidget()
        self.calendar_layout.addWidget(self.start_date_calendar)

        self.end_date_label = QLabel("Enter End Date")
        self.calendar_layout.addWidget(self.end_date_label)

        self.end_date_calendar = QCalendarWidget()
        self.calendar_layout.addWidget(self.end_date_calendar)

        self.layout.addLayout(self.calendar_layout, 1, 2)

    def log_in_window(self):
        self.log_in_window = LogInWindow()
        self.log_in_window.show()

    def sign_up_window(self):
        self.setDisabled(True)
        self.sign_up_window.show()

    def login_window(self):
        self.setDisabled(True)
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
        self.setDisabled(False)

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
