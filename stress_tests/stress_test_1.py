import random

from flight_reservation.database import Connector
from flight_reservation.database.repository import Repository
from flight_reservation.reservation_system import ReservationSystem


def main(reservationsystem, repository, name, last_name, row, column):
    user = repository.create_new_user(name=name, last_name=last_name)
    flights = reservationsystem.get_all_flights()
    flight_id = random.choice(flights)
    for i in range(100):
        reservationsystem.reserve_flight_with_specific_seat(user.id, flight_id, row, column)
    return True


if __name__ == "__main__":
    connector = Connector()
    repository = Repository(connector)
    reservationsystem = ReservationSystem(connector)
    try:
        main(reservationsystem, repository, "John", "Doe", 7, 2)
    finally:
        connector.close()
        print("Stress test done...")
