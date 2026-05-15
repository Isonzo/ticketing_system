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
# Run the application in debug mode
if __name__ == '__main__':
    # Debug=True means the server will auto-reload upon change
    app.run(debug=True)
