import database
from tools import BeanTools


def make_tools(tmp_path):
    """Build tools over a fresh database."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return BeanTools(db_file)


def customer(text):
    """Build a history containing one customer message."""
    return [{"role": "user", "content": text}]


def test_lookup_finds_id_inside_sentence(tmp_path):
    tools = make_tools(tmp_path)

    reply = tools.run(
        "look_up_order",
        {"order_id": "Is order B101 ready?"},
        customer("Is order B101 ready?")
    )

    assert "B101" in reply
    assert "preparing" in reply


def test_quantity_change_waits_for_approval(tmp_path):
    tools = make_tools(tmp_path)

    reply = tools.run(
        "request_quantity_change",
        {"order_id": "B101", "new_quantity": "3"},
        customer("Change order B101 to 3.")
    )

    assert "Request 1" in reply
    assert "has not changed" in reply

    order = database.find_order(tools.db_file, "B101")
    assert order["quantity"] == 2

    request = database.find_request(tools.db_file, 1)
    assert request["status"] == "waiting"


def test_unknown_tool_is_refused(tmp_path):
    tools = make_tools(tmp_path)

    reply = tools.run(
        "delete_order",
        {},
        customer("Delete my order.")
    )

    assert "There is no tool named" in reply


def test_missing_order_id_is_refused(tmp_path):
    tools = make_tools(tmp_path)

    reply = tools.run(
        "look_up_order",
        {},
        customer("Where is my order?")
    )

    assert "missing" in reply


def test_made_up_order_id_is_refused(tmp_path):
    tools = make_tools(tmp_path)

    reply = tools.run(
        "look_up_order",
        {"order_id": "B101"},
        customer("Where is my order?")
    )

    assert "has not given that order ID" in reply


def test_check_stock_returns_inventory(tmp_path):
    tools = make_tools(tmp_path)

    reply = tools.run(
        "check_stock",
        {"item": "Iced Vanilla Latte"},
        customer("How many Iced Vanilla Latte are available?")
    )

    assert "20" in reply
    assert "$5.50" in reply


def test_check_request_returns_waiting_status(tmp_path):
    tools = make_tools(tmp_path)

    database.add_change_request(
        tools.db_file, "B101", 3
    )

    reply = tools.run(
        "check_request",
        {"number": "1"},
        customer("What happened to request 1?")
    )

    assert "waiting" in reply
    