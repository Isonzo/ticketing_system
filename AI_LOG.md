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

## Instance 4: "Add User" HTML

**1. The Tool:** Gemini 3.1

**2. The Prompt:** "I wrote a Flask route (`/add_user`) that handles GET and POST requests to safely insert a new user into my SQLite database. My backend handles the `UNIQUE` constraint on the email column and passes either an `error` or `success` message to the template. Can you write the `add_user.html` template using Bootstrap 5 to capture `first_name`, `last_name`, and `email`, and show me how to link it in my `base.html` nav bar?"

**3. AI Output:** The AI generated the HTML form and navigation update.
* It created `add_user.html` extending the base layout, containing a Bootstrap card with inputs for the three required fields.
* It included Jinja conditional blocks (`{% if error %}` and `{% if success %}`) to dynamically render Bootstrap alert banners based on the variables passed from my backend route.
* It provided the HTML snippet to add an "Add User" link to the `base.html` navigation bar.

**4. Your Modification:** I integrated the template into my project and verified that the HTML `name` attributes perfectly matched the variable names I set in my `request.form.get()` Python backend logic. I then ran comprehensive testing on the UI, purposefully attempting to add a user with a duplicate email to ensure my custom Python `sqlite3.IntegrityError` logic correctly triggered the AI-generated error alert banner on the frontend.

## Instance 5: Relationship View Template & Debugging (HTML/Jinja)

**1. The Tool:** Gemini 3.1

**2. The Prompt:** "I need to build the 'Relationship Management' view (showing all tickets for a specific user) and a 'Delete' function. Can you provide the Flask routes and Jinja template to display a user's tickets? *(Follow-up prompt after testing)*: I am getting an error saying there is no attribute 'ticket_amount' when clicking profiles."

**3. AI Output:** The AI generated the backend routes and the `user_profile.html` template. However, the AI made a critical error in the Jinja templating. When attempting to dynamically calculate the total price in the HTML table, it hallucinated a column name, writing `{{ ticket['base_price'] + ticket['ticket_amount'] }}`. 

**4. Your Modification:** I implemented the code but immediately caught the rendering error during my UI testing. I cross-referenced the error with my `schema.sql` and identified the AI's mistake, which was using (`ticket_amount`) as a column. I manually debugged and corrected the Jinja template to use the accurate 3NF schema column (`tax_amount`), updating the line to `{{ "%.2f"|format(ticket['base_price'] + ticket['tax_amount']) }}`. This fixed the application and ensured the dynamic pricing calculation worked perfectly.
