from time import sleep
import uuid
from flight_reservation.database import Connector
from flight_reservation.reservation_system import ReservationSystem


if __name__ == "__main__":
    try:
        connector = Connector()
        system = ReservationSystem(connector)

        user_id = uuid.uuid1()
        sleep(0.2)
        flight_id = uuid.uuid1()
        res1 = system.repository.add_reservation(
            user_id=user_id,
            flight_id=flight_id,
            seat_row=1,
            seat_column=1
        )
        print(f"Adding reservation for user {user_id} on flight {flight_id}")

        print("----")

        res2 = system.repository.get_user_reservations(user_id)
        print(f"Getting reservations for user {user_id}")
        for res in res2:
            print(res)

        print("----")

        for user in system.repository.get_user('6cdd54aa-f70d-11ec-9e42-00d8612e7382'):
            print(user.id, user.first_name, user.last_name)
    finally:
        connector.close()
