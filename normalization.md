# Database Normalization Report

## 1. Original Functional Dependencies
Based on the initial database schema designed for the Event Ticketing Application, the original functional dependencies are as follows:

**Users Table:**
* `user_id` -> `first_name`, `last_name`, `email`, `created_at`
* (The user's ID uniquely determines their personal information and metadata).

**Events Table:**
* `event_id` -> `event_name`, `event_date`, `ticket_price`, `last_updated_at`
* (The event's ID uniquely determines the event details and base pricing).

**Tickets Table:**
* `ticket_id` -> `user_id`, `event_id`, `purchase_date`, `base_price`, `tax_amount`, `total_price`, `record_inserted_by`
* `base_price`, `tax_amount` -> `total_price`
* (The ticket ID uniquely identifies the transaction. However, the `total_price` is entirely dependent on the `base_price` and `tax_amount`).

## 2. Anomaly Identification
The original structure contains a violation of 3rd Normal Form (3NF) within the `Tickets` table due to a **Transitive Dependency**. 

Specifically, the `total_price` column is a calculated value (`base_price` + `tax_amount`). This creates a significant **Update Anomaly**:
* **The Update Anomaly:** If an administrator needs to update the `tax_amount` (e.g., due to a change in local tax laws) or the `base_price` (e.g., applying a retroactive discount), they must also remember to manually recalculate and update the `total_price`. If they update the base price but forget to update the total price, the database is left in an inconsistent, mathematically impossible state.

## 3. Decomposition Steps
To achieve 3rd Normal Form (3NF), a table must be in 2NF, and all its non-key attributes must be dependent *only* on the primary key (no transitive dependencies). 

**Step 1:** Identify the transitive dependency in the `Tickets` table (`total_price`).
**Step 2:** Remove the `total_price` column from the `Tickets` schema entirely. 
**Step 3:** Rely on the application layer (Python/SQLAlchemy) or SQL queries (`SELECT base_price + tax_amount AS total_price`) to calculate this value dynamically when requested by the UI, ensuring data integrity is never compromised.

## 4. Final Relational Schema (3NF)
The final schema that the Python application will use has removed the calculated column, successfully reducing the database to 3rd Normal Form.

**Users** (user_id PK, first_name, last_name, email, created_at)
**Events** (event_id PK, event_name, event_date, ticket_price, last_updated_at)
**Tickets** (ticket_id PK, user_id FK, event_id FK, purchase_date, base_price, tax_amount, record_inserted_by)
