import sys
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit)
from models.Accounts import Accounts


class SignUpWindow(QWidget):
    # signal that is sent to MainWindow so it can check if the user is logged in
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(50)

        self.setWindowTitle("Sign Up")
        self.setLayout(self.layout)
        self.setFixedSize(screen_size / 1.75)

        # Background Color
        self.setStyleSheet("background-color: #ffe0c2")

        # "Please Enter..." text
        self.title = QLabel("Please enter your information below.")
        self.title.setProperty("class", "heading")
        self.title.setStyleSheet("font-weight: bold;"
                                 "font-family: Tahoma;"
                                 "font-size: 32px")
        self.layout.addWidget(self.title, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)

        # Username label + text
        user_username = QLabel("Username:")
        user_username.setProperty("class", "normal")
        user_username.setStyleSheet("font-family: Tahoma;"
                                    "font-size: 16px")
        self.layout.addWidget(user_username, 1, 0)
        self.username = QLineEdit()
        self.username.setStyleSheet("background-color: white")
        self.layout.addWidget(self.username, 1, 1, 1, 2)

        # Password label + text
        user_password = QLabel("Password:")
        user_password.setProperty("class", "normal")
        user_password.setStyleSheet("font-family: Tahoma;"
                                    "font-size: 16px")
        self.layout.addWidget(user_password, 2, 0)
        self.password = QLineEdit()
        self.password.setStyleSheet("background-color: white")
        self.layout.addWidget(self.password, 2, 1, 1, 2)

        # Email label + text
        user_email = QLabel("Email Address:")
        user_email.setProperty("class", "normal")
        user_email.setStyleSheet("font-family: Tahoma;"
                                 "font-size: 16px")
        self.layout.addWidget(user_email, 3, 0)

        self.email = QLineEdit()
        self.email.setStyleSheet("background-color: white")
        self.layout.addWidget(self.email, 3, 1, 1, 2)

        # City label + text
        user_city = QLabel("City: ")
        user_city.setProperty("class", "normal")
        user_city.setStyleSheet("font-family: Tahoma;"
                                "font-size: 16px")
        self.layout.addWidget(user_city, 4, 0)
        self.city = QLineEdit()
        self.city.setStyleSheet("background-color: white")
        self.layout.addWidget(self.city, 4, 1, 1, 2)

        # "Sign up" button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up)
        sign_up_button.setStyleSheet("background-color: #6eb6ff;"
                                     "color: black;"
                                     "font-weight: bold;"
                                     "font-family: Tahoma;")
        self.layout.addWidget(sign_up_button, 5, 0, 1, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

    # Checks if account information is valid to make account
    # If not then it updates the title to show the user what went wrong
    def sign_up(self):
        account = Accounts()
        error_log = account.add_account(self.username.text(), self.password.text(), self.email.text(), "Client", self.city.text())
        if account.operation_success(error_log):
            self.title.setText("Account Created Successfully")
            error_log = account.login(self.username.text(), self.password.text())
        else:
            if not error_log['username-valid']:
                self.title.setText("Username must be between 6-16 characters AND only uses alphanumeric characters")

            elif not error_log['username-unique']:
                self.title.setText("Username is already taken")

            elif not error_log['password-valid']:
                self.title.setText("Password must be between 8-32 characters AND contains at least 1 number")

            elif not error_log['email-entered']:
                self.title.setText("Please enter a valid email")

            elif not error_log['city-entered']:
                self.title.setText("Please enter a valid city")

    # When window is closed, main window will check if user is logged in
    # Will replace login button with logout button
    def closeEvent(self, event):
        self.password.clear()
        self.username.clear()
        self.email.clear()
        self.window_closed.emit()
        event.accept()


app = QApplication(sys.argv)
screen = app.primaryScreen()
screen_size = screen.size()
