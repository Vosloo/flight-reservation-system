#!/usr/bin/env python

import uuid
from itertools import combinations, product

from flight_reservation.database import Connector

CITIES = ["Lublin", "Warszawa", "Poznan", "Krakow", "Gdansk", "Radom", "Wroclaw", "Lodz", "Katowice"]
FIRST_NAMES = ["John", "Marek", "Jerzy", "Klaus", "Wojtek", "Dawid", "Eustachy", "Diego", "Luther"]
SECOND_NAMES = [
    "Kenedy",
    "Obama",
    "Kowalski",
    "Trump",
    "Piekarski",
    "Szymczak",
    "Patyk",
    "Piaseczny",
    "Grzyb",
    "Kloc",
]
PLANE_NAMES = ["Galczynski", "Syrenka", "Balczewski", "Sokol", "Kalista", "Stoch"]


def create_keyspace(connector: Connector) -> None:
    print("Creating keyspace...")
    connector.execute("DROP KEYSPACE IF EXISTS flight_reservation")
    connector.execute(
        "CREATE KEYSPACE IF NOT EXISTS flight_reservation "
        "WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }"
    )
    connector.execute("USE flight_reservation")


def create_user(connector: Connector) -> list:
    print("Creating user table...")
    user_ids = []
    connector.execute("DROP TABLE IF EXISTS user")
    connector.execute("CREATE TABLE user (id uuid, first_name text, last_name text, PRIMARY KEY(id))")

    for person in product(FIRST_NAMES, SECOND_NAMES):
        first_name, last_name = person
        user_id = uuid.uuid1()
        user_ids.append(user_id)
        cql = "INSERT INTO user (id, first_name, last_name) VALUES (%s, %s, %s)"
        vals = [user_id, first_name, last_name]
        connector.execute(cql, vals)

    return user_ids


def create_plane(connector: Connector) -> list:
    print("Creating plane table...")
    plane_ids = []
    connector.execute("DROP TABLE IF EXISTS plane")
    connector.execute("CREATE TABLE plane (id uuid, name text, PRIMARY KEY(id))")

    cql = "INSERT INTO plane (id, name) VALUES (%s, %s)"
    for plane in range(6):
        plane_id = uuid.uuid1()
        plane_ids.append(plane_id)
        name = PLANE_NAMES[plane]
        vals = [plane_id, name]
        connector.execute(cql, vals)

    return plane_ids


def create_airport(connector: Connector) -> list:
    print("Creating airport table...")
    airport_ids = []
    connector.execute("DROP TABLE IF EXISTS airport")
    connector.execute(
        "CREATE TABLE airport (id uuid, name text, city text, country text, PRIMARY KEY(id))"
    )

    cql = "INSERT INTO airport (id, name, city, country) VALUES (%s, %s, %s, %s)"
    for airport in CITIES:
        airport_id = uuid.uuid1()
        airport_ids.append(airport_id)
        city_name = airport
        airport_name = city_name + "_airport"
        vals = [airport_id, airport_name, city_name, "Poland"]
        connector.execute(cql, vals)

    return airport_ids


def create_flight(connector: Connector, airport_ids: list, plane_ids: list) -> list:
    print("Creating flight table...")
    flight_ids = []
    connector.execute("DROP TABLE IF EXISTS flight")
    connector.execute(
        "CREATE TABLE flight "
        "(id uuid, plane_id uuid, departure_airport_id uuid, arrival_airport_id uuid, PRIMARY KEY(id))"
    )

    cql = (
        "INSERT INTO flight (id, plane_id, departure_airport_id, arrival_airport_id) "
        "VALUES (%s, %s, %s, %s)"
    )
    for ind, dep_arr in enumerate(combinations(airport_ids, 2)):
        flight_id = uuid.uuid1()
        flight_ids.append(flight_id)
        departure_airport_id, arrival_airport_id = dep_arr
        plane_id = plane_ids[ind % len(plane_ids)]

        vals = [flight_id, departure_airport_id, arrival_airport_id, plane_id]
        connector.execute(cql, vals)

    return flight_ids


def create_seat(connector: Connector, plane_ids: list) -> None:
    print("Creating seat table...")
    connector.execute("DROP TABLE IF EXISTS seat")
    connector.execute(
        "CREATE TABLE seat "
        "(plane_id uuid, row int, column int, is_vacant boolean, PRIMARY KEY((plane_id), row, column))"
    )

    cql = (
        "INSERT INTO seat (plane_id, row, column, is_vacant) VALUES "
        "(%(plane_id)s, %(row)s, %(column)s, %(is_vacant)s)"
    )
    for plane_id in plane_ids:
        for row in range(10):
            for col in range(6):
                vals = {"plane_id": plane_id, "row": row, "column": col, "is_vacant": True}
                connector.execute(cql, vals)


def create_reservation(connector: Connector) -> None:
    print("Creating reservation table...")
    connector.execute("DROP TABLE IF EXISTS reservation")
    connector.execute(
        "CREATE TABLE reservation "
        "(id uuid, user_id uuid, flight_id uuid, seat_id uuid, "
        "seat_row int, seat_col int, created_at timestamp, PRIMARY KEY(id))"
    )


if __name__ == "__main__":
    connector = Connector()

    try:
        create_keyspace(connector)
        user_ids = create_user(connector)
        plane_ids = create_plane(connector)
        airport_ids = create_airport(connector)
        flight_ids = create_flight(connector, airport_ids, plane_ids)
        create_seat(connector, plane_ids)
        create_reservation(connector)
    except Exception as e:
        print("Error while setting up the database:")
        print(e)
        raise e
    finally:
        connector.close()

    print("Database created")
