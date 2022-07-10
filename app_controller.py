from flight_reservation.database import Connector
from flight_reservation.reservation_system import ReservationSystem


class AppController:
    def __init__(self, db_connector: Connector) -> None:
        self.reservation_system = ReservationSystem(db_connector)

    def run(self):
        print(self.reservation_system.get_all_flights())


if __name__ == "__main__":
    connector = Connector()
    app_controller = AppController(connector)
    try:
        app_controller.run()
    finally:
        connector.close()
