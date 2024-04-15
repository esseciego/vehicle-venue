import sys
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QApplication, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from tests.test_Accounts import TestAccounts
from PyQt6.QtWidgets import QTableWidget
from models.Accounts import Accounts
from bson.objectid import ObjectId


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

        self.setStyleSheet("background-color: #ffe0c2")

    def initAdminLoginUI(self):  # Admin login UI elements
        # "Admin Login" text
        self.title = QLabel("Admin Login")
        self.title.setStyleSheet("color: black;"
                                 "font-weight: bold;"
                                 "font-family: Tahoma;"
                                 "font-size: 32px")
        self.layout.addWidget(self.title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # "Username:" text
        self.user_name_label = QLabel("Username:")
        self.user_name_label.setStyleSheet("font-family: Tahoma;"
                                           "font-size: 16px")
        self.layout.addWidget(self.user_name_label, 1, 0)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 1, 1)

        # "Password:" text
        self.user_password_label = QLabel("Password:")
        self.user_password_label.setStyleSheet("font-family: Tahoma;"
                                               "font-size: 16px")
        self.layout.addWidget(self.user_password_label, 2, 0)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password, 2, 1)

        # "Log In" button
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.authenticate_admin)
        self.login_button.setStyleSheet("background-color: #fa9352;"
                                        "color: black;"
                                        "font-weight: bold;"
                                        "font-family: Tahoma;")
        self.layout.addWidget(self.login_button, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

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
        accounts_model = Accounts()
        account_list = accounts_model.get_all_accounts()

        # Debug print: Output the account list to the console
        print("Retrieved account list:", account_list)


        # Initialize the table widget with the number of rows and columns
        self.table_widget = QTableWidget(len(account_list), 5)
        self.table_widget.setHorizontalHeaderLabels(["Username", "Password", "Email", "Role", "City"])

        for row, account in enumerate(account_list):
            # Debug print: Output each account to the console
            print(f"Inserting account into row {row}: {account}")
            self.table_widget.setItem(row, 0, QTableWidgetItem(account['username']))
            # It is not good practice to show passwords, but here is how you'd add it for debugging
            self.table_widget.setItem(row, 1, QTableWidgetItem("******"))
            self.table_widget.setItem(row, 2, QTableWidgetItem(account['email']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(account['role']))
            self.table_widget.setItem(row, 4, QTableWidgetItem(account.get('city', 'None')))

        self.table_widget.cellChanged.connect(self.on_cell_changed)

        # Clear out the previous table widget (if it exists) and other widgets before adding the new table
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            if widget_to_remove is not None:
                self.layout.removeWidget(widget_to_remove)
                widget_to_remove.deleteLater()

        # Add the new table to the layout
        self.layout.addWidget(self.table_widget, 2, 0)

        # Optionally add a button to go back to the settings page
        self.back_button = QPushButton("Back to Main")
        self.back_button.clicked.connect(self.close)
        self.layout.addWidget(self.back_button, 3, 0)

    def populate_table(self, account_list):
        self.table_widget.setRowCount(len(account_list))
        for row, account in enumerate(account_list):
            # Create the table items with account data
            username_item = QTableWidgetItem(account['username'])
            email_item = QTableWidgetItem(account['email'])
            role_item = QTableWidgetItem(account['role'])
            city_item = QTableWidgetItem(account.get('city', 'None'))

            # Set the _id as data associated with the username_item
            # Convert ObjectId to string because QTableWidgetItem can only store strings as data
            username_item.setData(Qt.ItemDataRole.UserRole, str(account['_id']))

            print(f"Row {row}: Storing _id {account['_id']}")

            # Add items to the table
            self.table_widget.setItem(row, 0, username_item)
            self.table_widget.setItem(row, 2, email_item)
            self.table_widget.setItem(row, 3, role_item)
            self.table_widget.setItem(row, 4, city_item)

    def on_cell_changed(self, row, column):
        print(f"Cell changed - Row: {row}, Column: {column}")

        # Assuming the _id is stored in the first column's user data
        account_id_str = self.table_widget.item(row, 0).data(Qt.ItemDataRole.UserRole)
        print(f"Retrieved _id string for update: {account_id_str}")

        if account_id_str:
            account_id = ObjectId(account_id_str)
            new_value = self.table_widget.item(row, column).text()

            fields = ["username", "password", "email", "role", "city"]
            if column < len(fields):
                field = fields[column]
                accounts_model = Accounts()
                success = accounts_model.update_account(account_id, field, new_value)
                if success:
                    print(f"Successfully updated account with id {account_id}")
                else:
                    print(f"Failed to update account with id {account_id}")
            else:
                print(f"Column index {column} out of range")
        else:
            print("No _id found for this row, update aborted.")

    def populate_table(self, account_list):
        self.table_widget.setRowCount(len(account_list))
        for row, account in enumerate(account_list):
            for col, key in enumerate(['username', 'password', 'email', 'role', 'city']):
                item = QTableWidgetItem(str(account[key]))
                item.setData(Qt.ItemDataRole.UserRole, str(account['_id']))
                self.table_widget.setItem(row, col, item)
            print(f"Inserted account into row {row}: {account}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_size = screen.size()
    settings_window = SettingsWindow()
    settings_window.show()
    sys.exit(app.exec())
