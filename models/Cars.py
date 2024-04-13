from Database import Database
from models.Car import Car


class Cars:
    # Model that represents all cars in system

    def __init__(self):
        pass

    def add_car(self, license_plate: str, type: str, curr_rental_location: str, mileage: int, cost_per_day: float,
                cost_per_mile: float):
        # Inserts new_car document into accounts collection if user input is valid. Doesn't insert if invalid
        # Returns error log

        database = Database()
        cars = database.cars_col

        new_car = Car(license_plate, type, curr_rental_location, mileage, cost_per_day, cost_per_mile)

        error_log = self.validate_new_car(new_car)

        if self.operation_success(error_log) == True:
            try:
                result = cars.insert_one(new_car.get_all_data()).inserted_id
                print(result)
            except ConnectionError:
                print('Server unavailable.')

        return error_log

    def delete_car(self, license_plate):
        # Deletes account with matching license_plate from cars collection
        # Returns true if deletion was successful. Else, returns false

        database = Database()
        cars = database.cars_col

        try:
            car_to_delete = {"license_plate": license_plate}
            result = cars.delete_one(car_to_delete)
            print(result)
            return True if result else False

        except ConnectionError:
            print('Server unavailable.')

        return

    def get_all_cars(self):
        # Returns a list of all cars + all their car data

        database = Database()
        cars = database.cars_col

        try:
            cursors = cars.find({})
            result = list(cursors)
            print(result)
            return result
        except ConnectionError:
            print('Server unavailable.')

        return

    def get_num_cars(self):
        # Returns an int with total num of cars in database

        database = Database()
        cars = database.cars_col

        try:
            result = cars.count_documents({})
            return result
        except ConnectionError:
            print('Server unavailable.')

        return

    def get_cars_by_location(self, location):
        # Returns a list of cars + all their car data from a city

        database = Database()
        cars = database.cars_col

        try:
            cars_from_location = {"curr_rental_location": location}
            cursors = cars.find(cars_from_location)
            result = list(cursors)
            print(result)
            return result
        except ConnectionError:
            print('Server unavailable.')

        return

    def get_car_rental_dates(self, license_plate):
        # Returns a list of a car's rental dates

        database = Database()
        cars = database.cars_col

        try:
            car_to_retrieve = {"license_plate": license_plate}
            retrieved_car = cars.find_one(car_to_retrieve)
            return list(retrieved_car["rental_dates"])
        except ConnectionError:
            print('Server unavailable.')

    def get_num_car_rental_dates(self, license_plate):
        # Returns a number of times a car is rented

        database = Database()
        cars = database.cars_col

        try:
            car_to_retrieve = {"license_plate": license_plate}
            retrieved_car = cars.find_one(car_to_retrieve)
            if retrieved_car:
                retrieved_car_date_list = list(retrieved_car["rental_dates"])
                return len(retrieved_car_date_list)
            else:
                return 0
        except ConnectionError:
            print('Server unavailable.')


    def validate_new_car(self, car):
        # Validates user input
        # Returns an error-log

        database = Database()
        cars = database.cars_col

        # Initializes error log
        error_log = {
            'license-plate-valid': True,
            'license-plate-unique': True,
            'type-entered': True,
            'curr-rental-location-entered': True,
        }

        # License plate valid? (Between 1-7 characters AND only uses alphanumeric characters AND letters must be upper-case)
        if ((len(car.license_plate) < 1) or (len(car.license_plate) > 7)
                or not (car.license_plate.isalnum())
                or (car.license_plate.islower())):
            error_log['license-plate-valid'] = False

        # License plate unique?
        car_to_find = {"license_plate": car.license_plate}
        result = cars.find_one(car_to_find)
        if not (result == None):
            error_log['license-plate-unique'] = False

        # Car type entered?
        if car.type == '':
            error_log['type-entered'] = False

        # Current rental location entered?
        if car.curr_rental_location == '':
            error_log['curr-rental-location-entered'] = False

        return error_log

    def operation_success(self, error_log):
        # Takes in error log from a CRUD operation
        # If an error was reported, return false. Else, return true

        for key, value in error_log.items():
            if value == False:
                return False

        return True
