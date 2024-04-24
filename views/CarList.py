from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (Qt, pyqtSignal, QDate)
from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QGridLayout, QScrollArea)

from views.SignUpWindow import screen_size
from views.SpecificCarWindow import SpecificCarWindow
from models.Cars import Cars

class CarList(QWidget):
    # Signal that is sent to Mainwindow for when a user is logged in or creates an account in the car window
    # MainWindow will update the users username
    username_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.window_layout = SpecificCarWindow()
        self.window_layout.username_signal.connect(self.username_check)

        # Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)  # Scroll Area which contains the widgets
        self.scroll.setFixedSize(int(screen_size.width() * .50), int(screen_size.height() * .75))

        self.cars = Cars()

    #Populate the scroll area with the car objects
    def make_car_list(self, location, start_date=QDate.currentDate(), end_date=QDate.currentDate().addDays(1), rental_period=None):
        if rental_period is None:
            rental_period = []
        print(location)
        list_layout = QGridLayout()  # Layout of the cars
        car_list = QWidget()  # Widget that contains the collection of the cars
        if location != "":
            self.list_of_cars = self.cars.get_cars_by_location(location)
            j = 0
            for i in range(len(self.list_of_cars)):
                if self.check_available_car(i, rental_period):
                    car_object = self.make_car_object(i)
                    list_layout.addWidget(car_object, int(j / 3), j % 3)
                    j += 1
        else:
            self.list_of_cars = self.cars.get_all_cars()
            j = 0
            for i in range(len(self.list_of_cars)):
                if self.check_available_car(i, rental_period):
                    car_object = self.make_car_object(i)
                    list_layout.addWidget(car_object, int(j / 3), j % 3)
                    j += 1

        car_list.setLayout(list_layout)
        self.scroll.setWidget(car_list)
        self.window_layout.set_dates(start_date, end_date)

        return self.scroll

    # Checks if a cars is available during a certain rental period
    def check_available_car(self, i, rental_period):
        if rental_period:
            for date in self.list_of_cars[i]['rental_dates']:
                start_date = QDate.fromString(date[0], Qt.DateFormat.ISODate)
                end_date = QDate.fromString(date[1], Qt.DateFormat.ISODate)

                if rental_period[0] <= start_date <= rental_period[1]:
                    return False
                if rental_period[0] <= end_date <= rental_period[1]:
                    return False

                if start_date <= rental_period[0] <= end_date:
                    return False
                if start_date <= rental_period[1] <= end_date:
                    return False

        return True

    # Makes the button with the car image based on what type of car it is
    def make_car_object(self, i):
        car_button = QPushButton('')
        if self.list_of_cars[i]['type'] == "SUV":
            icon = QtGui.QIcon('ui/images/suv_icon.png')
        elif self.list_of_cars[i]['type'] == "Van":
            icon = QtGui.QIcon('ui/images/van_icon.png')
        else:
            icon = QtGui.QIcon('ui/images/sedan_icon.png')
        car_button.setIcon(icon)
        car_button.setIconSize(QtCore.QSize(200, 200))
        car_button.setFixedSize(200, 200)
        car_button.clicked.connect(lambda: self.car_window(i))

        return car_button

    # Sets the car window when a button is clicked for a certain car
    def car_window(self, i):
        self.window_layout.set_pixmap(self.list_of_cars[i]['type'])

        self.window_layout.license_plate = self.list_of_cars[i]['license_plate']
        self.window_layout.rental_dates = self.list_of_cars[i]['rental_dates']
        self.window_layout.data_label.setText("License plate number: " + self.list_of_cars[i]['license_plate']
                                                       + "\n\nType: " + self.list_of_cars[i]['type']
                                                       + "\n\nLocation: " + self.list_of_cars[i]['curr_rental_location']
                                                       + "\n\nMileage: " + str(self.list_of_cars[i]['mileage'])
                                                       + "\n\nCost Per Day: " + str(self.list_of_cars[i]['cost_per_day'])
                                                       + "\n\nCost Per Mile: " + str(self.list_of_cars[i]['cost_per_mile']))
        self.window_layout.show()

    # when a user logs in in the car window, send a signal to mainwindow
    def username_check(self):
        self.username_signal.emit()
