# Generative AI Usage Log

## Instance 1: HTML/Jinja Template Generation

**1. The Tool:** Gemini 3.1 Pro

**2. The Prompt:** "Connect them" (Context: Requested the AI to connect the previously generated `app.py` Flask server to the `database.py` SQLite database and generate the frontend HTML skeleton).

**3. AI Output:** The AI generated two HTML files using Bootstrap 5 and Jinja2 templating syntax. 
* It created `base.html` to serve as the master layout containing the `<head>`, Bootstrap CDN links, and the main navigation bar.
* It created `index.html` which extends `base.html` and includes a Jinja2 `{% for event in events %}` loop to dynamically generate a Bootstrap card for every event record fetched from the database. It also included an `{% else %}` block to handle empty database states.

**4. Your Modification:** I reviewed the generated HTML structure to ensure it properly referenced the specific columns from my 3rd Normal Form (3NF) database schema (`event_name`, `event_date`, `ticket_price`). I verified that the Jinja2 variables matched the SQL dictionary keys passed from the Flask backend. (Note: I also had to troubleshoot a directory naming issue, ensuring the folder was named `templates` instead of `template` for Flask to correctly route the HTML).


