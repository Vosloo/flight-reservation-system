<h1> Flight reservation system </h1>


<h2> About </h2>

Flight reservation system using Python and Cassandra

<h2> Docker </h2>

Build the image with (replace <image_name> with the desired image name):

```bash
docker build -t <image_name> .
```

To set up nodes (please wait for a few seconds between creating nodes):

```bash
docker network create cassandra_network
docker run --name cas1 --network cassandra_network -d <image_name>
docker run --name cas2 -d --network cassandra_network -e CASSANDRA_SEEDS=cas1 <image_name>
docker run --name cas3 -d --network cassandra_network -e CASSANDRA_SEEDS=cas1 <image_name>
```

To run the cqlsh run:

```bash
docker run -it --network cassandra_network --rm <image_name> cqlsh cas1
```
