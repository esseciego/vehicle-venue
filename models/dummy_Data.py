# populate_dummy_data.py
from Accounts import Accounts

def populate_dummy_accounts():
    accounts_manager = Accounts()
    accounts_manager.create_dummy_accounts()
    print("Dummy accounts have been added to the database.")

if __name__ == "__main__":
    populate_dummy_accounts()
