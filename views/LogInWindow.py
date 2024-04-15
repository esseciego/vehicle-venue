import sys
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit)

from views.SignUpWindow import SignUpWindow
from views.SignUpWindow import screen_size
from models.Accounts import Accounts


class LogInWindow(QWidget):
    # signal that is sent to Mainwindow so it can check if the user is logged in
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(100)

        self.setWindowTitle("Log In")
        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

        self.setStyleSheet("background-color: #ffe0c2")

        # "User Login" text
        title = QLabel("User Login")
        title.setProperty("class", "heading")
        title.setStyleSheet("font-weight: bold;"
                            "font-family: Tahoma;"
                            "font-size: 32px")
        self.layout.addWidget(title, 0, 0, 1, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        # "Username:" text
        user_name = QLabel("Username:")
        user_name.setProperty("class", "normal")
        user_name.setStyleSheet("font-family: Tahoma;"
                                "font-size: 14px")
        self.layout.addWidget(user_name, 1, 0)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 1, 1, 1, 2)

        # "Password:" text
        user_password = QLabel("Password:")
        user_password.setProperty("class", "normal")
        user_password.setStyleSheet("font-family: Tahoma;"
                                    "font-size: 14px")
        self.layout.addWidget(user_password, 2, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 2, 1, 1, 2)

        # "Enter Username and Password." text (also tells user if their info was VALID or INVALID)
        self.confirmation_label = QLabel("Please enter your Username and Password.")
        self.confirmation_label.setProperty("class", "heading")
        self.confirmation_label.setStyleSheet("color: #bd6106;"
                                              "font-family: Tahoma;"
                                              "font-size: 14px")
        self.layout.addWidget(self.confirmation_label, 0, 0, 3, 0, Qt.AlignmentFlag.AlignCenter)

        # "Sign up" button - connected to SignUpWindow
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        sign_up_button.setStyleSheet("background-color: #6eb6ff;"
                                     "color: black;"
                                     "font-weight: bold;"
                                     "font-family: Tahoma;")
        self.layout.addWidget(sign_up_button, 4, 0)

        # "Log In" button - connected to LogInWindow
        login_button = QPushButton("Log In")
        login_button.clicked.connect(self.login)
        login_button.setStyleSheet("background-color: #fa9352;"
                                   "color: black;"
                                   "font-weight: bold;"
                                   "font-family: Tahoma;")
        self.layout.addWidget(login_button, 4, 2)

    def sign_up_window(self):
        # When sign up Button Pressed, send user to Sign Up window
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.show()
        self.password.clear()
        self.username.clear()
        self.close()

    def login(self):
        # Checks with the database whether account exists and user can sign in
        account = Accounts()
        error_log = account.login(self.username.text(), self.password.text())
        if account.operation_success(error_log):
            self.confirmation_label.setText("Login Successful")
        else:
            self.confirmation_label.setText("Invalid Username or Password! Please try again.")

    def closeEvent(self, event):
        # when window is closed, main window will check if user is logged in
        # will replace login button with logout button
        self.password.clear()
        self.username.clear()
        self.window_closed.emit()
        event.accept()
