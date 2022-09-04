import random

from definitions import NO_COLS, NO_ROWS
from flight_reservation.database import Connector
from flight_reservation.database.repository import Repository
from flight_reservation.model.flight import Flight
from flight_reservation.model.user import User
from flight_reservation.reservation_system import ReservationSystem
from flight_reservation.user_factory import UserFactory


def main(reservation_system: ReservationSystem, user: User, flight: Flight) -> None:
    row_ind, col_ind = random.randint(1, NO_ROWS - 1), random.randint(1, NO_COLS - 1)

    for _ in range(100):
        reserved = reservation_system.reserve_flight_with_specific_seat(
            user.id, flight.id, row_ind, col_ind
        )
        if reserved:
            print(f"Reserved seat: {row_ind} {col_ind}")
        else:
            print(f"Could not reserve seat: {row_ind} {col_ind}!")


def get_random_flight(reservation_system: ReservationSystem) -> Flight:
    return random.choice(reservation_system.get_all_flights())


if __name__ == "__main__":
    print("Initializing resources...")
    connector = Connector()
    user_factory = UserFactory()
    repository = Repository(connector)
    reservation_system = ReservationSystem(connector)

    user = user_factory.create_user(name="Stress", last_name="User")
    repository.add_user(user.id, user.first_name, user.last_name)

    flight = get_random_flight(reservation_system)

    print(f"Created user: {user.id} - {user.first_name} {user.last_name}")
    print(f"Selected flight with id: {flight.id}")

    try:
        print("Running test!")
        main(reservation_system, user, flight)
    finally:
        print("Cleaning up...")
        repository.clean_seats(flight.id)
        repository.clean_reservations()
        repository.delete_user(user.id)

        connector.close()
        print("Stress test done...")
