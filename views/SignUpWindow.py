import sys
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel, QLineEdit)
from models.Accounts import Accounts


class SignUpWindow(QWidget):
    # signal that is sent to Mainwindow so it can check if the user is logged in
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(50)

        self.setWindowTitle("Sign Up")
        self.setLayout(self.layout)
        self.resize(screen_size / 2.0)

        self.title = QLabel("Please Enter User Information to Create Account")
        self.title.setProperty("class", "heading")
        self.layout.addWidget(self.title, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)

        # Username Label
        user_email = QLabel("Username")
        user_email.setProperty("class", "normal")
        self.layout.addWidget(user_email, 1, 0)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 1, 1, 1, 2)

        # Password Label
        user_password = QLabel("Password")
        user_password.setProperty("class", "normal")
        self.layout.addWidget(user_password, 2, 0)
        self.password = QLineEdit()
        self.layout.addWidget(self.password, 2, 1, 1, 2)

        # Email label
        user_email = QLabel("Email Address")
        user_email.setProperty("class", "normal")
        self.layout.addWidget(user_email, 3, 0)
        self.email = QLineEdit()
        self.layout.addWidget(self.email, 3, 1, 1, 2)

        # Sign up Button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.clicked.connect(self.sign_up)
        self.layout.addWidget(sign_up_button, 4, 0)

    def sign_up(self):
        #Checks if account information is valid to make account
        #If not then it updates the title to show the user what went wrong
        account = Accounts()
        error_log = account.add_account(self.username.text(), self.password.text(), self.email.text())
        if (account.operation_success(error_log)):
            self.title.setText("Account Created Successfully")
            error_log = account.login(self.username.text(), self.password.text())
        else:
            if error_log['username-valid'] == False:
                self.title.setText("Username must be between 6-16 characters AND only uses alphanumeric characters")

            elif error_log['username-unique'] == False:
                self.title.setText("Username is already taken")

            elif error_log['password-valid'] == False:
                self.title.setText("Password must be between 8-32 characters AND contains at least 1 number")

            elif error_log['email-entered'] == False:
                self.title.setText("Please enter a valid Email")

    def closeEvent(self, event):
        #when window is closed, main window will check if user is logged in
        #will replace login button with logout button
        self.password.clear()
        self.username.clear()
        self.email.clear()
        self.window_closed.emit()
        event.accept()


app = QApplication(sys.argv)
screen = app.primaryScreen()
screen_size = screen.size()
