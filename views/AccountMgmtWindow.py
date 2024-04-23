import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox
)

from PyQt6.QtCore import Qt
from models.Accounts import Accounts
from bson.objectid import ObjectId


class AccountMgmtWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(10)
        self.setWindowTitle("Account Management")
        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() / 2), int(screen_size.height() / 2))

        # Manage Accounts label
        self.manage_accounts_label = QLabel("Manage Employee and Admin Accounts")
        self.manage_accounts_label.show()
        self.layout.addWidget(self.manage_accounts_label, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)

        # Save Changes button
        self.save_changes_button = QPushButton("Save Changes")
        self.save_changes_button.clicked.connect(self.save_all_changes)

        # Back To Main button
        self.back_button = QPushButton("Back to Main")
        self.back_button.clicked.connect(self.close)

        # FIXME: Edit accounts & create accounts button are to the left of the accounts button...?
        self.edit_accounts_button = QPushButton("Edit Accounts")
        self.edit_accounts_button.clicked.connect(self.show_account_list)
        self.layout.addWidget(self.edit_accounts_button, 1, 0)

        # Create Accounts button
        self.create_accounts_button = QPushButton("Create Accounts")
        self.create_accounts_button.clicked.connect(self.show_sign_up_page)
        self.layout.addWidget(self.create_accounts_button, 2, 0)

        # Create Accounts Title label
        self.create_accounts_title = QLabel("Please enter the user's information below.")
        self.create_accounts_title.setProperty("class", "heading")
        self.layout.addWidget(self.create_accounts_title, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.create_accounts_title.hide()

        # Username label + text
        self.user_username = QLabel("Username:")
        self.user_username.setProperty("class", "normal")
        self.layout.addWidget(self.user_username, 1, 0)
        self.user_username.hide()

        self.username = QLineEdit()
        self.layout.addWidget(self.username, 1, 1, 1, 2)
        self.username.hide()

        # Password label + text
        self.user_password = QLabel("Password:")
        self.user_password.setProperty("class", "normal")
        self.layout.addWidget(self.user_password, 2, 0)
        self.user_password.hide()

        self.password = QLineEdit()
        self.layout.addWidget(self.password, 2, 1, 1, 2)
        self.password.hide()

        # Email label + text
        self.user_email = QLabel("Email Address:")
        self.user_email.setProperty("class", "normal")
        self.layout.addWidget(self.user_email, 3, 0)
        self.user_email.hide()

        self.email = QLineEdit()
        self.layout.addWidget(self.email, 3, 1, 1, 2)
        self.email.hide()

        # City label + text
        self.user_city = QLabel("City:")
        self.user_city.setProperty("class","normal")
        self.layout.addWidget(self.user_city, 4, 0)
        self.user_city.hide()

        self.city = QLineEdit()
        self.layout.addWidget(self.city, 4, 1, 1, 2)
        self.city.hide()

        # Roles label + list
        self.user_role = QLabel("Role: ")
        self.user_role.setProperty("class", "normal")
        self.layout.addWidget(self.user_role, 5, 0)
        self.user_role.hide()

        self.role = QComboBox()
        self.role.addItems(["Employee", "Admin"])
        self.layout.addWidget(self.role, 5, 1, 1, 2)
        self.role.hide()

        # Sign up Button
        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.clicked.connect(self.sign_up)
        self.layout.addWidget(self.sign_up_button, 6, 0)
        self.sign_up_button.hide()

    def show_account_list(self):
        accounts_model = Accounts()
        account_list = accounts_model.get_accounts_by_role("Employee")

        self.table_widget = QTableWidget(len(account_list), 6)
        self.table_widget.setHorizontalHeaderLabels(["Username", "Password", "Email", "Role", "City"])
        self.table_widget.hideColumn(5)   # Hide the _id column

        for row, account in enumerate(account_list):
            self.table_widget.setItem(row, 0, QTableWidgetItem(account['username']))
            self.table_widget.setItem(row, 1, QTableWidgetItem("******"))
            self.table_widget.setItem(row, 2, QTableWidgetItem(account['email']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(account['role']))
            self.table_widget.setItem(row, 4, QTableWidgetItem(account.get('city', 'None')))
            id_item = QTableWidgetItem(str(account['_id']))
            self.table_widget.setItem(row, 5, id_item)

        self.table_widget.cellChanged.connect(self.on_cell_changed)
        self.layout.addWidget(self.table_widget, 2, 0)
        self.layout.addWidget(self.save_changes_button, 3, 0)
        self.save_changes_button.show()
        self.layout.addWidget(self.back_button, 4, 0)

        self.create_accounts_button.hide()
        self.edit_accounts_button.move(1, 0)

    def on_cell_changed(self, row, column):
        id_item = self.table_widget.item(row, 5)
        if id_item:
            account_id_str = id_item.text()
            account_id = ObjectId(account_id_str)
            new_value = self.table_widget.item(row, column).text()
            fields = ["username", "password", "email", "role", "city"]

            if column < len(fields):
                field = fields[column]
                accounts_model = Accounts()
                success = accounts_model.update_account(account_id, field, new_value)
                if success:
                    print(f"Successfully updated account with _id: {account_id}")
                else:
                    print(f"Failed to update account with _id: {account_id}")
            else:
                print("Column index out of range for updates.")
        else:
            print("No ID found, update aborted.")

    def show_sign_up_page(self):
        # Displays sign up form
        # Hide widgets from initial display
        self.manage_accounts_label.hide()
        self.edit_accounts_button.hide()
        self.create_accounts_button.hide()
        self.back_button.hide()

        self.create_accounts_title.show()
        self.user_username.show()
        self.username.show()
        self.user_password.show()
        self.password.show()
        self.user_email.show()
        self.email.show()
        self.user_city.show()
        self.city.show()
        self.user_role.show()
        self.role.show()
        self.sign_up_button.show()

    def sign_up(self):
        # Checks if account information is valid to make
        accounts_model = Accounts()
        error_log = accounts_model.add_account(self.username.text(), self.password.text(), self.email.text(), self.role.currentText(), self.city.text())

        if (accounts_model.operation_success(error_log)):
            self.create_accounts_title.setText("Account Created Successfully")
        else:
            if error_log['username-valid'] == False:
                self.create_accounts_title.setText("Username must be between 6-16 characters AND only uses alphanumeric characters")

            elif error_log['username-unique'] == False:
                self.create_accounts_title.setText("Username is already taken")

            elif error_log['password-valid'] == False:
                self.create_accounts_title.setText("Password must be between 8-32 characters AND contains at least 1 number")

            elif error_log['email-entered'] == False:
                self.create_accounts_title.setText("Please enter a valid email")

            elif error_log['city-entered'] == False:
                self.create_accounts_title.setText("Please enter a valid city")


    def save_all_changes(self):
        print("All changes have been saved.")
