import sys
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit)

from views.SignUpWindow import SignUpWindow
from views.SignUpWindow import screen_size
from models.Accounts import Accounts


class LogInWindow(QWidget):
    # Signal that is sent to MainWindow to check if the user is logged in
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

        # User login label
        title = QLabel("User Login")
        self.layout.addWidget(title, 0, 1, Qt.AlignmentFlag.AlignHCenter)

        # Confirmation label
        # Informs user if login was successful
        self.confirmation_label = QLabel("Enter Username and Password")
        self.layout.addWidget(self.confirmation_label, 0, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        # Username label
        user_name = QLabel("Username:")
        user_name.setProperty("class", "normal")
        self.layout.addWidget(user_name, 2, 0, Qt.AlignmentFlag.AlignLeft)

        self.username = QLineEdit()
        self.layout.addWidget(self.username, 2, 1, 1, 2,)

        # Password label
        user_password = QLabel("Password:")
        user_password.setProperty("class", "normal")
        self.layout.addWidget(user_password, 3, 0, Qt.AlignmentFlag.AlignLeft)

        self.password = QLineEdit()
        self.layout.addWidget(self.password, 3, 1, 1, 2)

        # SignUp button - connected to SignUpWindow
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        self.layout.addWidget(sign_up_button, 4, 0)

        # Login button - connected to LogInWindow
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
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
