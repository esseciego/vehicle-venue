from PyQt6.QtCore import (Qt, pyqtSignal, QDate)
from PyQt6.QtWidgets import (QWidget, QGridLayout,
                             QLabel, QScrollArea,
                             QHBoxLayout, QVBoxLayout, QPushButton)

from views.SignUpWindow import screen_size
from models.Rentals import Rentals

class RentalWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Rentals')

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

        # Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)  # Scroll Area which contains the widgets

        self.rentals = Rentals()

        self.layout.addWidget(self.make_rental_list())

        self.back_button = QPushButton('Back to main')
        self.back_button.clicked.connect(lambda: self.close())
        self.layout.addWidget(self.back_button)

    # Makes the list that shows all of the rentals
    def make_rental_list(self):
        list_layout = QVBoxLayout()  # Layout of the cars
        header_layout = QHBoxLayout()

        username_label = QLabel("Username")
        license_plates_label = QLabel("License Plate")
        rental_period_label = QLabel("Rental Period")

        header_layout.addWidget(username_label)
        header_layout.addWidget(license_plates_label)
        header_layout.addWidget(rental_period_label)

        list_layout.addLayout(header_layout)

        rental_list = QWidget()  # Widget that contains the collection of the cars
        all_rentals = self.rentals.get_all_rentals()

        for i in range(len(all_rentals)):
            rental_layout = QHBoxLayout()

            username = QLabel(all_rentals[i]['username'])
            license_plates = QLabel(all_rentals[i]['license_plate'])
            rental_period = QLabel(all_rentals[i]['start_rental_date'] + " - " + all_rentals[i]['end_rental_date'])

            rental_layout.addWidget(username)
            rental_layout.addWidget(license_plates)
            rental_layout.addWidget(rental_period)

            list_layout.addLayout(rental_layout)

        rental_list.setLayout(list_layout)
        self.scroll.setWidget(rental_list)

        return self.scroll

