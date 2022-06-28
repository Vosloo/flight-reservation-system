import uuid

from .database import Connector, Repository, QueryType


class ReservationSystem:
    def __init__(self, connector: Connector) -> None:
        self.query = Repository(connector)

        self._free_seats = {}

    def cancel_reservation(self, user_id: str, flight_id: str) -> bool:
        # TODO: Implement
        pass

    def reserve_flight_with_random_seat(self, user_id: str, flight_id: str) -> bool:
        # TODO: Implement
        pass

    def reserve_flight_with_specific_seat(
        self, user_id: str, flight_id: str, row: int, column: int
    ) -> bool:
        # TODO: Implement
        pass

    def _seat_is_free(self, flight_id: str, row: int, column: int) -> bool:
        flight_id = uuid.UUID(flight_id)

        if seats := self._free_seats.get(flight_id) is None:
            # Seats are not yet loaded for this flight
            res = self.query.query(QueryType.GET_FREE_SEATS, {"flight_id": flight_id})
            # TODO: Create _free_seats[flight_id] = res; res needs to have matrix structure (np.array?)
            seats = ... # seats = self._free_seats[flight_id]

        # seats[row][column] = (is_vacant) True/False

        # TODO:
        # return seats[row][column]
        return ...

    def _user_has_reservation_for_flight(self, user_id: str, flight_id: str) -> bool:
        # TODO: Implement
        pass

    # TODO: What more can we add here?
