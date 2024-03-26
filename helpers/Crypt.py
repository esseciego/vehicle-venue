from dotenv import load_dotenv
import os

import cryptocode


class Crypt:
    # Helper to encode/decode strings

    def __init__(self):
        # Load content from .env file
        load_dotenv()
        # Get key
        self.key = os.getenv("KEY")

    def encrypt(self, string):
        # Wrapper to encrypt string
        return cryptocode.encrypt(string, self.key)

    def decrypt(self, string):
        # Wrapper to decrypt string
        return cryptocode.decrypt(string, self.key)
