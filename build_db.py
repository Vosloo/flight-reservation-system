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


def create_user(connector: Connector) -> list:
    print("Creating user table...")
    user_ids = []
    connector.execute("DROP TABLE IF EXISTS flight_reservation.user")
    connector.execute(
        "CREATE TABLE flight_reservation.user "
        "(id uuid, first_name text, last_name text, PRIMARY KEY(id))"
    )

    for person in product(FIRST_NAMES, SECOND_NAMES):
        first_name, last_name = person
        user_id = uuid.uuid1()
        user_ids.append(user_id)
        cql = "INSERT INTO flight_reservation.user (id, first_name, last_name) VALUES (%s, %s, %s)"
        vals = [user_id, first_name, last_name]
        connector.execute(cql, vals)

    return user_ids


def create_plane(connector: Connector) -> list:
    print("Creating plane table...")
    plane_ids = []
    connector.execute("DROP TABLE IF EXISTS flight_reservation.plane")
    connector.execute("CREATE TABLE flight_reservation.plane (id uuid, name text, PRIMARY KEY(id))")

    cql = "INSERT INTO flight_reservation.plane (id, name) VALUES (%s, %s)"
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
    connector.execute("DROP TABLE IF EXISTS flight_reservation.airport")
    connector.execute(
        "CREATE TABLE flight_reservation.airport "
        "(id uuid, name text, city text, country text, PRIMARY KEY(id))"
    )

    cql = "INSERT INTO flight_reservation.airport (id, name, city, country) VALUES (%s, %s, %s, %s)"
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
    connector.execute("DROP TABLE IF EXISTS flight_reservation.flight")
    connector.execute(
        "CREATE TABLE flight_reservation.flight "
        "(id uuid, plane_id uuid, departure_airport_id uuid, arrival_airport_id uuid, "
        "PRIMARY KEY((id), plane_id))"
    )

    cql = (
        "INSERT INTO flight_reservation.flight "
        "(id, plane_id, departure_airport_id, arrival_airport_id) VALUES (%s, %s, %s, %s)"
    )
    for ind, dep_arr in enumerate(combinations(airport_ids, 2)):
        flight_id = uuid.uuid1()
        flight_ids.append(flight_id)
        departure_airport_id, arrival_airport_id = dep_arr
        plane_id = plane_ids[ind % len(plane_ids)]

        vals = [flight_id, departure_airport_id, arrival_airport_id, plane_id]
        connector.execute(cql, vals)

    return flight_ids


def create_seat(connector: Connector, flight_ids: list) -> None:
    print("Creating seat table...")
    connector.execute("DROP TABLE IF EXISTS flight_reservation.seat")
    connector.execute(
        "CREATE TABLE flight_reservation.seat "
        "(flight_id uuid, row int, column int, is_vacant boolean, "
        "PRIMARY KEY((flight_id), row, column))"
    )

    cql = (
        "INSERT INTO flight_reservation.seat (flight_id, row, column, is_vacant) VALUES "
        "(%(flight_id)s, %(row)s, %(column)s, %(is_vacant)s)"
    )
    for flight_id in flight_ids:
        for row, column in product(range(1, 11), range(1, 7)):
            vals = {
                "flight_id": flight_id,
                "row": row,
                "column": column,
                "is_vacant": True,
            }
            connector.execute(cql, vals)


def create_reservation(connector: Connector) -> None:
    print("Creating reservation table...")
    connector.execute("DROP TABLE IF EXISTS flight_reservation.reservation")
    connector.execute(
        "CREATE TABLE flight_reservation.reservation "
        "(user_id uuid, flight_id uuid, id uuid, seat_row int, seat_col int, created_at timestamp, "
        "PRIMARY KEY(user_id, flight_id, id))"
    )


if __name__ == "__main__":
    connector = Connector()

    try:
        create_keyspace(connector)
        user_ids = create_user(connector)
        plane_ids = create_plane(connector)
        airport_ids = create_airport(connector)
        flight_ids = create_flight(connector, airport_ids, plane_ids)
        create_seat(connector, flight_ids)
        create_reservation(connector)
    except Exception as e:
        print("Error while setting up the database:")
        print(e)
        raise e
    finally:
        print("Closing connection...")
        connector.close()

    print("Database created")
