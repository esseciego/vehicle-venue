class Rental:
    def __init__(self, username: str, license_plate: str, start_rental_date: str, end_rental_date: str):
        self.username = username
        self.license_plate = license_plate
        self.start_rental_date = start_rental_date
        self.end_rental_date = end_rental_date

    def get_all_data(self):
        return {
            'username': self.username,
            'license_plate': self.license_plate,
            'start_rental_date': self.start_rental_date,
            'end_rental_date': self.end_rental_date,
        }