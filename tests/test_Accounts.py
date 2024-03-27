import pytest
from models.Accounts import Accounts
from helpers.EnvVariables import EnvVariables

# To run tests, type 'pytest' in terminal at root directory


class TestAccounts:
    # Accounts test suite

    # FIXME: Make usernames for each test unique
    # Prevents getting failed tests in error message. Sometimes, documents aren't deleted on MongoDB fast enough
    # Use alphabetical names? -> "GoodApple", "GoodBanana", etc.

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
        envVariables = EnvVariables()

        result_user = envVariables.get_user()
        result_role = envVariables.get_role()

        expected_user = "GoodUsername"
        expected_role = "admin"

        assert result_user == expected_user
        assert result_role == expected_role

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
        envVariables = EnvVariables()

        result_user = envVariables.get_user()
        result_role = envVariables.get_role()

        expected_user = "NONE"
        expected_role = "NONE"

        assert result_user == expected_user
        assert result_role == expected_role

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
        envVariables = EnvVariables()

        result_user = envVariables.get_user()
        result_role = envVariables.get_role()

        expected_user = "NONE"
        expected_role = "NONE"

        assert result_user == expected_user
        assert result_role == expected_role

    def test_logout(self):
        accounts = Accounts()

        accounts.add_account("GoodUsername", "good_Password1!1", "goodemail@email.com", "admin",
                                          "Gainesville")
        accounts.login("GoodUsername", "good_Password1!1")
        accounts.logout()

        # Test environmental variable
        envVariables = EnvVariables()

        result_user = envVariables.get_user()
        result_role = envVariables.get_role()

        expected_user = "NONE"
        expected_role = "NONE"

        assert result_user == expected_user
        assert result_role == expected_role

        # Remove test account from database
        accounts.delete_account("GoodUsername")



if __name__ == '__main__':
    # Runs test suite when script is run
    pytest.main()
