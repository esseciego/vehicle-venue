import pytest
from models.Cars import Cars

# To run tests, type 'pytest' in terminal at root directory


class TestCars:
    # Test suite for cars model

    def test_add_car(self):
        cars = Cars()
        result = cars.add_car("<LICENSE_PLATE>", "<CAR_TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.02)
        assert result == True

        # Removes test car from database
        cars.delete_car("<LICENSE_PLATE>")


if __name__ == '__main__':
    pytest.main()
