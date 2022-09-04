import random
from typing import List

from .database import Connector, Repository
from .flight_adapter import FlightAdapter
from .model.flight import Flight

FIELD_ROW = "row"
FIELD_COLUMN = "column"
FIELD_IS_VACANT = "is_vacant"


class ReservationSystem:
    def __init__(self, connector: Connector) -> None:
        self.repository = Repository(connector)
        self.flight_adapter = FlightAdapter(connector)

    def cancel_reservation(self, user_id: str, flight_id: str, reservation_id: str) -> bool:
        reservation, = self.repository.get_reservation(user_id, flight_id, reservation_id).all()

        row, column = reservation.seat_row, reservation.seat_column
        self.repository.update_seat(flight_id, row, column, True)
        self.repository.delete_reservation(user_id, flight_id, reservation_id)

        return True

    def get_free_seats_in_flight(self, flight_id) -> list:
        return self.repository.get_free_seats(flight_id).all()

    def get_all_flights(self) -> List[Flight]:
        flights = self.repository.get_all_flights().all()

        return list(map(lambda flight: self.flight_adapter.load_flight_info(flight), flights))

    def get_user_reservations(self, user_id: str) -> list:
        return self.repository.get_user_reservations(user_id).all()

    def get_user_reservations_for_flight(self, user_id: str, flight_id: str) -> list:
        return self.repository.get_user_reservations_for_flight(user_id, flight_id)

    def reserve_flight_with_random_seat(self, user_id: str, flight_id: str) -> bool:
        free_seats_in_flight = self.repository.get_free_seats(flight_id)
        seat = random.choice(free_seats_in_flight)
        row, column = seat[FIELD_ROW], seat[FIELD_COLUMN]
        self.repository.add_reservation(user_id, flight_id, row, column)
        self.repository.update_seat(flight_id, row, column, True)

        return True

    def reserve_flight_with_specific_seat(
        self, user_id: str, flight_id: str, row: int, column: int
    ) -> bool:
        if self._seat_is_free(flight_id, row, column):
            self.repository.add_reservation(user_id, flight_id, row, column)
            self.repository.update_seat(flight_id, row, column, is_vacant=False)
            return True
        else:
            return False

    def _seat_is_free(self, flight_id: str, row: int, column: int) -> bool:
        free_seats = self.repository.get_free_seats(flight_id)
        for seat in free_seats:
            seat_row, seat_column = seat.row, seat.column
            if row == seat_row and column == seat_column:
                return seat.is_vacant

        return False
