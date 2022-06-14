from uuid import uuid4

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Reservation(Model):
    __table_name__ = "reservation"

    id = columns.UUID(primary_key=True, default=lambda: uuid4())
    user_id = columns.UUID(required=True)
    flight_id = columns.UUID(required=True)
    seat_id = columns.UUID(required=True)
    seat_row = columns.Integer(required=True)
    seat_column = columns.Integer(required=True)
    created_at = columns.DateTime(required=True)
