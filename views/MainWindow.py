import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (Qt, pyqtSignal, QDate)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QScrollArea, QCalendarWidget, QVBoxLayout)


from views.LogInWindow import LogInWindow
from views.SignUpWindow import SignUpWindow
from views.SignUpWindow import screen_size
from views.CarMgmtWindow import CarMgmtWindow
from views.CarList import CarList
from views.AccountMgmtWindow import AccountMgmtWindow
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
        self.layout.setColumnMinimumWidth(1, int(screen_size.width() * .61))
        self.layout.setColumnMinimumWidth(2, int(screen_size.width() * .2))
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(25, 30, 25, 50)

        self.calendar_layout = QVBoxLayout()

        self.setWindowTitle("Home Page")
        self.setLayout(self.layout)

        self.setFixedSize(int(screen_size.width()), int(screen_size.height() * .92))

        self.account = Accounts()

        self.user_location = ""

        # Car collection list
        self.cars = CarList()
        self.car_list = self.cars.make_car_list(self.user_location)
        self.layout.addWidget(self.car_list, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.cars.username_signal.connect(self.login_check)
        self.car_list.hide()

        # Welcome text
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

        # Car List tab
        self.collection_tab = QPushButton("Car Collection")
        self.collection_tab.setFlat(True)
        self.collection_tab.clicked.connect(self.car_collection)
        self.layout.addWidget(self.collection_tab, 0, 0, Qt.AlignmentFlag.AlignRight)

        # Home Page tab
        self.home_tab = QPushButton("Home")
        self.home_tab.setFlat(True)
        self.home_tab.clicked.connect(self.home_page)
        self.layout.addWidget(self.home_tab, 0, 0, Qt.AlignmentFlag.AlignLeft)

        #  Manage Accounts button
        self.accounts_mgmt_button = QPushButton("Manage Accounts")
        self.accounts_mgmt_button.setFlat(True)
        self.accounts_mgmt_button.clicked.connect(self.account_mgmt_window)
        self.layout.addWidget(self.accounts_mgmt_button, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.account_mgmt_window_instance = None

        # Manage Cars button
        self.car_mgmt_window_button = QPushButton("Manage Cars")
        self.car_mgmt_window_button.setFlat(True)
        self.car_mgmt_window_button.clicked.connect(self.car_mgmt_window)
        self.layout.addWidget(self.car_mgmt_window_button, 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.car_mgmt_window_instance = None  # Keep a reference to the car window

        # Sign Up button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        self.layout.addWidget(sign_up_button, 0, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.window_closed.connect(self.login_check)

        # Log In button
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.login_window)
        self.layout.addWidget(self.login_button, 0, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.login_window = LogInWindow()
        self.login_window.window_closed.connect(self.login_check)

        # Log Out button
        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button, 0, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.logout_button.hide()

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

    #open up the account edit window
    def account_mgmt_window(self):
        if self.account_mgmt_window_instance is None or not self.account_mgmt_window_instance.isVisible():
            self.account_mgmt_window_instance = AccountMgmtWindow()
        self.account_mgmt_window_instance.show()

    #open up the car edit window
    def car_mgmt_window(self):
        self.car_mgmt_window_instance = CarMgmtWindow()
        self.car_mgmt_window_instance.show()

    #open up the sign up window
    def sign_up_window(self):
        self.setDisabled(True)
        self.sign_up_window.show()

    #open up the login window
    def login_window(self):
        self.setDisabled(True)
        self.login_window.show()

    #logs user out
    def logout(self):
        self.account.logout()
        self.login_check()
        self.user_name_label.setText("Guest")

    #checks if the user has logged in
    #If yes as a client, replaces login button with log out button
    #If yes as an employee or admin, grants access and updates cars to only those at the location that they work at
    def login_check(self):
        # checks if a user is logged in
        # if a user is not logged in the User = NONE
        env_vars = EnvVariables()
        if env_vars.get_user() == "NONE":
            self.login_button.show()
            self.logout_button.hide()
            self.user_location = ""
            self.update_car_list()
        else:
            if env_vars.get_role() == "Employee" or env_vars.get_role() == "Admin":
                self.user_location = env_vars.get_city()
                self.update_car_list()
            else:
                self.user_location = ""
            self.logout_button.show()
            self.login_button.hide()
            self.user_name_label.setText(env_vars.get_user())
        self.setDisabled(False)

    #shows the car list and calendars
    def car_collection(self):
        self.welcome_label.hide()
        self.car_list.show()
        self.guide_label.show()
        self.start_date_label.show()
        self.start_date_calendar.show()
        self.end_date_label.show()
        self.end_date_calendar.show()
        self.filter_button.show()

    #Removes the car list and calendars
    def home_page(self):
        self.car_list.hide()
        self.guide_label.hide()
        self.start_date_label.hide()
        self.start_date_calendar.hide()
        self.end_date_label.hide()
        self.end_date_calendar.hide()
        self.filter_button.hide()
        self.welcome_label.show()

    #When a start date is selected, set the minumum end date to that date plus 1
    def minimum_end_date(self):
        start_date = self.start_date_calendar.selectedDate()
        end_date = self.end_date_calendar.selectedDate()
        if start_date > end_date:
            self.end_date_calendar.setSelectedDate(start_date.addDays(1))
        self.end_date_calendar.setMinimumDate(start_date.addDays(1))

    #When the filter button is pressed, it gets the dates selected from the calendars and sends them to CarList
    #where the car list is then made only with cars that are available during the rental period
    def filter(self):
        start_date = self.start_date_calendar.selectedDate()
        end_date = self.end_date_calendar.selectedDate()
        rental_period = [start_date, end_date]

        self.guide_label.setText("Showing Cars Available from " + start_date.toString()
                                 + " to " + end_date.toString())

        self.update_car_list(start_date, end_date, rental_period)

    #updates car list with the new paramaters
    def update_car_list(self, start_date=QDate.currentDate(), end_date=QDate.currentDate().addDays(1), rental_period=None):
        if rental_period is NOne:
            rental_period = []
        self.car_list = self.cars.make_car_list(self.user_location, start_date, end_date, rental_period)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
