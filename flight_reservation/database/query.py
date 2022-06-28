from cassandra.cluster import PreparedStatement, ResultSet

from .connector import Connector
from .query_type import QueryType


class Query:
    def __init__(self, connector: Connector) -> None:
        self._connector = connector

        self._prepared_queries = self._prepare_queries()

    def query(self, query_type: QueryType, *args) -> ResultSet:
        prepared_query = self._prepared_queries.get(query_type.value)
        if prepared_query is None:
            raise ValueError(f"Unknown query type: {query_type}")

        return self._connector.execute(prepared_query, *args)

    def _prepare_queries(self) -> dict:
        prepared_queries = {}

        # TODO: Prepare all queries and add them here

        prepared_queries[QueryType.GET_USER.value] = self._prepare_get_user()
        prepared_queries[QueryType.GET_USER_RESERVATIONS.value] = self._prepare_get_user_reservations()
        prepared_queries[
            QueryType.GET_USER_RESERVATION_FOR_FLIGHT.value
        ] = self._prepare_get_user_reservation_for_flight()
        prepared_queries[QueryType.GET_FREE_SEATS.value] = self._prepare_get_free_seats()
        prepared_queries[QueryType.GET_ALL_USERS.value] = self._prepare_get_all_users()
        prepared_queries[QueryType.GET_ALL_FLIGHT_RESERVATIONS.value] = self._prepare_get_all_flight_reservations()

        return prepared_queries

    def _prepare_get_all_users(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.user")

    def _prepare_get_all_flight_reservations(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.reservation")

    def _prepare_get_free_seats(self) -> PreparedStatement:
        return self._connector.prepare(
            "SELECT * FROM flight_reservation.seat WHERE flight_id = ?"
        )

    def _prepare_get_user(self) -> PreparedStatement:
        return self._connector.prepare("SELECT * FROM flight_reservation.user WHERE id = ?")

    def _prepare_get_user_reservations(self) -> PreparedStatement:
        return self._connector.prepare(
            "SELECT * FROM flight_reservation.reservation WHERE user_id = ?"
        )

    def _prepare_get_user_reservation_for_flight(self) -> PreparedStatement:
        return self._connector.prepare(
            "SELECT * FROM flight_reservation.reservation "
            "WHERE user_id = ? AND flight_id = ?"
        )
