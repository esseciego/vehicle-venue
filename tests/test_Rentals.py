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

    def test_get_rentals_by_location_multi(self):
        # Note: Using get_num_rentals_by_location() as a proxy for get_rentals_by_location()
        # For implementation, can just use rentals.get_cars_by_location()
        accounts = Accounts()
        cars = Cars()
        rentals = Rentals()

        accounts.add_account("MakeoutCreek", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        cars.add_car("FIRST", "<TYPE>", "XXXX", 1, 00.01, 00.01)
        cars.add_car("LOVE", "<TYPE>", "XXXX", 1, 00.01, 00.01)
        cars.add_car("LATE", "<TYPE>", "YYYY", 1, 00.01, 00.01)
        cars.add_car("SPRING", "<TYPE>", "ZZZZ", 1, 00.01, 00.01)

        rentals.create_rental("MakeoutCreek", "FIRST", "04-13-2024", "04-14-2024")
        rentals.create_rental("MakeoutCreek", "LATE", "04-15-2024", "04-16-2024")
        rentals.create_rental("MakeoutCreek", "SPRING", "04-17-2024", "04-18-2024")

        result_num_rentals_by_location = rentals.get_num_rentals_by_location("XXXX")
        expected_num_rentals_by_location = 1

        assert result_num_rentals_by_location == expected_num_rentals_by_location

        # Remove test data
        accounts.delete_account("MakeoutCreek")
        cars.delete_car("FIRST")
        cars.delete_car("LOVE")
        cars.delete_car("LATE")
        cars.delete_car("SPRING")
        rentals.delete_rental("MakeoutCreek", "FIRST", "04-13-2024", "04-14-2024")
        rentals.delete_rental("MakeoutCreek", "LATE", "04-15-2024", "04-16-2024")
        rentals.delete_rental("MakeoutCreek", "SPRING", "04-17-2024", "04-18-2024")

    def test_get_cars_by_location_none(self):
        # Note: Using get_num_rentals_by_location() as a proxy for get_rentals_by_location()
        # For implementation, can just use rentals.get_cars_by_location()
        accounts = Accounts()
        cars = Cars()
        rentals = Rentals()

        accounts.add_account("Puberty2", "good_Password1!1", "goodemail@email.com", "admin", "Gainesville")
        cars.add_car("LOSING", "<TYPE>", "MMMM", 1, 00.01, 00.01)
        cars.add_car("DOGS", "<TYPE>", "LLLL", 1, 00.01, 00.01)

        rentals.create_rental("Puberty2", "LOSING", "04-13-2024", "04-14-2024")
        rentals.create_rental("Puberty2", "DOGS", "04-15-2024", "04-16-2024")

        result_num_rentals_by_location = rentals.get_num_rentals_by_location("OOOO")
        expected_num_rentals_by_location = 0

        assert result_num_rentals_by_location == expected_num_rentals_by_location

        # Remove test data
        accounts.delete_account("Puberty2")
        cars.delete_car("LOSING")
        cars.delete_car("DOGS")
        rentals.delete_rental("Puberty2", "LOSING", "04-13-2024", "04-14-2024")
        rentals.delete_rental("Puberty2", "DOGS", "04-15-2024", "04-16-2024")


if __name__ == '__main__':
    pytest.main()