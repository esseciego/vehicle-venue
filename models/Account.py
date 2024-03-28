from helpers.Crypt import Crypt

class Account:
    # Model that represents a user's account in system

    def __init__(self, username: str, password: str, email: str, role: str, city: str):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.city = city

    def get_all_data(self):
        # Returns dictionary of account data
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'role': self.role,
            'city': self.city,
        }

    def encrypt_password(self):
        # Encodes password
        crypt = Crypt()
        self.password = crypt.encrypt(self.password)

    def get_decrypt_password(self):
        crypt = Crypt()
        decrypt_password = crypt.decrypt(self.password)
        return decrypt_password
