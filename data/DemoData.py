import sys
sys.path.append('../')

from models.Accounts import Accounts
from models.Cars import Cars
from models.Rentals import Rentals

# To handle demo data, (1) change into 'data' directory and (2) type 'python DemoData.py' in terminal

class DemoData:
    # Class to handle demo data

    def __init__(self):
        pass

    def insert_data(self):
        accounts = Accounts()
        cars = Cars()
        rentals = Rentals()

        # Insert accounts (8)
        accounts.add_account("ADmrina", "mrina_pass123", "mrina@email.com", "Admin", "Gainesville")
        accounts.add_account("EEouri", "ouri_pass123", "ouri@email.com", "Employee", "Gainesville")
        accounts.add_account("EEtagne", "tagne_pass123", "tagne@email.com", "Employee", "Gainesville")
        accounts.add_account("EEeute", "eute_pass123", "eute@email.com", "Employee", "Lady Lake")
        accounts.add_account("EEnsonic", "nsonic_pass123", "nsonic@email.com", "Employee", "Lady Lake")

        accounts.add_account("hlauritz", "hlauritz_pass123", "hlauritz@email.com", "Client", "Tavares")
        accounts.add_account("fkuzma", "fkuzma_pass123", "fkuzma@email.com", "Client", "Tavares")
        accounts.add_account("dparth", "dparth_pass123", "dparth@email.com", "Client", "Tavares")

        # Insert cars (8)
        cars.add_car("KITYPUR", "SUV", "Gainesville", 25, 81.00, 00.39)
        cars.add_car("MRGAY", "Van", "Gainesville", 30, 60.00, 00.40)
        cars.add_car("SUPBRA", "Sedan", "Gainesville", 45, 42.00, 00.42)
        cars.add_car("EATCHIA", "SUV", "Lady Lake", 30, 81.00, 00.39)
        cars.add_car("BYTEME2", "SUV", "Lady Lake", 40, 78.00, 00.32)

        cars.add_car("FUNKLFE", "Van", "Tavares", 20, 70.00, 00.42)
        cars.add_car("HALF666", "Van", "Tavares", 25, 64.00, 00.34)
        cars.add_car("LVRTOES", "Sedan", "Tavares", 50, 43.00, 00.20)

        # Insert rentals (4)
        rentals.create_rental("hlauritz", "KITYPUR", "2024-04-27", "2024-04-27")
        rentals.create_rental("fkuzma", "MRGAY", "2024-05-01", "2024-05-03")
        rentals.create_rental("dparth", "LVRTOES", "2024-05-06", "2024-05-11")
        rentals.create_rental("fkuzma", "LVRTOES", "2024-05-12", "2024-05-14")

        return

    def delete_data(self):
        accounts = Accounts()
        cars = Cars()
        rentals = Rentals()

        # Delete accounts (8)
        accounts.delete_account("ADmrina")
        accounts.delete_account("EEouri")
        accounts.delete_account("EEtagne")
        accounts.delete_account("EEeute")
        accounts.delete_account("EEnsonic")

        accounts.delete_account("hlauritz")
        accounts.delete_account("fkuzma")
        accounts.delete_account("dparth")

        # Deletes cars (8)
        cars.delete_car("KITYPUR")
        cars.delete_car("MRGAY")
        cars.delete_car("SUPBRA")
        cars.delete_car("EATCHIA")
        cars.delete_car("BYTEME2")

        cars.delete_car("FUNKLFE")
        cars.delete_car("HALF666")
        cars.delete_car("LVRTOES")

        # Delete rentals (4)
        rentals.delete_rental("hlauritz", "KITYPUR", "2024-04-27", "2024-04-27")
        rentals.delete_rental("fkuzma", "MRGAY", "2024-05-01", "2024-05-03")
        rentals.delete_rental("dparth", "LVRTOES", "2024-05-06", "2024-05-11")
        rentals.delete_rental("fkuzma", "LVRTOES", "2024-05-12", "2024-05-14")

        return


if __name__ == '__main__':
    demo_data = DemoData()

    print("*** Demo Data Handler ***")
    print("Press 'i' to insert demo data into the MongoDB database")
    print("Press 'd' to delete demo data from the MongoDB database")
    print("Press 'q' to quit")

    while True:
        key = input("Enter a key: ")
        if key == 'i':
            demo_data.insert_data()
        elif key == 'd':
            demo_data.delete_data()
        elif key == 'q':
            exit()
        else:
            print("Invalid input. Please try again.\n")
