import random
from multiprocessing import Process
from typing import List

from definitions import NO_COLS, NO_ROWS
from flight_reservation.database import Connector
from flight_reservation.database.repository import Repository
from flight_reservation.model.flight import Flight
from flight_reservation.model.user import User
from flight_reservation.reservation_system import ReservationSystem
from flight_reservation.user_factory import UserFactory


def execute_test(test_no):
    def main(reservation_system: ReservationSystem, user: User) -> None:
        reserved = reservation_system.reserve_all(user.id)
        if reserved:
            print(f"USER_{test_no}: Reserved all!")
        else:
            print(f"USER_{test_no}: Could not reserve all seats!")

    print(f"USER_{test_no}: Initializing resources...")
    connector = Connector()
    user_factory = UserFactory()
    repository = Repository(connector)
    reservation_system = ReservationSystem(connector)

    user = user_factory.create_user(name="Stress", last_name=f"User_{test_no}")
    repository.add_user(user.id, user.first_name, user.last_name)

    flights = reservation_system.get_all_flights()

    print(f"USER_{test_no}: Created user: {user.id} - {user.first_name} {user.last_name}")

    try:
        print(f"USER_{test_no}: Running test!")
        main(reservation_system, user)
    finally:
        print(f"USER_{test_no}: Cleaning up...")
        for flight in flights:
            repository.clean_seats(flight.id)
        repository.clean_reservations()
        repository.delete_user(user.id)

        connector.close()
        print(f"USER_{test_no}: Stress test done...")


if __name__ == "__main__":
    for user_no in range(2):
        Process(target=execute_test, args=(user_no,)).start()