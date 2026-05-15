import sqlite3
from flask import Flask, render_template, request, redirect

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

@app.route('/buy', methods=['GET', 'POST'])
def buy_ticket():
    error_message = None
    conn = get_db_connection()
    
    if request.method == 'POST':
        # Fetch form data (Notice we no longer ask for the price!)
        user_id_str = request.form.get('user_id')
        event_id_str = request.form.get('event_id')

        if not user_id_str or not event_id_str:
            error_message = "Please select both a user and an event."
        else:
            try:
                user_id = int(user_id_str)
                event_id = int(event_id_str)
                
                # Securely fetch the true base price from the database
                event = conn.execute('SELECT ticket_price FROM Events WHERE event_id = ?', (event_id,)).fetchone()
                
                if not event:
                    error_message = "Invalid event selected."
                else:
                    # The server dictates the price, not the user!
                    base_price = event['ticket_price']
                    tax_amount = base_price * 0.10 
                    
                    # Transaction Logic
                    try:
                        conn.execute('BEGIN TRANSACTION')
                        
                        conn.execute('''
                            INSERT INTO Tickets (user_id, event_id, purchase_date, base_price, tax_amount, record_inserted_by)
                            VALUES (?, ?, date('now'), ?, ?, 'web_user')
                        ''', (user_id, event_id, base_price, tax_amount))
                        
                        conn.execute('''
                            UPDATE Events 
                            SET last_updated_at = CURRENT_TIMESTAMP 
                            WHERE event_id = ?
                        ''', (event_id,))
                        
                        conn.commit()
                        conn.close()
                        return redirect('/dashboard')
                        
                    except sqlite3.Error as e:
                        conn.rollback()
                        error_message = f"Database error during transaction: {e}"

            except ValueError:
                error_message = "Invalid input detected."

    # For GET requests: Fetch lists to populate our dropdown menus
    users = conn.execute('SELECT user_id, first_name, last_name FROM Users').fetchall()
    events = conn.execute('SELECT event_id, event_name, ticket_price FROM Events').fetchall()
    conn.close()

    return render_template('buy_ticket.html', users=users, events=events, error=error_message)

# Run the application in debug mode
if __name__ == '__main__':
    # Debug=True means the server will auto-reload upon change
    app.run(debug=True)
