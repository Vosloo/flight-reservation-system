from .database import Repository
from .model import Airport, Flight, Plane


class FlightAdapter:
    def __init__(self, connector):
        self.repository = Repository(connector)

    def load_flight_info(self, flight) -> Flight:
        plane_row = self.repository.get_plane(flight.plane_id).one()
        plane = Plane(plane_row.id, plane_row.name)

        dep_airport_row = self.repository.get_airport(flight.departure_airport_id).one()
        dep_airport = Airport(
            dep_airport_row.id, dep_airport_row.name, dep_airport_row.city, dep_airport_row.country
        )

        arr_airport_row = self.repository.get_airport(flight.arrival_airport_id).one()
        arr_airport = Airport(
            arr_airport_row.id, arr_airport_row.name, arr_airport_row.city, arr_airport_row.country
        )

        return Flight(flight.id, plane, dep_airport, arr_airport)
