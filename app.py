import sqlite3
from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('event_ticketing.db')
    conn.row_factory = sqlite3.Row #access columns by name
    return conn

# Basic route to verify the server is running
@app.route('/')
def home():
    # Open connection
    conn = get_db_connection()
    
    # Query the database for all events
    events = conn.execute('SELECT * FROM Events ORDER BY event_date ASC').fetchall()
    
    # Close connection
    conn.close()
    
    # Pass the data to our HTML template
    return render_template('index.html', events=events)

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    
    # Note: We calculate total_price dynamically here to maintain 3NF
    overall_stats = conn.execute('''
        SELECT 
            COUNT(ticket_id) as total_tickets,
            SUM(base_price + tax_amount) as total_revenue,
            AVG(base_price + tax_amount) as avg_ticket_price
        FROM Tickets
    ''').fetchone()

    event_stats = conn.execute('''
        SELECT 
            e.event_name, 
            COUNT(t.ticket_id) as tickets_sold, 
            COALESCE(SUM(t.base_price + t.tax_amount), 0) as revenue 
        FROM Events e 
        LEFT JOIN Tickets t ON e.event_id = t.event_id 
        GROUP BY e.event_id
    ''').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', stats=overall_stats, event_stats=event_stats)

# Run the application in debug mode
if __name__ == '__main__':
    # Debug=True means the server will auto-reload upon change
    app.run(debug=True)
