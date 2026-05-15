import sqlite3

def initialize_database():
    conn = sqlite3.connect('event_ticketing.db')
    cursor = conn.cursor()

    print("Initializing DBs")

    # USERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # EVENTS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            event_id INTEGER PRIMARY KEY,
            event_name TEXT NOT NULL,
            event_date DATE NOT NULL,
            ticket_price REAL NOT NULL,
            last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # TICKETS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            ticket_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            event_id INTEGER,
            purchase_date DATE,
            base_price REAL,
            tax_amount REAL,
            record_inserted_by TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (event_id) REFERENCES Events(event_id)
        )
    ''')

    # INSERT DUMMY DATA
    # IGNORE is to prevent crashes
    cursor.executemany('''
        INSERT OR IGNORE INTO Users (user_id, first_name, last_name, email) 
        VALUES (?, ?, ?, ?)
    ''', [
        (1, 'Alice', 'Smith', 'alice@email.com'),
        (2, 'Bob', 'Jones', 'bob@email.com'),
        (3, 'Charlie', 'Brown', 'charlie@email.com')
    ])

    cursor.executemany('''
        INSERT OR IGNORE INTO Events (event_id, event_name, event_date, ticket_price) 
        VALUES (?, ?, ?, ?)
    ''', [
        (101, 'Summer Music Fest', '2026-07-15', 50.00),
        (102, 'Tech Conference 2026', '2026-09-10', 150.00)
    ])

    cursor.executemany('''
        INSERT OR IGNORE INTO Tickets (ticket_id, user_id, event_id, purchase_date, base_price, tax_amount, record_inserted_by) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        (1001, 1, 101, '2026-04-01', 50.00, 5.00, 'system_admin'),
        (1002, 2, 101, '2026-04-02', 50.00, 5.00, 'system_admin'),
        (1003, 3, 102, '2026-04-03', 150.00, 15.00, 'system_admin')
    ])

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Run the function if this script is executed directly
if __name__ == '__main__':
    initialize_database()
