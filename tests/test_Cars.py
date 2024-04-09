import pytest
from models.Cars import Cars

# To run tests, type 'pytest' in terminal at root directory


class TestCars:
    # Test suite for cars model

    def test_valid_new_car(self):
        cars = Cars()

        result_log = cars.add_car("L1CENSE", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        result_success = cars.operation_success(result_log)

        expected_log = {
            'license-plate-valid': True,
            'license-plate-unique': True,
            'type-entered': True,
            'curr-rental-location-entered': True,
        }
        expected_success = True

        assert result_log == expected_log
        assert result_success == expected_success

        # Removes test car from database
        cars.delete_car("L1CENSE")


    def test_invalid_new_license(self):
        cars = Cars()

        result_log = cars.add_car("dang", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        result_success = cars.operation_success(result_log)

        expected_log = {
            'license-plate-valid': False,
            'license-plate-unique': True,
            'type-entered': True,
            'curr-rental-location-entered': True,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success


    def test_taken_new_license(self):
        cars = Cars()

        cars.add_car("BIGEYES", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        result_log = cars.add_car("BIGEYES", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        result_success = cars.operation_success(result_log)

        expected_log = {
            'license-plate-valid': True,
            'license-plate-unique': False,
            'type-entered': True,
            'curr-rental-location-entered': True,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

        # Removes test car from database
        cars.delete_car("BIGEYES")


    def test_empty_new_type(self):
        cars = Cars()

        result_log = cars.add_car("SM0KE", "", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        result_success = cars.operation_success(result_log)

        expected_log = {
            'license-plate-valid': True,
            'license-plate-unique': True,
            'type-entered': False,
            'curr-rental-location-entered': True,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success


    def test_empty_new_location(self):
        cars = Cars()

        result_log = cars.add_car("PANG", "<TYPE>", "", 1, 00.01, 00.01)
        result_success = cars.operation_success(result_log)

        expected_log = {
            'license-plate-valid': True,
            'license-plate-unique': True,
            'type-entered': True,
            'curr-rental-location-entered': False,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

    # NOTE: Not sure how to unit test show_all_cars(). Might be easier to see if function works by seeing result in view
    # For now, will test get_num_cars() as a proxy
        # get_number_cars() returns number of cars that would match a get_all_cars() query

    def test_get_num_cars_many(self):
        cars = Cars()

        cars.add_car("CRYING", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        cars.add_car("IN", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        cars.add_car("PUBLIC", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)

        result_count = cars.get_num_cars()

        expected_count = 3

        assert result_count == expected_count

        # Removes test cars from database
        cars.delete_car("CRYING")
        cars.delete_car("IN")
        cars.delete_car("PUBLIC")

    def test_get_num_cars_none(self):
        cars = Cars()

        result_count = cars.get_num_cars()

        expected_count = 0

        assert result_count == expected_count


if __name__ == '__main__':
    pytest.main()
