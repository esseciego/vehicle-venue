class Car:
    # Model that represents a car in system

    def __init__(self, license_plate: str, car_type: str, curr_rental_location: str, mileage: int, cost_per_day: float,
                 cost_per_mile: float):
        self.license_plate = license_plate
        self.car_type = car_type
        self.curr_rental_location = curr_rental_location
        self.mileage = mileage
        self.cost_per_day = cost_per_day
        self.cost_per_mile = cost_per_mile

        self.curr_car_status = "AVAILABLE"
        self.rental_dates = []

    def get_all_data(self):
        # Returns dictionary of car data
        return {
            'license_plate': self.license_plate,
            'car_type': self.car_type,
            'curr_rental_location': self.curr_rental_location,
            'mileage': self.mileage,
            'cost_per_day': self.cost_per_day,
            'cost_per_mile': self.cost_per_mile,
            'curr_car_status': self.curr_car_status,
            'rental_dates': self.rental_dates,
        }
