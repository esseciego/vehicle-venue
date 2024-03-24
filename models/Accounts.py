from Database import Database
from models.Account import Account


class Accounts:
    # Model that represents all user accounts in system

    def __init__(self):
        pass

    def add_account(self, username, password, email, role, city):
        # Inserts new_account document into accounts collection
        # Returns true if insertion was successful. Else, returns false

        database = Database()
        accounts = database.accounts_col

        new_account = Account(username, password, email, role, city)

        try:
            result = accounts.insert_one(new_account.get_data()).inserted_id
            print(result)
            return True if result else False
        except ConnectionError:
            print('Server unavailable.')

    def delete_account(self, username):
        # Deletes new_account document from accounts collection
        # Returns true if deletion was successful. Else, returns false

        database = Database()
        accounts = database.accounts_col

        try:
            account_to_delete = {"username": username}
            result = accounts.delete_one(account_to_delete)
            print(result)
            return True if result else False

        except ConnectionError:
            print('Server unavailable.')


