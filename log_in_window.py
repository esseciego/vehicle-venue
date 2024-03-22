import sys
from sign_up_window import SignUpWindow
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit)
class LogInWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(100)

        self.setWindowTitle("Log In")
        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.signUpWindow)
        self.layout.addWidget(sign_up_button, 4, 0)

        title = QLabel("User Login")
        title.setProperty("class", "heading")
        self.layout.addWidget(title, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)

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
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        self.layout.addWidget(login_button, 4, 2)

    def signUpWindow(self):
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.show()
        self.close()

    def login(self):
        if self.username.text() == "Username" and self.password.text() == "Password":
            self.confirmation_label.setText("Login Successful")
            self.close()
        else:
            self.confirmation_label.setText("Invalid Username or Password. Please try again")

app = QApplication(sys.argv)
screen = app.primaryScreen()
screen_size = screen.size()