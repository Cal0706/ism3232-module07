-- The Bean Coffee Shop Database

-- Table 1: Customer Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer TEXT NOT NULL,
    item TEXT NOT NULL,
    status TEXT NOT NULL,
    quantity INTEGER NOT NULL
);

-- Table 2: Menu Items
CREATE TABLE IF NOT EXISTS menu_items (
    name TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

-- Table 3: Change Requests
CREATE TABLE IF NOT EXISTS change_requests (
    number INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    new_quantity INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'waiting'
);

-- Sample Customer Orders
INSERT OR IGNORE INTO orders
(order_id, customer, item, status, quantity)
VALUES
('B101', 'Jordan Lee', 'Iced Vanilla Latte', 'preparing', 2),
('B102', 'Taylor Smith', 'Blueberry Muffin', 'ready', 1),
('B103', 'Alex Rivera', 'Caramel Macchiato', 'pending', 2),
('B104', 'Sam Wilson', 'Iced Coffee', 'ready', 1),
('B105', 'Jamie Brown', 'Chocolate Croissant', 'preparing', 3);

-- Sample Menu Items and Inventory
INSERT OR IGNORE INTO menu_items
(name, category, price, stock)
VALUES
('Iced Vanilla Latte', 'Coffee', 5.50, 20),
('Blueberry Muffin', 'Pastry', 3.50, 12),
('Caramel Macchiato', 'Coffee', 5.75, 15),
('Iced Coffee', 'Coffee', 3.75, 25),
('Chocolate Croissant', 'Pastry', 4.25, 8);
