import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout,
    QLabel)

from views.LogInWindow import LogInWindow
from views.SignUpWindow import SignUpWindow
from views.SettingsWindow import SettingsWindow


class MainWindow(QWidget):
    # Basically the home page just a stand in
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(100)

        self.setWindowTitle("Home Page")
        self.setLayout(self.layout)

        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_size = screen.size()

        self.resize(screen_size)

        # Welcomes to home page
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

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.settings_window)
        self.layout.addWidget(settings_button, 0, 5)

        self.settings_window_instance = None

    def log_in_window(self):
        self.log_in_window = LogInWindow()
        self.log_in_window.show()

    def sign_up_window(self):
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.show()

    def settings_window(self):
        if self.settings_window_instance is None or not self.settings_window_instance.isVisible():
            self.settings_window_instance = SettingsWindow()
        self.settings_window_instance.show()


app = QApplication(sys.argv)
screen = app.primaryScreen()
screen_size = screen.size()

window = MainWindow()
window.show()
sys.exit(app.exec())
