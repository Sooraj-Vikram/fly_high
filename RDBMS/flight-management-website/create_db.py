import sqlite3

# Connect to the database (this will create `database.db` if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create flights table
cursor.execute('''
CREATE TABLE IF NOT EXISTS flights (
    flight_id TEXT PRIMARY KEY,
    airline_name TEXT,
    departure TEXT,
    destination TEXT,
    departure_time TEXT,
    arrival_time TEXT,
    seats_available INTEGER,
    ticket_price REAL
)
''')

# Create passengers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS passengers (
    customer_id TEXT PRIMARY KEY,
    passenger_name TEXT,
    contact_number TEXT,
    email TEXT,
    flight_id TEXT,
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
)
''')

# Create bookings table, with an additional `transaction_mode` field
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    flight_id TEXT,
    seats_booked INTEGER,
    transaction_mode TEXT,  -- New field for mode of transaction
    FOREIGN KEY (customer_id) REFERENCES passengers(customer_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
)
''')

# Create transactions table with the additional `customer_name` field
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    flight_id TEXT,
    customer_name TEXT,
    ticket_cost REAL,
    transaction_mode TEXT,
    FOREIGN KEY (customer_id) REFERENCES passengers(customer_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully with all required tables.")
