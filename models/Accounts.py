from Database import Database
from helpers.EnvVariables import EnvVariables
from models.Account import Account



class Accounts:
    # Model that represents all user accounts in system

    def __init__(self):
        pass

    def add_account(self, username, password, email, role, city):
        # Inserts new_account document into accounts collection if user input is valid. Doesn't insert if invalid
        # Returns error log

        database = Database()
        accounts = database.accounts_col

        new_account = Account(username, password, email, role, city)

        error_log = self.validate(new_account)

        if self.operation_success(error_log) == True:
            try:
                new_account.encrypt_password()
                result = accounts.insert_one(new_account.get_all_data()).inserted_id
                print(result)
            except ConnectionError:
                print('Server unavailable.')

        return error_log

    def delete_account(self, username):
        # Deletes account with matching username from accounts collection
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

        return

    def delete_all_accounts(self):
        # Deletes all accounts from database
        # Returns true if deletion was successful. Else returns false

        database = Database()
        accounts = database.accounts_col

        try:
            result = accounts.delete_many({})
            print(result)
            return True if result else False

        except ConnectionError:
            print('Server unavailable.')

    def validate(self, account):
        # FIXME: Change name to 'validate_new_account'
        # Validates user input
        # Returns an error-log

        database = Database()
        accounts = database.accounts_col

        # Initializes error log
        error_log = {
            'username-valid': True,
            'username-unique': True,
            'password-valid': True,
            'email-entered': True,
            'city-entered': True,
        }

        # Username valid? (Between 6-16 characters AND only uses alphanumeric characters)
        if ((len(account.username) < 6) or (len(account.username) > 16)
                or not (account.username.isalnum())):
            error_log['username-valid'] = False

        # Username unique?
        account_to_find = {"username": account.username}
        result = accounts.find_one(account_to_find)
        if not (result == None):
            error_log['username-unique'] = False

        # Password valid? (Between 8-32 characters AND contains at least 1 number)
        if ((len(account.password) < 6 or len(account.password) > 32)
                or not (any(chr.isdigit() for chr in account.password))):
            error_log['password-valid'] = False

        # Email entered?
        if account.email == '':
            error_log['email-entered'] = False

        # City entered?
        if account.city == '':
            error_log['city-entered'] = False

        return error_log

    def login(self, username, password):
        # Logs in user
        # Returns error log

        database = Database()
        accounts = database.accounts_col

        error_log = self.validate_login(username, password)
        # FIXME: Error log won't process
        if self.operation_success(error_log) == True:
            env_vars = EnvVariables()

            # Change USER .env variable
            env_vars.set_user(username)

            # Change ROLE .env variable
            account_to_find = {"username": username}
            result = accounts.find_one(account_to_find)
            role = result['role']
            env_vars.set_role(role)

        return error_log

    def logout(self):
        # Logs out user

        env_vars = EnvVariables()

        env_vars.set_user('NONE')
        env_vars.set_role('NONE')
        return

    def validate_login(self, username, password):
        # Validates whether login was correct

        database = Database()
        accounts = database.accounts_col

        # Initializes error log
        error_log = {
            'user-exists': True,
            'password-correct': True,
        }

        # User account exists?
        account_to_find = {"username": username}
        result = accounts.find_one(account_to_find)
        if result == None:
            error_log['user-exists'] = False
            error_log['password-correct'] = False
            return error_log

        # Password correct?
        account = Account(result['username'], result['password'], result['email'], result['role'], result['city'])
        decrypted_password = account.get_decrypt_password()
        if decrypted_password != password:
            error_log['password-correct'] = False

        return error_log

    def operation_success(self, error_log):
        # Takes in error log from a CRUD operation
        # If an error was reported, return false. Else, return true

        for key, value in error_log.items():
            if value == False:
                return False

        return True

