from enum import Enum, unique


@unique
class QueryType(Enum):
    GET_FREE_SEATS = "get_free_seats"
    GET_USER = "get_user"
    GET_USER_RESERVATION_FOR_FLIGHT = "get_user_reservation_for_flight"
    GET_USER_RESERVATIONS = "get_user_reservations"
