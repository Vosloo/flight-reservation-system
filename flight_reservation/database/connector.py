from cassandra.cluster import (
    EXEC_PROFILE_DEFAULT,
    Cluster,
    ExecutionProfile,
    PreparedStatement,
    ResultSet,
    Session,
    ConsistencyLevel,
)


class Connector:
    def __init__(self) -> None:
        profile = ExecutionProfile(
            consistency_level=ConsistencyLevel.ALL,
        )

        self._cluster = Cluster(
            ["127.0.0.1"], port=9042, execution_profiles={EXEC_PROFILE_DEFAULT: profile}
        )
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
