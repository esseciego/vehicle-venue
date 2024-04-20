import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from models.Accounts import Accounts
from bson.objectid import ObjectId

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initAdminLoginUI()

    def initUI(self):
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(10)
        self.setWindowTitle("Settings")
        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() / 2), int(screen_size.height() / 2))

    def initAdminLoginUI(self):
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
        self.settings_label = QLabel("Settings Page")
        self.settings_label.hide()

        self.save_changes_button = QPushButton("Save Changes")
        self.save_changes_button.clicked.connect(self.save_all_changes)
        self.save_changes_button.hide()  # Hide initially

        self.back_button = QPushButton("Back to Main")
        self.back_button.clicked.connect(self.close)

    def authenticate_admin(self):
        self.confirmation_label.setText("Login Successful")
        self.show_settings()

    def show_settings(self):
        self.title.hide()
        self.user_name_label.hide()
        self.username.hide()
        self.user_password_label.hide()
        self.password.hide()
        self.login_button.hide()
        self.confirmation_label.hide()
        self.settings_label.show()
        self.layout.addWidget(self.settings_label, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.account_list_button = QPushButton("Account List")
        self.account_list_button.clicked.connect(self.show_account_list)
        self.layout.addWidget(self.account_list_button, 1, 0)

    def show_account_list(self):
        accounts_model = Accounts()
        account_list = accounts_model.get_all_accounts()
        self.table_widget = QTableWidget(len(account_list), 6)
        self.table_widget.setHorizontalHeaderLabels(["Username", "Password", "Email", "Role", "City", "_id"])
        self.table_widget.hideColumn(5)  # Hide the _id column
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
                    print(f"Successfully updated account with id {account_id}")
                else:
                    print(f"Failed to update account with id {account_id}")
            else:
                print("Column index out of range for updates.")
        else:
            print("No ID found, update aborted.")

    def save_all_changes(self):
        print("All changes have been saved.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_size = screen.size()
    settings_window = SettingsWindow()
    settings_window.show()
    sys.exit(app.exec())
