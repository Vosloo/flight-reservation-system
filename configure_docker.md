docker network create my_network_name

docker run --name cass1 --network my_network_name -d cassandra

docker run --name cass2 -d --network my_network_name -e CASSANDRA_SEEDS=cass1 cassandra

docker run --name cass3 -d --network my_network_name -e CASSANDRA_SEEDS=cass1 cassandra

docker run -it --network my_network_name --rm cassandra cqlsh cass1
