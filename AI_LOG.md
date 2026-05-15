# Generative AI Usage Log

## Instance 1: HTML/Jinja Template Generation

**1. The Tool:** Gemini 3.1

**2. The Prompt:** "Connect them" (Context: Requested the AI to connect the previously generated `app.py` Flask server to the `database.py` SQLite database and generate the frontend HTML skeleton).

**3. AI Output:** The AI generated two HTML files using Bootstrap 5 and Jinja2 templating syntax. 
* It created `base.html` to serve as the master layout containing the `<head>`, Bootstrap CDN links, and the main navigation bar.
* It created `index.html` which extends `base.html` and includes a Jinja2 `{% for event in events %}` loop to dynamically generate a Bootstrap card for every event record fetched from the database. It also included an `{% else %}` block to handle empty database states.

**4. Your Modification:** I reviewed the generated HTML structure to ensure it properly referenced the specific columns from my 3rd Normal Form (3NF) database schema (`event_name`, `event_date`, `ticket_price`). I verified that the Jinja2 variables matched the SQL dictionary keys passed from the Flask backend. (Note: I also had to troubleshoot a directory naming issue, ensuring the folder was named `templates` instead of `template` for Flask to correctly route the HTML).

## Instance 2: Dashboard Frontend Generation (HTML/Jinja)

**1. The Tool:** Gemini 3.1

**2. The Prompt:** "Here is my Flask backend code for the `/dashboard` route containing my SQL aggregation queries (COUNT, SUM, AVG). Can you write the `dashboard.html` template using Bootstrap and Jinja to display these metrics, and update my `base.html` nav bar to link to the new page?"

**3. AI Output:** The AI generated the frontend templates required to display the dashboard data. 
* It updated the existing `base.html` to include a navigation link to the `/dashboard` route.
* It created a new `dashboard.html` file that extended the base template. It used Bootstrap cards to display the top-level aggregate statistics (`total_tickets`, `total_revenue`, and `avg_ticket_price`) and generated an HTML table utilizing a Jinja `{% for event in event_stats %}` loop to display the revenue breakdown per event.

**4. Your Modification:** I reviewed the generated HTML to ensure the Jinja variable names exactly matched the dictionary keys returned by my custom SQLite `row_factory` backend queries. I also verified that the formatting filters (like `|format`) were correctly applied to the currency values. Once I tested it out and it looked fine I left it alone.

## Instance 3: Secure Checkout Implementation & UI Generation

**1. The Tool:** Gemini 3.1

**2. The Prompt:** "I need to build a checkout form (`/buy`) using Bootstrap and Jinja. I have the basic Flask backend logic with a SQL transaction, but I want to improve the UX and security. Can you generate the HTML using dynamic `<select>` dropdowns for the Users and Events, and help me update my backend to securely fetch the ticket price directly from the database based on the selected `event_id`?"

**3. AI Output:** The AI generated the updated HTML form and refined the backend logic.
* It created `buy_ticket.html` using Jinja `{% for %}` loops to populate Bootstrap dropdown menus with readable user names and event details.
* It updated the Flask `/buy` route to fetch the true `ticket_price` from the `Events` table using a parameterized SQL query before executing the multi-step `BEGIN TRANSACTION` block.

**4. Your Modification:** I originally designed a basic form where the user input the base price manually. However, I independently identified that allowing the frontend to dictate the price was a massive security vulnerability (client-side manipulation) and that forcing users to memorize IDs was poor UX. I explicitly directed the AI to redesign the template using dynamic dropdowns and I rewrote the backend flow to securely query my 3NF database for the true price, completely closing the security loophole before committing the transaction.
