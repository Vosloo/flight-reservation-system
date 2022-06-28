import sys
from pyrsistent import s
from flight_reservation.database import Connector, QueryType
from flight_reservation.reservation_system import ReservationSystem

if __name__ == "__main__":
    try:
        connector = Connector()
        system = ReservationSystem(connector)


        all_users = system.query.query(QueryType.GET_ALL_USERS)
        for user in all_users:
            print(user)
        
        all_flight_reservation = system.query.query(QueryType.GET_ALL_FLIGHT_RESERVATIONS)
        for flight in all_flight_reservation:
            print(flight)
        
        #system._seat_is_free("d2854968-f657-11ec-9cae-00d8612e7382", 1, 1)
    finally:
        connector.close()
