from Database import Database
from models.Rental import Rental


class Rentals:
    # Model that represents all rentals in system

    def __init__(self):
        pass

    def create_rental(self, username, license_plate, start_rental_date, end_rental_date):
        # Inserts new_rental into rentals collection + Updates car's rental dates list
        # Returns error log

        new_rental = Rental(username, license_plate, start_rental_date, end_rental_date)

        error_log = self.validate_new_rental(new_rental)

        if self.operation_success(error_log) == True:
            try:
                self.create_rental_callback(username, license_plate, start_rental_date, end_rental_date)
            except ConnectionError:
                print('Server unavailable.')

        return error_log

    def delete_rental(self, username, license_plate, start_rental_date, end_rental_date):
        # Deletes rental with matching data from rentals collection + Removes rental dates from list
        # Returns true if deletion was successful. Else, returns false

        try:
            self.delete_rental_callback(username, license_plate, start_rental_date, end_rental_date)
        except ConnectionError:
            print('Server unavailable.')

        return

    def get_all_rentals(self):
        # Returns a list of all rentals + all their rental data

        database = Database()
        rentals = database.rentals_col

        try:
            cursors = rentals.find({})
            result = list(cursors)
            print(result)
            return result
        except ConnectionError:
            print('Server unavailable.')

        return

    def get_num_rentals(self):
        # Returns number of rentals + all their rental data

        rentals = self.get_all_rentals()
        return self.count_rentals(rentals)

    def get_rentals_by_location(self, location):
        # Returns a list of rentals + all their rental data from a rental location

        database = Database()
        rentals = database.rentals_col
        cars = database.cars_col

        try:
            # Get cars from a certain rental location
            cars_from_location = {"curr_rental_location": location}
            cursors = cars.find(cars_from_location)
            car_list = list(cursors)

            license_sublist = []
            for car in car_list:
                license_sublist.append(car['license_plate'])

            # Get rentals of cars from a certain rental location
            rental_sublist = []
            for license in license_sublist:
                rentals_with_license = {"license_plate": license}
                cursors = rentals.find(rentals_with_license)
                rental_sublist += list(cursors)

            return rental_sublist
        except ConnectionError:
            print('Server unavailable.')

    def get_num_rentals_by_location(self, location):
        # Returns a number of rentals + all their rental data from a rental locaiton

        rental_sublist = self.get_rentals_by_location(location)
        return self.count_rentals(rental_sublist)

    def create_rental_callback(self, username, license_plate, start_rental_date, end_rental_date):
        # Defines sequence of operations for rental transaction
        # Assumes that all parameters are valid

        database = Database()
        cars = database.cars_col
        rentals = database.rentals_col

        rental = Rental(username, license_plate, start_rental_date, end_rental_date)

        # Operation 1: Add rental to rentals database
        try:
            result = rentals.insert_one(rental.get_all_data()).inserted_id
            print(result)
        except ConnectionError:
            print('Server unavailable.')
            return

        # Operation 2 - Pushes new rental dates in car's rental dates list
        try:
            car_to_update = {"license_plate": license_plate}
            rental_dates_to_add = [start_rental_date, end_rental_date]
            update_operation = {"$push": {"rental_dates": rental_dates_to_add}}

            cars.update_one(car_to_update, update_operation)
        except ConnectionError:
            print('Server unavailable.')
            return

        return

    def delete_rental_callback(self, username, license_plate, start_rental_date, end_rental_date):
        # Defines sequence of operations for rental transaction
        # Assumes that all parameters are valid

        database = Database()

        database = Database()
        cars = database.cars_col
        rentals = database.rentals_col

        # Operation 1: Delete rental from rentals database
        try:
            rental_to_delete = {"username": username, "license_plate": license_plate,
                                "start_rental_date": start_rental_date, "end_rental_date": end_rental_date}
            result = rentals.delete_one(rental_to_delete)
            print(result)
        except ConnectionError:
            print('Server unavailable.')

        # Operation 2: Deletes rental dates in car's rental dates list
        try:
            car_to_update = {"license_plate": license_plate}
            rental_dates_to_remove = [start_rental_date, end_rental_date]
            update_operation = {"$pull": {"rental_dates": rental_dates_to_remove}}

            cars.update_one(car_to_update, update_operation)
        except ConnectionError:
            print('Server unavailable.')

        return

    def validate_new_rental(self, rental):
        # Validates user input
        # Returns an error-log

        database = Database()
        accounts = database.accounts_col
        cars = database.cars_col

        # Initializes error log
        error_log = {
            'user-exists': True,
            'car-exists': True,
        }

        # User account exists?
        account_to_find = {"username": rental.username}
        result = accounts.find_one(account_to_find)
        if result == None:
            error_log['user-exists'] = False

        # Car exists?
        car_to_find = {"license_plate": rental.license_plate}
        result = cars.find_one(car_to_find)
        if result == None:
            error_log['car-exists'] = False

        return error_log

    def operation_success(self, error_log):
        # Takes in error log from a CRUD operation
        # If an error was reported, return false. Else, return true

        for key, value in error_log.items():
            if value == False:
                return False

        return True

    def count_rentals(self, rental_list):
        if rental_list:
            return len(rental_list)
        else:
            return 0





