from enum import Enum, unique


@unique
class QueryType(Enum):
    ADD_RESERVATION = "add_reservation"
    ADD_USER = "add_user"
    CLEAN_SEATS = "clean_seats"
    CLEAN_RESERVATIONS = "clean_reservations"
    DELETE_USER = "delete_user"
    DELETE_RESERVATION = "delete_reservation"
    GET_AIRPORT = "get_airport"
    GET_ALL_FLIGHT_RESERVATIONS = "get_all_flight_reservations"
    GET_ALL_FLIGHTS = "get_all_flights"
    GET_ALL_USERS = "get_all_users"
    GET_ALL_SEATS = "get_all_seats"
    GET_PLANE = "get_plane"
    GET_RESERVATION = "get_reservation"
    GET_USER = "get_user"
    GET_USER_RESERVATIONS = "get_user_reservations"
    GET_USER_RESERVATIONS_FOR_FLIGHT = "get_user_reservations_for_flight"
    UPDATE_SEAT = "update_seat"
