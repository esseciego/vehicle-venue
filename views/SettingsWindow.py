import sys
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QApplication,QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from tests.test_Accounts import TestAccounts
from PyQt6.QtWidgets import QTableWidget



class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initAdminLoginUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(100)
        self.setWindowTitle("Settings")
        self.setLayout(self.layout)

        # Assuming screen_size is obtained the same way as in MainWindow
        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() / 2), int(screen_size.height() / 2))

    def initAdminLoginUI(self):
        # Admin login UI elements
        self.title = QLabel("Admin Login")
        self.layout.addWidget(self.title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.user_name_label = QLabel("Username:")
        self.layout.addWidget(self.user_name_label, 1, 0)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 1, 1)

        self.user_password_label = QLabel("Password:")
        self.layout.addWidget(self.user_password_label, 2, 0)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password, 2, 1)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authenticate_admin)
        self.layout.addWidget(self.login_button, 3, 0, 1, 2)

        self.confirmation_label = QLabel("")
        self.layout.addWidget(self.confirmation_label, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Hide settings UI until admin is authenticated
        self.settings_label = QLabel("Settings Page")
        self.settings_label.hide()

    def authenticate_admin(self):
        # Since any credentials are acceptable, we directly show the settings.
        self.confirmation_label.setText("Login Successful")
        self.show_settings()

    def show_settings(self):
        # Hide login UI
        self.title.hide()
        self.user_name_label.hide()
        self.username.hide()
        self.user_password_label.hide()
        self.password.hide()
        self.login_button.hide()
        self.confirmation_label.hide()

        # Show settings UI
        self.settings_label.show()
        self.layout.addWidget(self.settings_label, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)
        # Here, you would add your settings controls

        self.account_list_button = QPushButton("Account List")
        self.account_list_button.clicked.connect(self.show_account_list)
        self.layout.addWidget(self.account_list_button, 1, 0)

    def show_account_list(self):
        # Create an instance of TestAccounts to use the dummy accounts
        test_accounts = TestAccounts()

        # Fetch the dummy account data
        account_list = test_accounts.get_dummy_accounts()

        # Set up the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(account_list))
        self.table_widget.setColumnCount(5)  # Adjust the number of columns based on account attributes
        self.table_widget.setHorizontalHeaderLabels(["Username", "Password", "Email", "Role", "City"])

        for row, account in enumerate(account_list):
            self.table_widget.setItem(row, 0, QTableWidgetItem(account['username']))
            self.table_widget.setItem(row, 1, QTableWidgetItem(account['password']))  # Be cautious with real passwords
            self.table_widget.setItem(row, 2, QTableWidgetItem(account['email']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(account['role']))
            self.table_widget.setItem(row, 4, QTableWidgetItem(account['city']))

        # Add the table to the layout and hide the settings label and button
        self.layout.addWidget(self.table_widget)
        self.settings_label.hide()
        self.account_list_button.hide()

        # Optionally, add a button to go back to the settings page
        self.back_to_settings_button = QPushButton("Back to Settings")
        self.back_to_settings_button.clicked.connect(self.show_settings)
        self.layout.addWidget(self.back_to_settings_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_size = screen.size()
    settings_window = SettingsWindow()
    settings_window.show()
    sys.exit(app.exec())
