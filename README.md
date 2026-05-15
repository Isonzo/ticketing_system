# TicketMaster Pro: Event Ticketing System

## Project Description
This is a full-stack Python web application designed to manage event ticketing. It allows administrators and users to view upcoming events, dynamically add new users, securely purchase tickets, and view high-level sales metrics. The database has been normalized to 3rd Normal Form (3NF) to ensure strict data integrity.

## Installation Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment
   * Linux: `source venv/bin/activate`
5. Install the required dependencies: `pip install Flask`

## Database Setup
This project uses SQLite. To initialize the database with the 3NF schema and sample data, run the following command from the root directory:
`python database.py`
This will generate an `event_ticketing.db` file locally.

## Usage
1. Start the Flask development server by running: `python app.py`
2. Open your web browser and navigate to `http://127.0.0.1:5000`
3. **Features:**
   * **Home:** View upcoming events.
   * **Dashboard:** View aggregated sales data and revenue breakdowns.
   * **Add User:** Create a new user profile in the system.
   * **Buy Ticket:** Securely purchase a ticket (utilizes server-side validation and SQL transaction logic).
