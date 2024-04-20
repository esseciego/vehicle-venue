from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# a class that helps connect to mongo DB
class Database:
    # Holds car rentals database
    def __init__(self):
        self.uri = "mongodb+srv://tears_user:sobbing.emoji@carrental.fiinqnj.mongodb.net/?retryWrites=true&w=majority&appName=CarRental"

        # Create a new client and connect to the server
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
        except Exception as e:
            print(e)
            exit()

        # Gets references to collections
        self.db = self.client.car_rental_data

        self.accounts_col = self.db.accounts
        self.cars_col = self.db.cars
        self.rentals_col = self.db.rentals

    def get_client(self):
        return self.client







