from uuid import uuid4

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Airport(Model):
    __table_name__ = "airport"

    id = columns.UUID(primary_key=True, default=lambda: uuid4())
    name = columns.Text(required=True)
    city = columns.Text(required=True)
    country = columns.Text(required=True)
