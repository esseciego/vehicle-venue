from dotenv import load_dotenv, set_key
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

    def set_user(self, username):
        # Sets current user
        os.environ['USER'] = username
        return

    def set_role(self, role):
        # Sets current user's role
        os.environ['ROLE'] = role
        pass
