from dataclasses import dataclass


@dataclass
class Airport:
    id: str
    name: str
    city: str
    country: str

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"

    def __repr__(self):
        return str(self)
