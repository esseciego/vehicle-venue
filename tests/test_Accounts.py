import pytest
from models.Accounts import Accounts
from helpers.EnvVariables import EnvVariables

# To run tests, type 'pytest' in terminal at root directory

class TestAccounts:
    def setup_method(self):
        # Initialize the Accounts model and add dummy accounts for testing
        self.accounts = Accounts()
        self.create_dummy_accounts()

    def create_dummy_accounts(self):
        # Add dummy accounts here
        self.accounts.add_account("admin1", "adminpass", "admin1@example.com", "admin", "CityA")
        self.accounts.add_account("user1", "userpass", "user1@example.com", "user", "CityB")
        # ... Add more dummy accounts as needed ...

    def teardown_method(self):
        # Clean up / delete dummy accounts after tests run
        self.accounts.delete_account("admin1")
        self.accounts.delete_account("user1")
        # ... Add more cleanup as needed ...

    def get_dummy_accounts(self):
        # Method to retrieve dummy accounts for other uses such as GUI display
        return [
            {'username': 'admin1', 'password': 'adminpass', 'email': 'admin1@example.com', 'role': 'admin',
             'city': 'CityA'},
            {'username': 'user1', 'password': 'userpass', 'email': 'user1@example.com', 'role': 'user',
             'city': 'CityB'},
            # ... Include the rest of the dummy accounts ...
        ]

    def test_valid_new_acc(self):
        accounts = Accounts()

        result_log = accounts.add_account("GoodUsername", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'username-valid': True,
            'username-unique': True,
            'password-valid': True,
            'email-entered': True,
            'city-entered': True,
        }
        expected_success = True

        assert result_log == expected_log
        assert result_success == expected_success

        # Removes test account from database
        accounts.delete_account("GoodUsername")

    def test_invalid_new_username(self):
        accounts = Accounts()

        result_log = accounts.add_account("evilusername>:D", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'username-valid': False,
            'username-unique': True,
            'password-valid': True,
            'email-entered': True,
            'city-entered': True,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

    def test_taken_new_username(self):
        accounts = Accounts()

        accounts.add_account("UnoriginalUser", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        result_log = accounts.add_account("UnoriginalUser", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'username-valid': True,
            'username-unique': False,
            'password-valid': True,
            'email-entered': True,
            'city-entered': True,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

        accounts.delete_account("UnoriginalUser")

    def test_invalid_new_password(self):
        accounts = Accounts()

        result_log = accounts.add_account("GoodUsername", "evilpasswordmwahaha", "goodemail@email.com", "admin", "Gainesville")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'username-valid': True,
            'username-unique': True,
            'password-valid': False,
            'email-entered': True,
            'city-entered': True,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

    def test_empty_new_email(self):
        accounts = Accounts()

        result_log = accounts.add_account("GoodUsername", "good_Password1!1", "", "admin", "Gainesville")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'username-valid': True,
            'username-unique': True,
            'password-valid': True,
            'email-entered': False,
            'city-entered': True,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

    def test_empty_new_city(self):
        accounts = Accounts()

        result_log = accounts.add_account("GoodUsername", "good_Password1!1", "goodemail@gmail.com", "admin", "")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'username-valid': True,
            'username-unique': True,
            'password-valid': True,
            'email-entered': True,
            'city-entered': False,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

    def test_valid_login(self):
        # Test result log
        accounts = Accounts()

        accounts.add_account("GoodUsername", "good_Password1!1", "goodemail@email.com", "admin",
                             "Gainesville")
        result_log = accounts.login("GoodUsername", "good_Password1!1")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'user-exists': True,
            'password-correct': True,
        }
        expected_success = True

        assert result_log == expected_log
        assert result_success == expected_success

        # Test environmental variable
        env_vars = EnvVariables()

        result_user = env_vars.get_user()
        result_role = env_vars.get_role()
        result_city = env_vars.get_city()

        expected_user = "GoodUsername"
        expected_role = "admin"
        expected_city = "Gainesville"

        assert result_user == expected_user
        assert result_role == expected_role
        assert result_city == expected_city

        # Remove test account from database
        accounts.delete_account("GoodUsername")

        # Reset .env variables
        accounts.logout()


    def test_login_user_not_exist(self):
        # Test result log
        accounts = Accounts()

        accounts.add_account("GoodUsername", "good_Password1!1", "goodemail@email.com", "admin",
                                          "Gainesville")
        result_log = accounts.login("WHAT_IS_THIS_ACC_LMAO", "good_Password1!1")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'user-exists': False,
            'password-correct': False,
        }
        expected_success = False

        assert result_success == expected_success
        assert result_log == expected_log

        # Test environmental variable
        env_vars = EnvVariables()

        result_user = env_vars.get_user()
        result_role = env_vars.get_role()
        result_city = env_vars.get_city()

        expected_user = "NONE"
        expected_role = "NONE"
        expected_city = "NONE"

        assert result_user == expected_user
        assert result_role == expected_role
        assert result_city == expected_city

    def test_login_password_incorrect(self):
        # Test result log
        accounts = Accounts()

        accounts.add_account("GoodUsername", "good_Password1!1", "goodemail@email.com", "admin",
                                          "Gainesville")
        result_log = accounts.login("GoodUsername", "WRONG_PASSWORD_LMAO")
        result_success = accounts.operation_success(result_log)

        expected_log = {
            'user-exists': True,
            'password-correct': False,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

        # Test environmental variable
        env_vars = EnvVariables()

        result_user = env_vars.get_user()
        result_role = env_vars.get_role()
        result_city = env_vars.get_city()

        expected_user = "NONE"
        expected_role = "NONE"
        expected_city = "NONE"

        assert result_user == expected_user
        assert result_role == expected_role
        assert result_city == expected_city

    def test_logout(self):
        accounts = Accounts()

        accounts.add_account("GoodUsername", "good_Password1!1", "goodemail@email.com", "admin",
                                          "Gainesville")
        accounts.login("GoodUsername", "good_Password1!1")
        accounts.logout()

        # Test environmental variable
        env_vars = EnvVariables()

        result_user = env_vars.get_user()
        result_role = env_vars.get_role()
        result_city = env_vars.get_city()

        expected_user = "NONE"
        expected_role = "NONE"
        expected_city = "NONE"

        assert result_user == expected_user
        assert result_role == expected_role
        assert result_city == expected_city

        # Remove test account from database
        accounts.delete_account("GoodUsername")

    def test_user_exists_(self):
        accounts = Accounts()

        accounts.add_account("ShowYouOff", "good_Password1!1", "goodemail@email.com", "Admin", "Gainesville")

        result1_bool = accounts.user_exists("ShowYouOff")
        expected1_bool = True

        assert result1_bool == expected1_bool

        result2_bool = accounts.user_exists("HideMeOn")
        expected2_bool = False

        assert result2_bool == expected2_bool

        # Remove test accounts
        accounts.delete_account("ShowYouOff")

    def test_get_user_role(self):
        # FIXME: get_user returns 'NONE' if user is a client
        accounts = Accounts()

        accounts.add_account("Polymorphing", "good_Password1!1", "goodemail@email.com", "Admin", "Gainesville")
        accounts.add_account("Crying", "good_Password1!1", "goodemail@email.com", "Client", "Gainesville")

        result1_role = accounts.get_user_role("Polymorphing")
        expected1_role = "Admin"

        assert result1_role == expected1_role

        result2_role = accounts.get_user_role("Crying")
        expected2_role = "Client"

        assert result2_role == expected2_role

        result3_role = accounts.get_user_role("Juliet")
        expected3_role = "NONE"

        assert result3_role == expected3_role

        # Remove test accounts
        accounts.delete_account("Polymorphing")
        accounts.delete_account("Crying")


if __name__ == '__main__':
    test_accounts = TestAccounts()
    test_accounts.setup_method()  # Set up dummy accounts

    # Optionally, run the tests
    pytest.main()
