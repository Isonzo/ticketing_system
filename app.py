from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Basic route to verify the server is running
@app.route('/')
def home():
    return "<h1>Event Ticketing App is Running!</h1><p>Ready to connect to the database.</p>"

# Run the application in debug mode
if __name__ == '__main__':
    # Debug=True means the server will auto-reload upon change
    app.run(debug=True)
