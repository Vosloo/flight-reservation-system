from dataclasses import dataclass


@dataclass
class Plane:
    id: str
    name: str

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return str(self)
