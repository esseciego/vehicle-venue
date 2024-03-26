import pytest
from models.Accounts import Accounts

# To run tests, type 'pytest' in terminal at root directory


#update acc function should go here
class TestAccounts:
    # Accounts test suite

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



if __name__ == '__main__':
    # Runs test suite when script is run
    pytest.main()
