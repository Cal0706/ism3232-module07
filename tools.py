# tools.py
# Author: Cam Lopez

import database


class BeanTools:
    """The tools the model may ask for."""

    def __init__(self, db_file):
        self.db_file = db_file

    def tool_list(self):
        """Return the tools the model may ask for."""
        return [
            self.look_up_order,
            self.check_stock,
            self.request_quantity_change,
            self.check_request,
        ]

    def look_up_order(self, order_id):
        """Look up the status, item, and quantity of an order.

        Args:
            order_id: The order ID, like B101.
        """
        for word in order_id.upper().split():
            order = database.find_order(self.db_file, word.strip("?.!,#"))

            if order is not None:
                return (
                    f"Order {order['order_id']} is "
                    f"{order['status']}. "
                    f"Item: {order['item']}. "
                    f"Quantity: {order['quantity']}."
                )

        return "No order with that ID was found. Order IDs look like B101."

    def check_stock(self, item):
        """Check the inventory and price of a menu item.

        Args:
            item: The menu item name, like Iced Vanilla Latte.
        """
        for name in database.item_names(self.db_file):
            if self.words(name) in self.words(item):
                product = database.find_item(self.db_file, name)

                stock = product["stock"]
                price = product["price"]

                return f"We have {stock} of the {name} in stock, at ${price:.2f} each."

        return "That menu item was not found."

    def request_quantity_change(self, order_id, new_quantity):
        """Ask staff to change the quantity of an order.

        Args:
            order_id: The order ID, like B101.
            new_quantity: The requested new quantity.
        """
        order_id = order_id.upper()

        if database.find_order(self.db_file, order_id) is None:
            return "No order with that ID was found."

        try:
            quantity = int(str(new_quantity))
        except ValueError:
            return "The quantity must be a positive whole number."

        if quantity <= 0:
            return "The quantity must be a positive whole number."

        try:
            number = database.add_change_request(self.db_file, order_id, quantity)
        except OverflowError:
            return "That quantity is too large."

        return f"Request {number} was sent to staff. The quantity has not changed yet."

    def check_request(self, number):
        """Check what staff decided about a quantity change.

        Args:
            number: The request number, like 3.
        """
        try:
            request = database.find_request(self.db_file, int(number))
        except ValueError:
            return "Request numbers look like 3."
        except OverflowError:
            return f"There is no request {number}."

        if request is None:
            return f"There is no request {number}."

        order_id = request["order_id"]

        if request["status"] == "waiting":
            return (
                f"Request {number} for order {order_id} is waiting for staff approval."
            )

        return f"Request {number} for order {order_id} was {request['status']}."

    def run(self, name, arguments, history):
        """Run a tool only if every check passes."""

        if name == "look_up_order":
            order_id = self.clean(arguments, "order_id")

            if order_id == "":
                return "The order ID is missing. Ask the customer for it."

            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID. Ask them for it."

            return self.look_up_order(order_id)

        if name == "check_stock":
            item = self.clean(arguments, "item")

            if item == "":
                return "The menu item is missing. Ask the customer for it."

            return self.check_stock(item)

        if name == "request_quantity_change":
            order_id = self.clean(arguments, "order_id")
            new_quantity = self.clean(arguments, "new_quantity")

            if order_id == "" or new_quantity == "":
                return "The order ID and new quantity are both needed."

            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID. Ask them for it."

            quantity_words = {
                "1": "one",
                "2": "two",
                "3": "three",
                "4": "four",
                "5": "five",
                "6": "six",
                "7": "seven",
                "8": "eight",
                "9": "nine",
                "10": "ten",
            }

            word = quantity_words.get(new_quantity, new_quantity)

            if not (
                self.customer_said(history, new_quantity)
                or self.customer_said(history, word)
            ):
                return "The customer has not given that quantity. Ask them for it."

            return self.request_quantity_change(order_id, new_quantity)

        if name == "check_request":
            number = self.clean(arguments, "number")

            if number == "":
                return "The request number is missing. Ask the customer for it."

            if not self.customer_said(history, number):
                return (
                    "The customer has not given that request number. Ask them for it."
                )

            return self.check_request(number)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces."""
        return str(arguments.get(key, "")).strip()

    def words(self, text):
        """Return text in lower case as whole words."""
        cleaned = []

        for word in text.lower().split():
            cleaned.append(word.strip("?.!,#"))

        return " " + " ".join(cleaned) + " "

    def customer_said(self, history, text):
        """Return True if the customer typed text as whole words."""
        wanted = self.words(text)

        for message in history:
            if message["role"] == "user" and wanted in self.words(message["content"]):
                return True

        return False
