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

    def initAdminLoginUI(self):  # Admin login UI elements
        # "Admin Login" text
        self.title = QLabel("Admin Login")
        self.layout.addWidget(self.title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # "Username:" text
        self.user_name_label = QLabel("Username:")
        self.layout.addWidget(self.user_name_label, 1, 0)
        self.username = QLineEdit()
        self.layout.addWidget(self.username, 1, 1)

        # "Password:" text
        self.user_password_label = QLabel("Password:")
        self.layout.addWidget(self.user_password_label, 2, 0)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password, 2, 1)

        # "Log In" button
        self.login_button = QPushButton("Log In")
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
        self.table_widget.setColumnCount(6)  # Add a new column for _id
        self.table_widget.setHorizontalHeaderLabels(["Username", "Password", "Email", "Role", "City", "_id"])
        self.table_widget.hideColumn(5)  # Hide the _id column

        self.table_widget.setRowCount(len(account_list))
        for row, account in enumerate(account_list):
            # Add account data to the table
            self.table_widget.setItem(row, 0, QTableWidgetItem(account['username']))
            self.table_widget.setItem(row, 1, QTableWidgetItem("******"))
            self.table_widget.setItem(row, 2, QTableWidgetItem(account['email']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(account['role']))
            self.table_widget.setItem(row, 4, QTableWidgetItem(account.get('city', 'None')))

            # Store the _id in the hidden column
            id_item = QTableWidgetItem(str(account['_id']))
            self.table_widget.setItem(row, 5, id_item)

    def on_cell_changed(self, row, column):
        print(f"Cell changed - Row: {row}, Column: {column}")

        # Check if the item is not None before getting text
        id_item = self.table_widget.item(row, 5)
        if id_item is not None:
            account_id_str = id_item.text()
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
                    print("Column index out of range for updates.")
            else:
                print("No _id string found for this row, update aborted.")
        else:
            print(f"No item found in row {row}, column 5.")

    def populate_table(self, account_list):
        # Assuming self.table_widget is a QTableWidget
        self.table_widget.setRowCount(len(account_list))

        # Column headers should match the keys from the account dict
        headers = ['Username', 'Password', 'Email', 'Role', 'City']
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        # Loop over the account list and populate the table
        for row, account in enumerate(account_list):
            for col, key in enumerate(['username', 'password', 'email', 'role', 'city']):
                # Create a new QTableWidgetItem with the data
                item = QTableWidgetItem(str(account[key]))

                # Special handling for the username item to store the ObjectId
                if key == 'username':
                    # Set the ObjectId as data associated with the item, using the UserRole data role
                    item.setData(Qt.ItemDataRole.UserRole, str(account['_id']))

                # Set the item at the proper location in the table
                self.table_widget.setItem(row, col, item)

            print(f"Inserted account into row {row}: {account}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_size = screen.size()
    settings_window = SettingsWindow()
    settings_window.show()
    sys.exit(app.exec())
