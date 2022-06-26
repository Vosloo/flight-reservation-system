from cassandra.cluster import Cluster, ResultSet


class Connector:
    def __init__(self) -> None:
        self._cluster = Cluster(["127.0.0.1"], port=9042)
        self._session = self._cluster.connect()

    def execute(self, query: str, *args) -> ResultSet:
        return self._session.execute(query, *args)

    def close(self) -> None:
        self._session.shutdown()
        self._cluster.shutdown()
