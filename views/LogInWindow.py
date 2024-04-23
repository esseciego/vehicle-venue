from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QGridLayout, QLabel,
                             QLineEdit, QApplication)

from views.SignUpWindow import SignUpWindow
from views.SignUpWindow import screen_size
from models.Accounts import Accounts

class LogInWindow(QWidget):
    #signal that is sent to Mainwindow so it can check if the user is logged in
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setRowMinimumHeight(2, 100)
        self.layout.setRowMinimumHeight(3, 50)
        self.layout.setRowMinimumHeight(4, 100)

        self.setWindowTitle("Log In")
        self.setLayout(self.layout)
        self.setFixedSize(screen_size / 2.0)

        # Sign up window instance
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.window_closed.connect(self.close_check)

        title = QLabel("User Login")
        self.layout.addWidget(title, 0, 1, Qt.AlignmentFlag.AlignHCenter)

        # Label that instructs user if login was successful
        self.confirmation_label = QLabel("Enter Username and Password")
        self.layout.addWidget(self.confirmation_label, 0, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        # Username label
        user_name = QLabel("Username:")
        user_name.setProperty("class", "normal")
        self.layout.addWidget(user_name, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 2, 1, 1, 2,)

        # Password Label
        user_password = QLabel("Password:")
        user_password.setProperty("class", "normal")
        self.layout.addWidget(user_password, 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 3, 1, 1, 2)

        # Sign up Button - connected to SignUpWindow
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up)
        self.layout.addWidget(sign_up_button, 4, 0)

        # Login Button - connected to LogInWindow
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        login_button.setDefault(True)
        self.layout.addWidget(login_button, 4, 2)

    # Shows the sign up window, hides the login window
    def sign_up(self):
        #When sign up Button Pressed, send user to Sign Up window
        self.sign_up_window.show()
        self.password.clear()
        self.username.clear()
        self.hide()

    # Connects to the accounts backend, checks if login information is valid,
    # if so logs them in, if not say it was invalid
    def login(self):
        #Checks with the database whether account exists and user can sign in
        account = Accounts()
        error_log = account.login(self.username.text(), self.password.text())
        if(account.operation_success(error_log)):
            self.confirmation_label.setText("Login Successful")
        else:
            self.confirmation_label.setText("Invalid Username or Password. Please try again")

    # When signup window is closed it sends a signal to here to close login window
    def close_check(self):
        self.close()

    # when window is closed, main window will check if user is logged in
    # will replace login button with logout button
    def closeEvent(self, event):
        self.password.clear()
        self.username.clear()
        self.window_closed.emit()
        event.accept()
