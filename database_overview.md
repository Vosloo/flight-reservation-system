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
    - id: integer
    - first_name: string
    - last_name: string

Primary key: id

---

- plane:
    - id: integer
    - name: string
    - seat_id: foreign key to "seat" **(only id)**

Primary key: id

---

- seat:
    - id: integer
    - plane_id: foreign key to "plane" (needed ???)
    - row: integer
    - column: integer
    - vacant: boolean

Primary key: ((id), row, column)

---

- flight:
    - id: integer
    - plane_id: foreign key to "plane"
    - departure_airport_id: foreign key to "airport"
    - arrival_airport_id: foreign key to "airport"
    - departure_time: datetime
    - arrival_time: datetime

Primary key: id

---

- airport:
    - id: integer
    - name: string
    - city: string
    - country: string

Primary key: id

---

- reservation:
    - id: integer
    - user_id: foreign key to "user"
    - flight_id: foreign key to "flight"
    - seat_id: foreign key to "seat" **(id, row, column)**
    - created_at: datetime

Primary key: id
