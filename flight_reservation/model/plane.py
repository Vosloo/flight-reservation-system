from uuid import uuid4

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Plane(Model):
    __table_name__ = "plane"

    id = columns.UUID(primary_key=True, default=lambda: uuid4())
    name = columns.Text(required=True)
    seat_id = columns.UUID(required=True)
