import random
import uuid

from .database import Connector, Repository


class ReservationSystem:
    def __init__(self, connector: Connector) -> None:
        self.repository = Repository(connector)

        self._free_seats = {}

    def cancel_reservation(self, user_id: str, flight_id: str, reservation_id: str) -> bool:
        self.repository.delete_reservation(user_id, flight_id, reservation_id)
        reservation = self.repository.get_reservation(user_id, flight_id, reservation_id)
        row, column = reservation["row"], reservation["column"]
        self.repository.update_seat(flight_id, row, column, True)
        # usuń z tabeli reservation
        # zmień na wolne w tabeli siedzeń
        print("Reservation was canceled.")
        return True

    def reserve_flight_with_random_seat(self, user_id: str, flight_id: str) -> bool:
        free_seats_in_flight = self.repository.get_free_seats(flight_id)
        seat = random.choice(free_seats_in_flight)
        row, column = seat["row"], seat["column"]
        self.repository.add_reservation(user_id, flight_id, row, column)
        self.repository.update_seat(flight_id, row, column, True)

        return True

    def reserve_flight_with_specific_seat(
        self, user_id: str, flight_id: str, row: int, column: int
    ) -> bool:
        self.repository.add_reservation(user_id, flight_id, row, column)
        self.repository.update_seat(flight_id, row, column, True)

        return True

    def _seat_is_free(self, flight_id: str, row: int, column: int) -> bool:
        flight_id = uuid.UUID(flight_id)

        free_seats = self.repository.get_free_seats(flight_id)
        for seat in free_seats:
            seat_row, seat_column = seat["row"], seat["column"]
            if row == seat_row and column == seat_column:
                return seat["is_vacant"]

        return False

    def _user_has_reservation_for_flight(self, user_id: str, flight_id: str) -> bool:
        # TODO: Implement
        pass

    # TODO: What more can we add here?
