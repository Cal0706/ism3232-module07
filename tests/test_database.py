import database


def make_db(tmp_path):
    """Create a fresh database with sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return db_file


def test_create_tables_twice_adds_no_duplicate_rows(tmp_path):
    db_file = make_db(tmp_path)

    database.create_tables(db_file)

    assert len(database.all_orders(db_file)) == 5
    assert len(database.all_items(db_file)) == 5


def test_find_order_needs_the_exact_id(tmp_path):
    db_file = make_db(tmp_path)

    assert database.find_order(db_file, "B101") is not None
    assert database.find_order(db_file, "B10") is None
    assert database.find_order(db_file, "B999") is None


def test_sql_in_an_order_id_is_just_text(tmp_path):
    db_file = make_db(tmp_path)

    result = database.find_order(
        db_file, "' OR 1=1 --"
    )

    assert result is None
    assert len(database.all_orders(db_file)) == 5


def test_change_requests_get_numbers_and_wait(tmp_path):
    db_file = make_db(tmp_path)

    number = database.add_change_request(
        db_file, "B101", 3
    )

    assert number == 1
    assert database.find_request(db_file, number)["status"] == "waiting"
    assert database.find_order(db_file, "B101")["quantity"] == 2
    assert len(database.waiting_requests(db_file)) == 1


def test_approve_changes_the_quantity_once(tmp_path):
    db_file = make_db(tmp_path)

    database.add_change_request(db_file, "B101", 3)

    assert database.approve_request(db_file, 1) == "Request 1 approved."
    assert database.find_order(db_file, "B101")["quantity"] == 3
    assert database.approve_request(db_file, 1) == "Request 1 is already approved."
    assert database.waiting_requests(db_file) == []


def test_reject_changes_nothing_and_cannot_be_approved_later(tmp_path):
    db_file = make_db(tmp_path)

    database.add_change_request(db_file, "B101", 4)

    assert database.reject_request(db_file, 1) == "Request 1 rejected."
    assert database.find_order(db_file, "B101")["quantity"] == 2
    assert database.approve_request(db_file, 1) == "Request 1 is already rejected."
    assert database.waiting_requests(db_file) == []
    