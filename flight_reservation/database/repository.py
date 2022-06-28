from cassandra.cluster import PreparedStatement, ResultSet

from .connector import Connector
from .query_type import QueryType


class Repository:
    def __init__(self, connector: Connector) -> None:
        self._connector = connector
        self._prepared_queries = self._prepare_queries()

    def _prepare_queries(self) -> dict:
        prepared_queries = {}

        prepared_queries[QueryType.ADD_RESERVATION.value] = self._prepare_add_reservation()
        prepared_queries[QueryType.DELETE_RESERVATION.value] = self._prepare_delete_reservation()
        prepared_queries[
            QueryType.GET_ALL_FLIGHT_RESERVATIONS.value
        ] = self._prepare_get_all_flight_reservations()
        prepared_queries[QueryType.GET_ALL_USERS.value] = self._prepare_get_all_users()
        prepared_queries[QueryType.GET_FREE_SEATS.value] = self._prepare_get_free_seats()
        prepared_queries[
            QueryType.GET_USER_RESERVATIONS_FOR_FLIGHT.value
        ] = self._prepare_get_user_reservations_for_flight()
        prepared_queries[QueryType.GET_USER_RESERVATIONS.value] = self._prepare_get_user_reservations()
        prepared_queries[QueryType.GET_USER.value] = self._prepare_get_user()
        prepared_queries[QueryType.UPDATE_SEAT.value] = self._prepare_update_seat()

        return prepared_queries

    def add_reservation(self, user_id: str, flight_id: str, id: str) -> None:
        query = self._prepared_queries[QueryType.ADD_RESERVATION.value]
        self._connector.execute(query, user_id, flight_id, id)

    def _prepare_add_reservation(self) -> PreparedStatement:
        return self._connector.prepare(
            "INSERT INTO flight_reservation.reservation (user_id, flight_id, id) VALUES (?, ?, ?)"
        )

    def delete_reservation(self, user_id: str, flight_id: str, id: str) -> None:
        query = self._prepared_queries[QueryType.DELETE_RESERVATION.value]
        self._connector.execute(query, user_id, flight_id, id)

    def _prepare_delete_reservation(self) -> PreparedStatement:
        return self._connector.prepare(
            "DELETE FROM flight_reservation.reservation WHERE user_id = ? AND flight_id = ? AND id = ?"
        )

    def get_all_flight_reservations(self) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_ALL_FLIGHT_RESERVATIONS.value]
        return self._connector.execute(query)

    def _prepare_get_all_flight_reservations(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.reservation")

    def get_all_users(self) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_ALL_USERS.value]
        return self._connector.execute(query)

    def _prepare_get_all_users(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.user")

    def get_free_seats(self, flight_id: str) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_FREE_SEATS.value]
        return self._connector.execute(query, flight_id)

    def _prepare_get_free_seats(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.seat WHERE flight_id = ?")

    def get_user(self, user_id: str) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_USER.value]
        return self._connector.execute(query, user_id)

    def _prepare_get_user(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.user WHERE id = ?")

    def get_user_reservations(self, user_id: str) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_USER_RESERVATIONS.value]
        return self._connector.execute(query, user_id)

    def _prepare_get_user_reservations(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.reservation WHERE user_id = ?")

    def get_user_reservations_for_flight(self, user_id: str, flight_id: str) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_USER_RESERVATIONS_FOR_FLIGHT.value]
        return self._connector.execute(query, user_id, flight_id)

    def _prepare_get_user_reservations_for_flight(self) -> PreparedStatement:
        return self._connector.prepare(
            "SELECT * FROM flight_reservation.reservation WHERE user_id = ? AND flight_id = ?"
        )

    def update_seat(self, flight_id: str, row: int, column: int, is_vacant: bool) -> None:
        query = self._prepared_queries[QueryType.UPDATE_SEAT.value]
        self._connector.execute(query, is_vacant, flight_id, row, column)

    def _prepare_update_seat(self) -> PreparedStatement:
        return self._connector.prepare(
            "UPDATE flight_reservation.seat SET is_vacant = ? "
            "WHERE flight_id = ? AND row = ? AND column = ?"
        )
