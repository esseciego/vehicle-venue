from PyQt6.QtCore import (Qt, pyqtSignal, QDate)
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout,
                             QCalendarWidget, QLabel)

from views.SignUpWindow import screen_size
from views.ClientLogInWindow import ClientLogInWindow
from views.LogInWindow import LogInWindow
from models.Rentals import Rentals
from helpers.EnvVariables import EnvVariables


class SpecificCarWindow(QWidget):
    # When a user logs in in the car window, send a signal to mainwindow to update the username
    username_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.rentals = Rentals()

        self.setWindowTitle("Reserve a Car")

        self.layout = QHBoxLayout()
        self.layout.setSpacing(20)
        self.layoutV = QVBoxLayout()
        self.calendar_layout = QVBoxLayout()

        # the car image png
        self.car_pixmap = QPixmap()

        # where the car image is stored
        self.car_image = QLabel()
        self.layoutV.addWidget(self.car_image)

        # car data label
        self.data_label = QLabel()
        self.data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutV.addWidget(self.data_label, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addLayout(self.layoutV)

        # LoginWindow window
        self.login_window = LogInWindow()
        self.login_window.window_closed.connect(self.login_check)

        # LoginWindow for when an employee is logging in for a client
        self.client_login_window = ClientLogInWindow()
        self.client_login_window.window_closed.connect(self.login_check)

        # variables used to make a reservation
        self.license_plate = ""
        self.rental_dates = []

        # Guide prompt
        self.guide_label = QLabel("Choose a START and END date")
        self.guide_label.setStyleSheet("color: black;"
                                       "font-weight: bold;"
                                       "font-family: Tahoma;"
                                       "font-size: 20px")
        self.calendar_layout.addWidget(self.guide_label)

        # Enter start date prompt
        self.start_date_label = QLabel("Enter Start Date:")
        self.start_date_label.setStyleSheet("color: #f5840c;"
                                            "font-family: Tahoma;"
                                            "font-style: italic;"
                                            "font-weight: bold")
        self.calendar_layout.addWidget(self.start_date_label)

        # Calendar where user can enter start date
        self.start_date_calendar = QCalendarWidget()
        self.start_date_calendar.setMinimumDate(QDate.currentDate())
        self.start_date_calendar.setSelectedDate(QDate.currentDate())
        self.start_date_calendar.clicked.connect(self.minimum_end_date)
        self.start_date_calendar.setStyleSheet("background-color: #d9e5ff")
        self.calendar_layout.addWidget(self.start_date_calendar)

        # End date prompt
        self.end_date_label = QLabel("Enter End Date:")
        self.end_date_label.setStyleSheet("color: #f5840c;"
                                          "font-family: Tahoma;"
                                          "font-style: italic;"
                                          "font-weight: bold")
        self.calendar_layout.addWidget(self.end_date_label)

        # Calendar where user can enter end date
        self.end_date_calendar = QCalendarWidget()
        self.end_date_calendar.setMinimumDate(QDate.currentDate())
        self.end_date_calendar.setSelectedDate(QDate.currentDate().addDays(1))
        self.end_date_calendar.setStyleSheet("background-color: #d9e5ff")
        self.calendar_layout.addWidget(self.end_date_calendar)

        # Make reservation button
        self.reserve_button = QPushButton("Make Reservation")
        self.reserve_button.clicked.connect(self.reserve)
        self.reserve_button.setStyleSheet("background-color: #6eb6ff;"
                                          "color: black;"
                                          "font-weight: bold;"
                                          "font-family: Tahoma;")
        self.calendar_layout.addWidget(self.reserve_button)

        self.layout.addLayout(self.calendar_layout)

        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

        # Background color
        self.setStyleSheet("background-color: #ffe0c2")

    # set the car image based on what kind of car it is
    def set_pixmap(self, type):
        if type == "SUV":
            self.car_pixmap = QPixmap('ui/images/suv_icon.png')
        elif type == "Van":
            self.car_pixmap = QPixmap('ui/images/van_icon.png')
        else:
            self.car_pixmap = QPixmap('ui/images/sedan_icon.png')

        self.car_pixmap = self.car_pixmap.scaled(int(screen_size.width() / 5), int(screen_size.width() / 5))
        self.car_image.setPixmap(self.car_pixmap)
        self.car_image.setFixedSize(int(screen_size.width() / 5), int(screen_size.width() / 5))

    # sets the dates on the calendar based on what dates were selected in the car list window
    def set_dates(self, start_date, end_date):
        self.start_date_calendar.setSelectedDate(start_date)
        self.end_date_calendar.setSelectedDate(end_date)

    # when a start date is chosen, set the minimum end date to be that date plus one,
    # avoids having a negative rental period
    def minimum_end_date(self):
        start_date = self.start_date_calendar.selectedDate()
        end_date = self.end_date_calendar.selectedDate()
        if start_date > end_date:
            self.end_date_calendar.setSelectedDate(start_date.addDays(1))
        self.end_date_calendar.setMinimumDate(start_date.addDays(1))

    # when make reservation button is pressed, checks if a user is a client or admin/employee
    # admin/employees have to login/create a user account to make a reservation
    # clients must be logged into an account to create a reservation
    def reserve(self):
        env_vars = EnvVariables()
        if env_vars.get_user() == "NONE":
            self.login_window.confirmation_label.setText("You must sign into an account to make a reservation")
            self.login_window.show()
            self.setDisabled(True)
        elif env_vars.get_role() == "Employee" or env_vars.get_role() == "Admin":
            self.client_login_window.show()
            self.setDisabled(True)
        else:
            self.make_reservation(env_vars.get_user())

    # uses Rentals backend to check if a reservation is valid and make one
    def make_reservation(self, username):
        start_date = self.start_date_calendar.selectedDate()
        end_date = self.end_date_calendar.selectedDate()
        if self.check_available(start_date, end_date):
            error_log = self.rentals.create_rental(username, self.license_plate,
                                                   start_date.toString(Qt.DateFormat.ISODate),
                                                   end_date.toString(Qt.DateFormat.ISODate))
            if self.rentals.operation_success(error_log):
                self.guide_label.setText("Reservation Created Successfully!")
            else:
                self.guide_label.setText("Something went wrong!")
        else:
            self.guide_label.setText("Car not available during those dates, please select another rental period")

    # checks if the car is available during the rental period selected
    def check_available(self, start_date, end_date):
        for date in self.rental_dates:
            start_rental_date = QDate.fromString(date[0], Qt.DateFormat.ISODate)
            end_rental_date = QDate.fromString(date[1], Qt.DateFormat.ISODate)

            if start_date <= start_rental_date <= end_date:
                return False
            if start_date <= end_rental_date <= end_date:
                return False

            if start_rental_date <= start_date <= end_rental_date:
                return False
            if start_rental_date <= end_date <= end_rental_date:
                return False

        return True

    # Checks for if a client or admin/employee logs in,
    def login_check(self):
        # checks if a user is logged in
        # if a user is not logged in the User = NONE
        self.setDisabled(False)
        env_vars = EnvVariables()
        if env_vars.get_user() == "NONE":
            return
        elif env_vars.get_role() == "Employee" or env_vars.get_role() == "Admin":
            self.make_reservation(self.client_login_window.client_username)
        else:
            self.username_signal.emit()
            self.make_reservation(env_vars.get_user())

    # resets the guide label when the window is closed
    def closeEvent(self, event):
        self.guide_label.setText("Choose Start and End Dates of Desired Rental Period")
        event.accept()
