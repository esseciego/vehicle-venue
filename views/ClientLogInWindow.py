from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QGridLayout, QLabel,
                             QLineEdit)

from views.ClientSignUpWindow import ClientSignUpWindow
from views.SignUpWindow import screen_size
from models.Accounts import Accounts


class ClientLogInWindow(QWidget):
    # signal that is sent to MainWindow so it can check if the user is logged in
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setRowMinimumHeight(2, 100)
        self.layout.setRowMinimumHeight(3, 50)
        self.layout.setRowMinimumHeight(4, 100)

        self.setWindowTitle("Log In")
        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

        # Background Color
        self.setStyleSheet("background-color: #cce4fc")

        self.client_sign_up_window = ClientSignUpWindow()
        self.client_sign_up_window.window_closed.connect(self.close_check)
        self.client_username = ""

        title = QLabel("Client Login")
        title.setStyleSheet("font-weight: bold;"
                            "font-family: Tahoma;"
                            "font-size: 32px")
        self.layout.addWidget(title, 0, 1, Qt.AlignmentFlag.AlignHCenter)

        # "Enter the..." (Also lets employee/admin know if it was successful)
        self.confirmation_label = QLabel("Enter the Client's Details below:")
        self.confirmation_label.setStyleSheet("color: #bd6106;"
                                              "font-family: Tahoma;"
                                              "font-size: 14px")
        self.layout.addWidget(self.confirmation_label, 0, 1,
                              Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        # "Username:" text
        user_name = QLabel("Username:")
        user_name.setProperty("class", "normal")
        user_name.setStyleSheet("font-family: Tahoma;"
                                "font-size: 14px")
        self.layout.addWidget(user_name, 2, 0, Qt.AlignmentFlag.AlignLeft)

        self.username = QLineEdit()
        self.username.setStyleSheet("background-color: white")
        self.layout.addWidget(self.username, 2, 1, 1, 2, )

        # "Password:" text
        user_password = QLabel("Password:")
        user_password.setProperty("class", "normal")
        user_password.setStyleSheet("font-family: Tahoma;"
                                    "font-size: 14px")
        self.layout.addWidget(user_password, 3, 0, Qt.AlignmentFlag.AlignLeft)

        self.password = QLineEdit()
        self.password.setStyleSheet("background-color: white")
        self.layout.addWidget(self.password, 3, 1, 1, 2)

        # "Sign Up" button (connected to SignUpWindow)
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up)
        sign_up_button.setStyleSheet("background-color: #fa9352;"
                                     "color: black;"
                                     "font-weight: bold;"
                                     "font-family: Tahoma;")
        self.layout.addWidget(sign_up_button, 4, 0)

        # "Login" Button (connected to LogInWindow)
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        login_button.setDefault(True)
        login_button.setStyleSheet("background-color: #6eb6ff;"
                                   "color: black;"
                                   "font-weight: bold;"
                                   "font-family: Tahoma;")
        self.layout.addWidget(login_button, 4, 2)

    def sign_up(self):
        # When sign up Button Pressed, send user to Sign Up window
        self.client_sign_up_window.show()
        self.password.clear()
        self.username.clear()
        self.hide()

    def login(self):
        # Checks with the database whether account exists and user can sign in
        account = Accounts()
        error_log = account.validate_login(self.username.text(), self.password.text())
        if (account.operation_success(error_log)):
            self.confirmation_label.setText("Login Successful")
            self.client_sign_up_window.client_username = self.username.text()
        else:
            self.confirmation_label.setText("Invalid Username or Password. Please try again")

    def close_check(self):
        self.close()

    def closeEvent(self, event):
        # when window is closed, main window will check if user is logged in
        # will replace login button with logout button
        self.client_username = self.client_sign_up_window.client_username
        self.password.clear()
        self.username.clear()
        self.window_closed.emit()
        event.accept()
