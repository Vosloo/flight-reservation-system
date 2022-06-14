from uuid import uuid4

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Seat(Model):
    __table_name__ = "seat"

    id = columns.UUID(partition_key=True, default=lambda: uuid4())  # partition_key
    row = columns.Integer(primary_key=True, required=True)  # cluster_key
    column = columns.Integer(primary_key=True, required=True)  # cluster_key
    is_vacant = columns.Boolean(required=True)
