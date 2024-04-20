import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (Qt, pyqtSignal, QDate)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QScrollArea, QCalendarWidget, QVBoxLayout)


from views.LogInWindow import LogInWindow
from views.SignUpWindow import SignUpWindow
from views.SignUpWindow import screen_size
from views.CarWindow import CarWindow
from views.CarList import CarList
from views.SettingsWindow import SettingsWindow
from models.Accounts import Accounts
from helpers.EnvVariables import EnvVariables


class MainWindow(QWidget):
    # Basically the home page just a stand in
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setRowMinimumHeight(0, int(screen_size.height() * .1))
        self.layout.setRowMinimumHeight(1, int(screen_size.height() * .75))
        self.layout.setColumnMinimumWidth(0, int(screen_size.width() * .15))
        self.layout.setColumnMinimumWidth(1, int(screen_size.width() * .58))
        self.layout.setColumnMinimumWidth(2, int(screen_size.width() * .23))
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(25, 30, 25, 50)

        self.calendar_layout = QVBoxLayout()

        self.setWindowTitle("Home Page")
        self.setLayout(self.layout)

        self.setFixedSize(int(screen_size.width()), int(screen_size.height() * .92))

        self.account = Accounts()

        # Car collection list
        self.cars = CarList()
        self.car_list = self.cars.make_car_list()
        self.layout.addWidget(self.car_list, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.cars.username_signal.connect(self.login_check)
        self.car_list.hide()

        # Welcomes to home page
        self.welcome_label = QLabel("Welcome to the VehicleVenue\n\n"
                                    "Project Manager: Esse Ciego\n"
                                    "Scrum Master: Truman Moore\n"
                                    "Development Team: Austin Wing and Reid Castillo")
        self.welcome_label.setProperty("class", "heading")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.welcome_label, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Guest text
        self.user_name_label = QLabel("Guest")
        self.user_name_label.setProperty("class", "heading")
        self.layout.addWidget(self.user_name_label, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # TODO: Align "Manage Cars" button to be adjacent to other buttons
        self.car_mgmt_window_instance = None  # Keep a reference to the car window
        self.car_mgmt_window_button = QPushButton("Manage Cars")
        self.car_mgmt_window_button.clicked.connect(self.car_mgmt_window)
        self.layout.addWidget(self.car_mgmt_window_button, 1, 0)

        # CarList tab
        self.collection_tab = QPushButton("Car Collection")
        self.collection_tab.setFlat(True)
        self.collection_tab.clicked.connect(self.car_collection)
        self.layout.addWidget(self.collection_tab, 0, 0, Qt.AlignmentFlag.AlignHCenter)

        # HomePage tab
        self.home_tab = QPushButton("Home")
        self.home_tab.setFlat(True)
        self.home_tab.clicked.connect(self.home_page)
        self.layout.addWidget(self.home_tab, 0, 0, Qt.AlignmentFlag.AlignLeft)

        # SignUp button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        self.layout.addWidget(sign_up_button, 0, 2, Qt.AlignmentFlag.AlignLeft)
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.window_closed.connect(self.login_check)

        # LogIn button
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.login_window)
        self.layout.addWidget(self.login_button, 0, 2, Qt.AlignmentFlag.AlignHCenter)
        self.login_window = LogInWindow()
        self.login_window.window_closed.connect(self.login_check)

        # LogOut button
        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button, 0, 2, Qt.AlignmentFlag.AlignHCenter)
        self.logout_button.hide()

        # FIXME: Make sure comments on each widget are consistent (check different windows too)
        # FIXME: Make sure widget styles are consistent
            # Might need to force Truman's changes?

        # Settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.settings_window)
        self.layout.addWidget(self.settings_button, 0, 2, Qt.AlignmentFlag.AlignRight)
        self.settings_window_instance = None

        # Guide text
        self.guide_label = QLabel("Choose a Start and End Dates of Desired Rental Period")
        self.calendar_layout.addWidget(self.guide_label)
        self.guide_label.hide()

        # Enter start date prompt
        self.start_date_label = QLabel("Enter Start Date")
        self.calendar_layout.addWidget(self.start_date_label)
        self.start_date_label.hide()

        # Calendar where user can enter start date
        self.start_date_calendar = QCalendarWidget()
        self.start_date_calendar.setMinimumDate(QDate.currentDate())
        self.start_date_calendar.setSelectedDate(QDate.currentDate())
        self.start_date_calendar.clicked.connect(self.minimum_end_date)
        self.calendar_layout.addWidget(self.start_date_calendar)
        self.start_date_calendar.hide()

        # End date prompt
        self.end_date_label = QLabel("Enter End Date")
        self.calendar_layout.addWidget(self.end_date_label)
        self.end_date_label.hide()

        # Calendar where user can enter end date
        self.end_date_calendar = QCalendarWidget()
        self.end_date_calendar.setMinimumDate(QDate.currentDate())
        self.end_date_calendar.setSelectedDate(QDate.currentDate().addDays(1))
        self.calendar_layout.addWidget(self.end_date_calendar)
        self.end_date_calendar.hide()

        # Filter button to only show cars available for the start and end date
        self.filter_button = QPushButton("Filter Cars")
        self.filter_button.clicked.connect(self.filter)
        self.calendar_layout.addWidget(self.filter_button)
        self.filter_button.hide()

        self.layout.addLayout(self.calendar_layout, 1, 2)

    def sign_up_window(self):
        self.setDisabled(True)
        self.sign_up_window.show()

    # TODO: See if you can refactor settings_window() and car_mgmt_window() into something simpler
    # Function might be similar to log_in_window or sign_up window above
    def settings_window(self):
        if self.settings_window_instance is None or not self.settings_window_instance.isVisible():
            self.settings_window_instance = SettingsWindow()
        self.settings_window_instance.show()

    def car_mgmt_window(self):
        if self.car_window_instance is None or not self.car_window_instance.isVisible():
            self.car_window_instance = CarWindow()
        self.car_window_instance.show()

    def login_window(self):
        self.setDisabled(True)
        self.login_window.show()

    def logout(self):
        self.account.logout()
        self.login_check()
        self.user_name_label.setText("Guest")

    def login_check(self):
        # checks if a user is logged in
        # if a user is not logged in the User = NONE
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
        self.guide_label.show()
        self.start_date_label.show()
        self.start_date_calendar.show()
        self.end_date_label.show()
        self.end_date_calendar.show()
        self.filter_button.show()

    def home_page(self):
        self.car_list.hide()
        self.guide_label.hide()
        self.start_date_label.hide()
        self.start_date_calendar.hide()
        self.end_date_label.hide()
        self.end_date_calendar.hide()
        self.filter_button.hide()
        self.welcome_label.show()

    def minimum_end_date(self):
        start_date = self.start_date_calendar.selectedDate()
        end_date = self.end_date_calendar.selectedDate()
        if start_date > end_date:
            self.end_date_calendar.setSelectedDate(start_date.addDays(1))
        self.end_date_calendar.setMinimumDate(start_date.addDays(1))

    def filter(self):
        start_date = self.start_date_calendar.selectedDate()
        end_date = self.end_date_calendar.selectedDate()
        rental_period = [start_date, end_date]

        self.guide_label.setText("Showing Cars Available from " + start_date.toString()
                                 + " to " + end_date.toString())
        self.car_list = self.cars.make_car_list(start_date, end_date, rental_period)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
