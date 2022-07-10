from dataclasses import dataclass

from .airport import Airport
from .plane import Plane


@dataclass
class Flight:
    id: str
    plane: Plane
    departure_airport: Airport
    arrival_airport: Airport

    def __str__(self):
        return (
            f"Flight: {self.departure_airport.name} to {self.arrival_airport.name} ({self.plane.name})"
        )

    def __repr__(self):
        return str(self)
