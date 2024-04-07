from Database import Database
from models.Car import Car

class Cars:
    # Model that represents all cars in system

    def __init__(self):
        pass

    def add_car(self, license_plate: str, car_type: str, curr_rental_location: str, mileage: int, cost_per_day: float, cost_per_mile: float):
        # Inserts new_car document into accounts collection if user input is valid. Doesn't insert if invalid
        # Returns error log

        database = Database()
        cars = database.cars_col

        new_car = Car(license_plate, car_type, curr_rental_location, mileage, cost_per_day, cost_per_mile)

        try:
            result = cars.insert_one(new_car.get_all_data()).inserted_id
            print(result)
            return True if result else False
        except ConnectionError:
            print('Server unavailable.')

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







