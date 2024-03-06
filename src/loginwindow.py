import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://tears_user:sobbing.emoji@carrental.fiinqnj.mongodb.net/?retryWrites=true&w=majority&appName=CarRental"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(10)

        self.setWindowTitle("User Sign Up")
        self.setLayout(self.layout)
        self.resize(800, 600)

        # Username label
        user_name = QLabel("Username:")
        user_name.setProperty("class", "normal")
        self.layout.addWidget(user_name, 1, 0)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 1, 1, 1, 2)

        # Password Label
        user_password = QLabel("Password")
        user_password.setProperty("class", "normal")
        self.layout.addWidget(user_password, 2, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 2, 1, 1, 2)

        # Password Label
        user_password = QLabel("Email Address")
        user_password.setProperty("class", "normal")
        self.layout.addWidget(user_password, 3, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 3, 1, 1, 2)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(100)

        # Sign Up button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.signUpWindow)
        self.layout.addWidget(sign_up_button, 4, 0)

        self.loginWindow()

    def loginWindow(self):
            title = QLabel("User Login")
            title.setProperty("class", "heading")
            self.layout.addWidget(title, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)

            self.setWindowTitle("User Login")
            self.setLayout(self.layout)
            self.resize(800, 600)

            #Username label
            user_name = QLabel("Username:")
            user_name.setProperty("class", "normal")
            self.layout.addWidget(user_name, 1, 0)
            self.username = QLineEdit()
            self.layout.addWidget(self.username, 1, 1, 1, 2)

            # Password Label
            user_password = QLabel("Password")
            user_password.setProperty("class", "normal")
            self.layout.addWidget(user_password, 2, 0)
            self.password = QLineEdit()
            self.layout.addWidget(self.password, 2, 1, 1, 2)

            self.confirmation_label = QLabel("Enter Username and Password")
            self.confirmation_label.setProperty("class", "heading")
            self.layout.addWidget(self.confirmation_label, 0, 0, 3, 0, Qt.AlignmentFlag.AlignCenter)

            #Login Button
            button2 = QPushButton("Login")
            button2.clicked.connect(self.login)
            self.layout.addWidget(button2, 4, 2)

    def signUpWindow(self):
        self.window2 = SignUpWindow()
        self.window2.show()
        self.hide()

    def login(self):
        if self.username.text() == "Username" and self.password.text() == "Password":
            self.confirmation_label.setText("Login Successful")
            print("Login Successful")
            #goes to another window
        else:
            self.confirmation_label.setText("Invalid Username or Password. Please try again")
            print("Invalid Username or Password")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

