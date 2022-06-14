<h1>Database overview</h1>

<h2>Tables:</h2>

<ol>
    <li>user</li>
    <li>plane</li>
    <li>seat</li>
    <li>flight</li>
    <li>airport</li>
    <li>reservation</li>
</ol>

---

<h2>Tables overview:</h2>


- user:
    - id: uuid
    - first_name: string
    - last_name: string

Primary key: id

---

- plane:
    - id: uuid
    - name: string
    - seat_id: foreign key to "seat"

Primary key: id

---

- seat:
    - id: uuid
    - row: integer
    - column: integer
    - is_vacant: boolean

Primary key: ((id), row, column)

---

- flight:
    - id: uuid
    - plane_id: foreign key to "plane"
    - departure_airport_id: foreign key to "airport"
    - arrival_airport_id: foreign key to "airport"

Primary key: id

---

- airport:
    - id: uuid
    - name: string
    - city: string
    - country: string

Primary key: id

---

- reservation:
    - id: uuid
    - user_id: foreign key to "user"
    - flight_id: foreign key to "flight"
    - seat_id: foreign key to "seat:id"
    - seat_row: foreign key to "seat:row"
    - seat_column: foreign key to "seat:column"
    - created_at: datetime

Primary key: id
