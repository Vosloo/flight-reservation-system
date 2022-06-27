from flight_reservation.database import Connector
from flight_reservation.reservation_system import ReservationSystem

if __name__ == "__main__":
    try:
        connector = Connector()
        system = ReservationSystem(connector)

        system._seat_is_free("d2854968-f657-11ec-9cae-00d8612e7382", 1, 1)
    finally:
        connector.close()
