from cassandra.cluster import Cluster, PreparedStatement, ResultSet, Session

KEYSPACE = "flight_reservation"


class Connector:
    def __init__(self) -> None:
        self._cluster = Cluster(["127.0.0.1"], port=9042)
        self._session: Session = self._cluster.connect()

    def prepare(self, query: str) -> PreparedStatement:
        return self._session.prepare(query)

    def execute(self, query: str, *args) -> ResultSet:
        return self._session.execute(query, *args)

    def close(self) -> None:
        self._session.shutdown()
        self._cluster.shutdown()

    def __del__(self) -> None:
        self.close()
