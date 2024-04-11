import pytest
from models.Accounts import Accounts
from models.Cars import Cars
from models.Rentals import Rentals

# To run tests, type 'pytest' in terminal at root directory


class TestRentals:
    # Test suite for rentals model

    def test_valid_rental_blank(self):
        accounts = Accounts()
        cars = Cars()
        rentals = Rentals()

        accounts.add_account("Laurel", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        cars.add_car("SOFT", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)

        # Get initial values
        init_rentals_count = rentals.get_num_rentals()
        init_rental_dates_count = 0

        result_log = rentals.create_rental("Laurel", "SOFT", "04-13-2024", "04-14-2024")
        result_success = rentals.operation_success(result_log)

        # Subtest 1 : Tests if log is correct
        expected_log = {
            'user-exists': True,
            'car-exists': True,
        }
        expected_success = True

        assert result_log == expected_log
        assert result_success == expected_success

        # Subtest 2 : Tests if rentals database were updated
        final_rentals_count = rentals.get_num_rentals()
        result_rentals_added = final_rentals_count - init_rentals_count
        expected_rentals_added = 1
        assert result_rentals_added == expected_rentals_added

        # Subtest 3 : Tests if car's rental dates were updated
        final_rental_dates_count = cars.get_num_car_rental_dates("SOFT")
        result_rental_dates_added = final_rental_dates_count - init_rental_dates_count
        expected_rental_dates_added = 1
        assert result_rental_dates_added == expected_rental_dates_added

        # Remove test data
        accounts.delete_account("Laurel")
        cars.delete_car("SOFT")
        rentals.delete_rental("Laurel", "SOFT", "04-13-2024", "04-14-2024")

    def test_valid_rental_multi_rentals(self):
        accounts = Accounts()
        cars = Cars()
        rentals = Rentals()

        accounts.add_account("Retired", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        cars.add_car("SQUARE", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        rentals.create_rental("Retired",  "SQUARE", "04-13-2024", "04-14-2024")

        # Get initial values
        init_rentals_count = rentals.get_num_rentals()
        init_rental_dates_count = cars.get_num_car_rental_dates("SQUARE")

        result_log = rentals.create_rental("Retired", "SQUARE", "04-15-2024", "04-16-2024")
        result_success = rentals.operation_success(result_log)

        # Subtest 1 : Tests if log is correct
        expected_log = {
            'user-exists': True,
            'car-exists': True,
        }
        expected_success = True

        assert result_log == expected_log
        assert result_success == expected_success

        # Subtest 2 : Tests if rentals database were updated
        final_rentals_count = rentals.get_num_rentals()
        result_rentals_added = final_rentals_count - init_rentals_count
        expected_rentals_added = 1
        assert result_rentals_added == expected_rentals_added

        # Subtest 3 : Tests if car's rental dates were updated
        final_rental_dates_count = cars.get_num_car_rental_dates("SQUARE")
        result_rental_dates_added = final_rental_dates_count - init_rental_dates_count
        expected_rental_dates_added = 1
        assert result_rental_dates_added == expected_rental_dates_added

        # Remove test data
        accounts.delete_account("Retired")
        cars.delete_car("SQUARE")
        rentals.delete_rental("Retired", "SQUARE", "04-13-2024", "04-14-2024")
        rentals.delete_rental("Retired", "SQUARE", "04-15-2024", "04-16-2024")

    def test_invalid_user_and_license(self):
        accounts = Accounts()
        cars = Cars()
        rentals = Rentals()

        accounts.add_account("Lush", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        cars.add_car("LIQUID", "<TYPE>", "<CURR_RENTAL_LOCATION>", 1, 00.01, 00.01)
        rentals.create_rental("Lush",  "LIQUID", "04-13-2024", "04-14-2024")

        # Get initial values
        init_rentals_count = rentals.get_num_rentals()
        init_rental_dates_count = cars.get_num_car_rental_dates("LIQUID")

        result_log = rentals.create_rental("l0sh", "L1QUID", "04-15-2024", "04-16-2024")
        result_success = rentals.operation_success(result_log)

        # Subtest 1 : Tests if log is correct
        expected_log = {
            'user-exists': False,
            'car-exists': False,
        }
        expected_success = False

        assert result_log == expected_log
        assert result_success == expected_success

        # Subtest 2 : Tests if rentals database were updated
        final_rentals_count = rentals.get_num_rentals()
        result_rentals_added = final_rentals_count - init_rentals_count
        expected_rentals_added = 0
        assert result_rentals_added == expected_rentals_added

        # Subtest 3 : Tests if car's rental dates were updated
        final_rental_dates_count = cars.get_num_car_rental_dates("SQUARE")
        result_rental_dates_added = final_rental_dates_count - init_rental_dates_count
        expected_rental_dates_added = 0
        assert result_rental_dates_added == expected_rental_dates_added

        # Remove test data
        accounts.delete_account("Lush")
        cars.delete_car("LIQUID")
        rentals.delete_rental("Lush", "LIQUID", "04-13-2024", "04-14-2024")


if __name__ == '__main__':
    pytest.main()