import unittest
from models.Accounts import Accounts


class TestAccounts(unittest.TestCase):
    # Accounts test suite
    def test_add_account(self):
        accounts = Accounts()
        result = accounts.add_account("<NAME>", "<PASSWORD>", "<EMAIL>", "<ROLE>", "<CITY>")
        self.assertEqual(result, True)

        # Removes test account from database
        accounts.delete_account("<NAME>")


if __name__ == '__main__':
    # Runs test suite when script is run
    unittest.main()
