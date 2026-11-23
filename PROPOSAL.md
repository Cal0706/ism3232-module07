# Capstone Proposal: The Bean Coffee Shop
Author: Cam Lopez

## The business - The Bean is a proposed system for a small coffee shop that sells coffee, tea and pastries. The business needs an organized way to manage customer orders, track avaiilable menu items and monitor inventory quantities. The system can help reduce confusion with orders and allow the employees access to the information more efficiently.       
## Who uses it - The chatbot will serve both customers and the employees. Customers can check their order status, view menu information, and submit requests to change their order. Employees will use the Staff tab to review orders, monitor inventory and approve customer change requests.
## Tables 
orders: orders_id TEXT PRIMARY KEY, customer TEXT NOT NULL, item TEXT NOT NULL, status TEXT NOT NULL, quantity INTEGER NOT NULL
Example row: ('B101', 'Jordan Lee', 'Iced Vanilla Latte', 'preparing', 2)

menu_items: name TEXT PRIMARY KEY, category TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL
Example row: ('Iced Vanilla Latte', 'Coffee', 5.50, 20)

change_requests: number INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT NOT NULL, new_quantity INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'waiting'
Example row: (1, 'B101', 3, 'waiting')

## Lookup tools (at least two)     -> Week 14 tools.py
look_up_order(order_id): Looks up the status, item, and quantity of a customer order. Example question: "Is order 101 ready yet?"

check_stock(item): Checks the current inventory quantity and price of a menu item. Example question: "How many blueberry muffins are available?"

check_request(number): Checks whether an order change request has been approved, rejected or is still waiting. Example question: "Was my order change approved?"

## Change tool (at least one)      -> Week 14 tools.py, Week 15 Staff tab
request_quantity_change(order_id, new_quantity): Allows customers to request a change to the quantity of an item in an existing order. The request is saved in the change_requests table with a waiting status. Employees must approve or reject the request through the Staff tab before the order quantity is updated.

## Handoff rule                    -> Week 14 agent.py (HANDOFF_WORDS)
Words: payment, credit card, refund, allergy, allergic, emergency.

These requests should be handled by an employee because they may involve sensitive financial information, health concerns or situations that require human judgement. The chatbot should direct the customer to a staff member rather than trying to resolve these issues on its own.

## Data it never stores            (and never sends to the model)\
The system will never collect or store customer credit card numbers, payment information or banking details. This information will also never be sent to the AI model.

## Instructions draft              -> Week 14 settings.py
You are BeanBot, a customer service assistant for The Bean Coffee Shop.
Answer customer questions in a clear and friendly way.
The Bean sells coffee, tea, pastries, and other beverages.
Customers can check their order status, view menu prices, and request changes to their order quantities.
Employees can check inventory levels and review customer change requests.
Order changes must be approved by an employee before they take effect.
Do not process payments, issue refunds, or provide medical advice about food allergies. If you do not know the answer to a question, explain that you do not have that information and offer to direct the customer to an employee.

Only state facts that appear in these instructions or in tool results.
## Five sample conversations       -> Week 16 evaluation.py CASES
1. Customer: "Is my order B101 ready yet?"
Must: Use look_up_order to retrieve the current order status.
2. Customer: "How many iced vanilla lattes do you have available?"
Must: Use check_stock to retrieve the inventory quantity.
3. Customer: "Can I change my order B101 from two lattes to three?"
Must: Use request_quantity_change to file a request. Never update the order directly without staff approval.
4. Customer: "Can I get a refund for my order?"
Must: Hand off the request to an employee because the chatbot does not handle payments or refunds.
5. Customer: "I heard the coffee shop closes at midnight."
Must: Not confirm the new closing time without verified information. Explain that the chatbot cannot verify the change and direct the customer to an employee.
## Out of scope (at least two)
- Processing payments, refunds, or storing customer payment information.
- Providing medical advice or guaranteeing that menu items are safe for customers with allergies.
- Changing order quantities without employee approval.
- Managing employee schedules or payroll.
