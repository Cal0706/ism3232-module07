# test_agent.py
# Author: Cam Lopez

import database
from agent import SupportChatbot
from fake_model import FakeModel
from fallback_model import FallbackModel
from keyword_model import KeywordModel
from tools import BeanTools


class SilentModel:
    """A model that never has an answer."""

    def decide(self, instructions, history, tools):
        return None


def make_bot(tmp_path, model):
    """Build a chatbot over a fresh database."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)

    return SupportChatbot(
        "BeanBot",
        "Be friendly.",
        BeanTools(db_file),
        model
    )


def ask_for_tool(name, arguments):
    """Build a decision when a model wants a tool."""
    return {"tool": name, "arguments": arguments}


def test_model_chosen_lookup_answers_from_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "look_up_order",
                {"order_id": "B101"}
            ),
            {"text": "Your order B101 is preparing."},
        ]
    )

    bot = make_bot(tmp_path, model)
    bot.respond("What is the status of order B101?")

    assert "B101" in bot.history[1]["content"]
    assert "preparing" in bot.history[1]["content"]


def test_made_up_quantity_never_reaches_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "request_quantity_change",
                {"order_id": "B101", "new_quantity": "5"}
            ),
            {"text": "What is the new quantity?"},
        ]
    )

    bot = make_bot(tmp_path, model)
    bot.respond("Please change the quantity on order B101")

    assert database.waiting_requests(bot.tools.db_file) == []
    assert database.find_order(
        bot.tools.db_file, "B101"
    )["quantity"] == 2
    