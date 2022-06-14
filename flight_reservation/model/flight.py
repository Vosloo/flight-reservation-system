from uuid import uuid4

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Flight(Model):
    __table_name__ = "flight"

    id = columns.UUID(primary_key=True, default=lambda: uuid4())
    plane_id = columns.UUID(required=True)
    departure_airport_id = columns.UUID(required=True)
    arrival_airport_id = columns.UUID(required=True)
