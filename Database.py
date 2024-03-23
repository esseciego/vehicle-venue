from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class Database:
    # Holds CarRentals Database
    def __init__(self):
        uri = "mongodb+srv://tears_user:sobbing.emoji@carrental.fiinqnj.mongodb.net/?retryWrites=true&w=majority&appName=CarRental"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
