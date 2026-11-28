# database.py
# Author: Cam Lopez

import sqlite3


def query_all(db_file, sql, values=()):
    """Run a SELECT and return every row as a dictionary."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, values).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def query_one(db_file, sql, values=()):
    """Run a SELECT and return the first row as a dictionary, or None."""
    rows = query_all(db_file, sql, values)
    if rows == []:
        return None
    return rows[0]


def change(db_file, sql, values=()):
    """Run an INSERT or UPDATE, save it, and return the ID of the last row inserted."""
    conn = sqlite3.connect(db_file)
    cursor = conn.execute(sql, values)
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def create_tables(db_file):
    """Create the tables and the sample rows, unless they are already there."""
    with open("schema.sql") as f:
        script = f.read()
    conn = sqlite3.connect(db_file)
    conn.executescript(script)
    conn.commit()
    conn.close()


def find_order(db_file, order_id):
    """Find a customer order by its ID."""
    return query_one(db_file, "SELECT * FROM orders WHERE order_id = ?", (order_id,))


def find_item(db_file, name):
    """Find a menu item by its name."""
    return query_one(db_file, "SELECT * FROM menu_items WHERE name = ?", (name,))


def item_names(db_file):
    """Return all menu item names."""
    rows = query_all(db_file, "SELECT name FROM menu_items ORDER BY name")
    return [row["name"] for row in rows]


def add_change_request(db_file, order_id, new_quantity):
    """Submit a request to change an order quantity."""
    if find_order(db_file, order_id) is None:
        raise ValueError("Order not found.")

    if type(new_quantity) is not int or new_quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")

    return change(
        db_file,
        """INSERT INTO change_requests
        (order_id, new_quantity)
        VALUES (?, ?)""",
        (order_id, new_quantity),
    )


def find_request(db_file, number):
    """Find a change request by its number."""
    return query_one(
        db_file, "SELECT * FROM change_requests WHERE number = ?", (number,)
    )


def waiting_requests(db_file):
    """Return all requests waiting for approval."""
    return query_all(
        db_file,
        """SELECT * FROM change_requests
        WHERE status = ? ORDER BY number""",
        ("waiting",),
    )


def approve_request(db_file, number):
    """Approve a request and update the order quantity."""
    with sqlite3.connect(db_file) as conn:
        conn.execute("BEGIN IMMEDIATE")
        conn.row_factory = sqlite3.Row

        request = conn.execute(
            "SELECT * FROM change_requests WHERE number = ?", (number,)
        ).fetchone()

        if request is None:
            return f"Request {number} not found."

        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."

        conn.execute(
            "UPDATE orders SET quantity = ? WHERE order_id = ?",
            (request["new_quantity"], request["order_id"]),
        )

        conn.execute(
            "UPDATE change_requests SET status = ? WHERE number = ?",
            ("approved", number),
        )

    return f"Request {number} approved."


def reject_request(db_file, number):
    """Reject a request without changing the order."""
    with sqlite3.connect(db_file) as conn:
        conn.execute("BEGIN IMMEDIATE")
        conn.row_factory = sqlite3.Row

        request = conn.execute(
            "SELECT * FROM change_requests WHERE number = ?", (number,)
        ).fetchone()

        if request is None:
            return f"Request {number} not found."

        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."

        conn.execute(
            "UPDATE change_requests SET status = ? WHERE number = ?",
            ("rejected", number),
        )

    return f"Request {number} rejected."


def all_orders(db_file):
    """Return all customer orders."""
    return query_all(db_file, "SELECT * FROM orders ORDER BY order_id")


def all_items(db_file):
    """Return all menu items and inventory."""
    return query_all(db_file, "SELECT * FROM menu_items ORDER BY name")
