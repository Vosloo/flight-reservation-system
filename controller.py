from flight_reservation.database import Connector
from flight_reservation.reservation_system import ReservationSystem


if __name__ == "__main__":
    try:
        connector = Connector()
        system = ReservationSystem(connector)

        for user in system.query.get_all_users():
            print(user.id, user.first_name, user.last_name)
    finally:
        connector.close()
