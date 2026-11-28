# main.py
# Author: Cam Lopez

from agent import SupportChatbot
from database import (
    all_orders,
    approve_request,
    create_tables,
    reject_request,
    waiting_requests,
)
from ollama_model import OllamaModel
from settings import DB_FILE, INSTRUCTIONS, MODEL_NAME
from tools import BeanTools

create_tables(DB_FILE)

bot = SupportChatbot(
    "BeanBot", INSTRUCTIONS, BeanTools(DB_FILE), OllamaModel(MODEL_NAME)
)

print("Welcome to The Bean Coffee Shop!")
print("Type a message, or type quit to stop.")

user_message = input("You: ")

while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")

print("\nStaff review")

for request in waiting_requests(DB_FILE):
    number = request["number"]

    print(
        f"Request {number}: Order {request['order_id']} "
        f"to quantity {request['new_quantity']}"
    )

    answer = input("Approve? yes or no: ")

    if answer == "yes":
        print(approve_request(DB_FILE, number))
    elif answer == "no":
        print(reject_request(DB_FILE, number))
    else:
        print(f"Request {number} is still waiting.")

print("\nCurrent customer orders")

for order in all_orders(DB_FILE):
    print(order["order_id"], order["item"], order["quantity"], order["status"])
