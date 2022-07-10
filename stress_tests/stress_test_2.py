import random

from flight_reservation.database import Connector
from flight_reservation.database.repository import Repository
from flight_reservation.reservation_system import ReservationSystem


def main(reservationsystem, repository, name, last_name, row, column):
    user = repository.create_new_user(name=name, last_name=last_name)
    for action in range(100):
        r = random.random()
        if r < 0.33:
            reservationsystem.get_all_flights()
        elif r < 0.66:
            # flight id somehow
            reservationsystem.reserve_flight_with_random_seat()
        else:
            continue
            # if user has reservation cancel it
            # else
            # reservationsystem.reserve_flight_with_random_seat()
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
