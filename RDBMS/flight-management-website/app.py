from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db',timeout=5)
    conn.row_factory = sqlite3.Row
    return conn

# Index Page
@app.route('/')
def index():
    return render_template('index.html')

# Flight Management Page
@app.route("/flight-management", methods=['GET', 'POST'])
def flight_management():
    conn = get_db_connection()
    if request.method == 'POST':
        flight_id = request.form['flight-id']
        airline_name = request.form['airline-name']
        departure = request.form['departure']
        destination = request.form['destination']
        departure_time = request.form['time']
        arrival_time = request.form['arrival-time']
        seats_available = int(request.form['seats-available'])
        ticket_price = float(request.form['ticket-price'])
        
        conn.execute('''INSERT INTO flights (flight_id, airline_name, departure, destination, departure_time, arrival_time, seats_available, ticket_price)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (flight_id, airline_name, departure, destination, departure_time, arrival_time, seats_available, ticket_price))
        conn.commit()
        return redirect(url_for('flight_management'))
    
    flights = conn.execute('SELECT * FROM flights').fetchall()
    conn.close()
    return render_template('flight-management.html', flights=flights)

# Passenger Management Page
@app.route('/passenger-management', methods=['GET', 'POST'])
def passenger_management():
    conn = get_db_connection()
    if request.method == 'POST':
        customer_id = request.form['customer-id']
        passenger_name = request.form['passenger-name']
        contact_number = request.form['contact-number']
        email = request.form['email']
        
        conn.execute('''INSERT INTO passengers (customer_id, passenger_name, contact_number, email, flight_id)
                        VALUES (?, ?, ?, ?, ?)''', 
                        (customer_id, passenger_name, contact_number, email, None))  # Flight ID set to None initially
        conn.commit()
        return redirect(url_for('passenger_management'))
    
    passengers = conn.execute('SELECT * FROM passengers').fetchall()
    conn.close()
    return render_template('passenger-management.html', passengers=passengers)

# Booking Page (Book or Cancel Tickets)
@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    conn = get_db_connection()
    if request.method == 'POST':
        action = request.form.get('action', 'book')
        customer_id = request.form['customer-id']
        flight_id = request.form['flight-id']
        transaction_mode = request.form.get('transaction_mode')

        if action == 'book':
            # Get the ticket price from the flights table
            flight = conn.execute('SELECT ticket_price FROM flights WHERE flight_id = ?', (flight_id,)).fetchone()
            if flight is None:
                return "Flight not found", 404
            
            ticket_cost = flight['ticket_price']

            conn.execute('''INSERT INTO bookings (customer_id, flight_id, transaction_mode, seats_booked)
                            VALUES (?, ?, ?, 1)''', 
                            (customer_id, flight_id, transaction_mode))
            conn.execute('UPDATE flights SET seats_available = seats_available - 1 WHERE flight_id = ?', 
                         (flight_id,))
            # Update the passenger's flight_id
            conn.execute('UPDATE passengers SET flight_id = ? WHERE customer_id = ?', (flight_id, customer_id))

            # Insert into transactions table when booking
            conn.execute('''INSERT INTO transactions (customer_id, flight_id, ticket_cost, transaction_mode)
                            VALUES (?, ?, ?, ?)''', 
                            (customer_id, flight_id, ticket_cost, transaction_mode))
        
        elif action == 'cancel':
            conn.execute('DELETE FROM bookings WHERE customer_id = ? AND flight_id = ?', (customer_id, flight_id))
            conn.execute('UPDATE flights SET seats_available = seats_available + 1 WHERE flight_id = ?', 
                         (flight_id,))
            # Update the passenger's flight_id to None
            conn.execute('UPDATE passengers SET flight_id = NULL WHERE customer_id = ?', (customer_id,))

            # Insert into transactions table when cancelling
            conn.execute('''INSERT INTO transactions (customer_id, flight_id, ticket_cost, transaction_mode)
                            VALUES (?, ?, 0, 'Cancellation')''', 
                            (customer_id, flight_id))

        conn.commit()
        return redirect(url_for('bookings'))

    bookings = conn.execute('''SELECT b.customer_id, b.flight_id, f.departure, f.destination, b.transaction_mode
                                FROM bookings b
                                JOIN flights f ON b.flight_id = f.flight_id''').fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

# Transaction Management Page
@app.route('/transaction-management')
def transaction_management():
    conn = get_db_connection()
    transactions = conn.execute('''SELECT t.customer_id, p.passenger_name AS customer_name, t.flight_id, t.ticket_cost, t.transaction_mode
                                   FROM transactions t
                                   JOIN passengers p ON t.customer_id = p.customer_id''').fetchall()
    conn.close()
    return render_template('transaction-management.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
