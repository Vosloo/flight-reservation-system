from datetime import datetime
from typing import Union
from uuid import UUID, uuid1

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
        prepared_queries[QueryType.GET_AIRPORT.value] = self._prepare_get_airport()
        prepared_queries[
            QueryType.GET_ALL_FLIGHT_RESERVATIONS.value
        ] = self._prepare_get_all_flight_reservations()
        prepared_queries[QueryType.GET_ALL_FLIGHTS.value] = self._prepare_get_all_flights()
        prepared_queries[QueryType.GET_ALL_USERS.value] = self._prepare_get_all_users()
        prepared_queries[QueryType.GET_FREE_SEATS.value] = self._prepare_get_free_seats()
        prepared_queries[QueryType.GET_PLANE.value] = self._prepare_get_plane()
        prepared_queries[QueryType.GET_RESERVATION.value] = self._prepare_get_reservation()
        prepared_queries[
            QueryType.GET_USER_RESERVATIONS_FOR_FLIGHT.value
        ] = self._prepare_get_user_reservations_for_flight()
        prepared_queries[QueryType.GET_USER_RESERVATIONS.value] = self._prepare_get_user_reservations()
        prepared_queries[QueryType.GET_USER.value] = self._prepare_get_user()
        prepared_queries[QueryType.UPDATE_SEAT.value] = self._prepare_update_seat()

        return prepared_queries

    def execute_query(self, query: str, *args) -> ResultSet:
        """Executes arbitrary query"""
        return self._connector.execute(query, args)

    def add_reservation(
        self, user_id: Union[str, UUID], flight_id: Union[str, UUID], seat_row: int, seat_column: int
    ) -> None:
        user_id = self._format_as_uuid(user_id)
        flight_id = self._format_as_uuid(flight_id)

        query = self._prepared_queries[QueryType.ADD_RESERVATION.value]
        self._connector.execute(
            query, [user_id, flight_id, uuid1(), seat_row, seat_column, datetime.now()]
        )

    def _prepare_add_reservation(self) -> PreparedStatement:
        return self._connector.prepare(
            "INSERT INTO flight_reservation.reservation "
            "(user_id, flight_id, id, seat_row, seat_column, created_at) VALUES (?, ?, ?, ?, ?, ?)"
        )

    def delete_reservation(
        self, user_id: Union[str, UUID], flight_id: Union[str, UUID], _id: Union[str, UUID]
    ) -> None:
        user_id = self._format_as_uuid(user_id)
        flight_id = self._format_as_uuid(flight_id)
        _id = self._format_as_uuid(_id)

        query = self._prepared_queries[QueryType.DELETE_RESERVATION.value]
        self._connector.execute(query, [user_id, flight_id, _id])

    def _prepare_delete_reservation(self) -> PreparedStatement:
        return self._connector.prepare(
            "DELETE FROM flight_reservation.reservation WHERE user_id = ? AND flight_id = ? AND id = ?"
        )

    def get_airport(self, airport_id: Union[str, UUID]) -> ResultSet:
        airport_id = self._format_as_uuid(airport_id)

        query = self._prepared_queries[QueryType.GET_AIRPORT.value]
        return self._connector.execute(query, [airport_id])

    def _prepare_get_airport(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.airport WHERE id = ?")

    def get_all_flight_reservations(self) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_ALL_FLIGHT_RESERVATIONS.value]
        return self._connector.execute(query)

    def _prepare_get_all_flight_reservations(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.reservation")

    def get_all_flights(self) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_ALL_FLIGHTS.value]
        return self._connector.execute(query)

    def _prepare_get_all_flights(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.flight")

    def get_all_users(self) -> ResultSet:
        query = self._prepared_queries[QueryType.GET_ALL_USERS.value]
        return self._connector.execute(query)

    def _prepare_get_all_users(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.user")

    def get_free_seats(self, flight_id: Union[str, UUID]) -> ResultSet:
        flight_id = self._format_as_uuid(flight_id)

        query = self._prepared_queries[QueryType.GET_FREE_SEATS.value]
        return self._connector.execute(query, [flight_id])

    def _prepare_get_free_seats(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.seat WHERE flight_id = ?")

    def get_plane(self, plane_id: Union[str, UUID]) -> ResultSet:
        plane_id = self._format_as_uuid(plane_id)

        query = self._prepared_queries[QueryType.GET_PLANE.value]
        return self._connector.execute(query, [plane_id])

    def _prepare_get_plane(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.plane WHERE id = ?")

    def get_reservation(
        self, user_id: Union[str, UUID], flight_id: Union[str, UUID], _id: Union[str, UUID]
    ) -> ResultSet:
        user_id = self._format_as_uuid(user_id)
        flight_id = self._format_as_uuid(flight_id)
        _id = self._format_as_uuid(_id)

        query = self._prepared_queries[QueryType.GET_RESERVATION.value]
        return self._connector.execute(query, [user_id, flight_id, _id])

    def _prepare_get_reservation(self) -> PreparedStatement:
        return self._connector.prepare(
            "SELECT * FROM flight_reservation.reservation "
            "WHERE user_id = ? AND flight_id = ? AND id = ?"
        )

    def get_user(self, user_id: Union[str, UUID]) -> ResultSet:
        user_id = self._format_as_uuid(user_id)

        query = self._prepared_queries[QueryType.GET_USER.value]
        return self._connector.execute(query, [user_id])

    def _prepare_get_user(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.user WHERE id = ?")

    def get_user_reservations(self, user_id: Union[str, UUID]) -> ResultSet:
        user_id = self._format_as_uuid(user_id)

        query = self._prepared_queries[QueryType.GET_USER_RESERVATIONS.value]
        return self._connector.execute(query, [user_id])

    def _prepare_get_user_reservations(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.reservation WHERE user_id = ?")

    def get_user_reservations_for_flight(
        self, user_id: Union[str, UUID], flight_id: Union[str, UUID]
    ) -> ResultSet:
        user_id = self._format_as_uuid(user_id)
        flight_id = self._format_as_uuid(flight_id)

        query = self._prepared_queries[QueryType.GET_USER_RESERVATIONS_FOR_FLIGHT.value]
        return self._connector.execute(query, [user_id, flight_id])

    def _prepare_get_user_reservations_for_flight(self) -> PreparedStatement:
        return self._connector.prepare(
            "SELECT * FROM flight_reservation.reservation WHERE user_id = ? AND flight_id = ?"
        )

    def update_seat(self, flight_id: Union[str, UUID], row: int, column: int, is_vacant: bool) -> None:
        flight_id = self._format_as_uuid(flight_id)

        query = self._prepared_queries[QueryType.UPDATE_SEAT.value]
        self._connector.execute(query, [is_vacant, flight_id, row, column])

    def _prepare_update_seat(self) -> PreparedStatement:
        return self._connector.prepare(
            "UPDATE flight_reservation.seat SET is_vacant = ? "
            "WHERE flight_id = ? AND row = ? AND column = ?"
        )

    def _format_as_uuid(self, value: Union[UUID, str]) -> UUID:
        if isinstance(value, str):
            return UUID(value)
        elif isinstance(value, UUID):
            return value
        else:
            raise ValueError(f"Invalid value type for UUID: {type(value)}")
