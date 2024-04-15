from dotenv import load_dotenv
import os

class EnvVariables:
    def __init__(self):
        pass

    def get_user(self):
        # Returns current user's role
        load_dotenv()
        return os.getenv('USER')

    def get_role(self):
        # Returns current user's role
        load_dotenv()
        return os.getenv('ROLE')

    def get_city(self):
        # Returns current user's city
        load_dotenv()
        return os.getenv('CITY')

    def set_user_data(self, username, role, city):
        os.environ['USER'] = username
        os.environ['ROLE'] = role
        os.environ['CITY'] = city
        return

    def reset_user_data(self):
        os.environ['USER'] = 'NONE'
        os.environ['ROLE'] = 'NONE'
        os.environ['CITY'] = 'NONE'
