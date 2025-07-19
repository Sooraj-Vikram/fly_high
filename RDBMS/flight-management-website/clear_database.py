import sqlite3

def get_db_connection():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    return conn

def clear_database():
    conn = get_db_connection()
    try:
        # Begin a transaction
        conn.execute('BEGIN TRANSACTION;')

        # Delete all records from the tables
        conn.execute('DELETE FROM bookings;')
        conn.execute('DELETE FROM transactions;')
        conn.execute('DELETE FROM passengers;')
        conn.execute('DELETE FROM flights;')

        # Commit the transaction
        conn.commit()
        print("All records have been deleted successfully.")
    
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"An error occurred: {e}")
    
    finally:
        conn.close()

if __name__ == '__main__':
    clear_database()
