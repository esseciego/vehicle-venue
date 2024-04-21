import sys
from PyQt6.QtCore import (Qt, pyqtSignal, QDate)
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QCalendarWidget)

from views.SignUpWindow import screen_size
from views.LogInWindow import LogInWindow
from models.Rentals import Rentals
from helpers.EnvVariables import EnvVariables

class SpecificCarWindow(QWidget):
    username_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.rentals = Rentals()

        self.setWindowTitle("Reserve a Car")

        self.layout = QHBoxLayout()
        self.layout.setSpacing(20)
        self.layoutV = QVBoxLayout()
        self.calendar_layout = QVBoxLayout()

        self.car_pixmap = QPixmap()

        self.car_image = QLabel()
        self.layoutV.addWidget(self.car_image)

        self.data_label = QLabel()
        self.data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutV.addWidget(self.data_label, Qt.AlignmentFlag.AlignHCenter)

        self.layout.addLayout(self.layoutV)

        self.login_window = LogInWindow()
        self.login_window.window_closed.connect(self.login_check)

        self.license_plate = ""
        self.rental_dates = []

        # Guide prompt
        self.guide_label = QLabel("Choose a Start and End Dates of Desired Rental Period")
        self.calendar_layout.addWidget(self.guide_label)

        # Enter start date prompt
        self.start_date_label = QLabel("Enter Start Date")
        self.calendar_layout.addWidget(self.start_date_label)

        # Calendar where user can enter start date
        self.start_date_calendar = QCalendarWidget()
        self.start_date_calendar.setMinimumDate(QDate.currentDate())
        self.start_date_calendar.setSelectedDate(QDate.currentDate())
        self.start_date_calendar.clicked.connect(self.minimum_end_date)
        self.calendar_layout.addWidget(self.start_date_calendar)

        # End date prompt
        self.end_date_label = QLabel("Enter End Date")
        self.calendar_layout.addWidget(self.end_date_label)

        # Calendar where user can enter end date
        self.end_date_calendar = QCalendarWidget()
        self.end_date_calendar.setMinimumDate(QDate.currentDate())
        self.end_date_calendar.setSelectedDate(QDate.currentDate().addDays(1))
        self.calendar_layout.addWidget(self.end_date_calendar)

        #
        self.reserve_button = QPushButton("Make Reservation")
        self.reserve_button.clicked.connect(self.reserve)
        self.calendar_layout.addWidget(self.reserve_button)

        self.layout.addLayout(self.calendar_layout)

        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

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

    def set_dates(self, start_date, end_date):
        self.start_date_calendar.setSelectedDate(start_date)
        self.end_date_calendar.setSelectedDate(end_date)

    def minimum_end_date(self):
        start_date = self.start_date_calendar.selectedDate()
        end_date = self.end_date_calendar.selectedDate()
        if start_date > end_date:
            self.end_date_calendar.setSelectedDate(start_date.addDays(1))
        self.end_date_calendar.setMinimumDate(start_date.addDays(1))

    def reserve(self):
        env_vars = EnvVariables()

        if env_vars.get_user() == "NONE":
            self.login_window.confirmation_label.setText("You must sign into an account to make a reservation")
            self.login_window.show()
            self.setDisabled(True)
        else:
            self.make_reservation(env_vars.get_user())


    def make_reservation(self, username):
        start_date = self.start_date_calendar.selectedDate()
        end_date = self.end_date_calendar.selectedDate()
        if self.check_available(start_date, end_date):
            self.guide_label.setText("Reservation Created Successfully!")
            self.rentals.create_rental(username, self.license_plate,
                                       start_date.toString(Qt.DateFormat.ISODate),
                                       end_date.toString(Qt.DateFormat.ISODate))
        else:
            self.guide_label.setText("Car not available during those dates, please select another rental period")

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

    def login_check(self):
        # checks if a user is logged in
        # if a user is not logged in the User = NONE
        self.setDisabled(False)
        env_vars = EnvVariables()
        if env_vars.get_user() == "NONE":
            return
        else:
            self.username_signal.emit()
            self.make_reservation(env_vars.get_user())