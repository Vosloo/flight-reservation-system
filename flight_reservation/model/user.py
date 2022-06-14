from uuid import uuid4
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class User(Model):
    __table_name__ = 'user'

    id = columns.UUID(primary_key=True, default=lambda: uuid4())
    first_name = columns.Text(required=True)
    last_name = columns.Text(required=True)
