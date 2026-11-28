# keyword_model.py
# Author: Cam Lopez


class KeywordModel:
    """A stand-in model that decides with keyword rules."""

    def decide(self, instructions, history, tools):
        """Return a reply or a tool request."""
        last = history[-1]

        if last["role"] == "tool":
            return {"text": last["content"]}

        text = last["content"].lower()

        if "order" in text:
            return {"tool": "look_up_order", "arguments": {"order_id": last["content"]}}

        if any(
            word in text
            for word in (
                "stock",
                "available",
                "price",
                "inventory",
                "how many",
                "how much",
            )
        ):
            return {"tool": "check_stock", "arguments": {"item": last["content"]}}

        if "hello" in text or text.strip() == "hi":
            return {
                "text": "Hello! Welcome to The Bean Coffee Shop. How can I help you today?"
            }

        return {
            "text": "I'm not sure how to help with that. I can check your order status or menu item availability."
        }
