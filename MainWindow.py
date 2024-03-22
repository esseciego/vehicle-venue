import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit)

#Basically the home page just a stand in
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(100)

        self.setWindowTitle("Home Page")
        self.setLayout(self.layout)
        self.resize(screen_size)

        #Welcomes to home page
        welcome_label = QLabel("Welcome to the Car Rental Site")
        welcome_label.setProperty("class", "heading")
        self.layout.addWidget(welcome_label, 0, 0, 3, 0, Qt.AlignmentFlag.AlignCenter)

        # Sign Up button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up_window)
        self.layout.addWidget(sign_up_button, 0, 3)

        # Log In button
        log_in_button = QPushButton("Log In")
        log_in_button.clicked.connect(self.log_in_window)
        self.layout.addWidget(log_in_button, 0, 4)

    def log_in_window(self):
        self.log_in_window = LogInWindow()
        self.log_in_window.show()

    def sign_up_window(self):
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.show()

#Sign up window just a stand in
class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(100)

        self.setWindowTitle("Log In")
        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

        # First Name Label
        user_name_first = QLabel("First Name")
        user_name_first.setProperty("class", "normal")
        self.layout.addWidget(user_name_first, 0, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 0, 1, 1, 2)

        # Last Name Label
        user_name_last = QLabel("Last Name")
        user_name_last.setProperty("class", "normal")
        self.layout.addWidget(user_name_last, 1, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 1, 1, 1, 2)

        # Username label
        user_name = QLabel("Username:")
        user_name.setProperty("class", "normal")
        self.layout.addWidget(user_name, 2, 0)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 2, 1, 1, 2)

        # Password Label
        user_name_first = QLabel("Password")
        user_name_first.setProperty("class", "normal")
        self.layout.addWidget(user_name_first, 3, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 3, 1, 1, 2)

        # Email Label
        user_name_first = QLabel("Email Address")
        user_name_first.setProperty("class", "normal")
        self.layout.addWidget(user_name_first, 4, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 4, 1, 1, 2)

#User Log in window
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
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            self.confirmation_label.setText("Invalid Username or Password. Please try again")

app = QApplication(sys.argv)
screen = app.primaryScreen()
screen_size = screen.size()
window = MainWindow()
window.show()
app.exec()