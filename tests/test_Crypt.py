import pytest
from helpers.Crypt import Crypt

# To run tests, type 'pytest' in terminal at root directory

class TestCrypt:
    # Crypt test suite

    def test_crypt(self):
        crypt = Crypt()

        message = "Womp womp womp"

        encrypted_message = crypt.encrypt(message)
        decrypted_message = crypt.decrypt(encrypted_message)

        assert message == decrypted_message