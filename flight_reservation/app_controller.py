from time import sleep

from .database.connector import Connector
from .reservation_system import ReservationSystem


class AppController:
    def __init__(self, db_connector: Connector) -> None:
        print("Initialization...", end="", flush=True)
        self.reservation_system = ReservationSystem(db_connector)
        print("\rInitialization done")

    def run(self):
        while True:
            print("Running...")
            sleep(5)
            print("Done")
            break


if __name__ == "__main__":
    connector = Connector()
    app_controller = AppController(connector)
    try:
        app_controller.run()
    finally:
        print("Closing...")
        connector.close()
        print("Closed")
