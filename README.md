# Shift Handoff Notes

A structured handoff tool for any workplace where work continues across a shift change, including hospitals, warehouses, retail, restaurants, security, and manufacturing.

Many teams still rely on verbal handoffs, sticky notes, or shared notebooks, which can lead to important details being missed. A patient detail, pending delivery, equipment issue, or customer request can easily get overlooked.

**Shift Handoff Notes** gives each shift a structured place to leave important information and gives the next shift a clear, filterable view of what's open. Urgent items are flagged separately from routine updates.

## Why This, Specifically

A bad shift handoff isn't just an inconvenience. In healthcare, it can mean a missed medication follow-up. In a warehouse, it could mean a safety issue goes unreported. In retail, it could mean a customer promise gets forgotten.

This tool doesn't try to replace judgment or communication between coworkers. Instead, it makes sure important information survives the handoff rather than depending on someone remembering to mention it.

## Try It Immediately

The app comes pre-loaded with two example handoffs:

- Nursing floor
- Warehouse receiving team

This lets you explore the application without needing a second person to create a handoff.

After starting the app, open **View Handoffs** to see the example data.

## Features

- **Submit a handoff:** Record what was completed, what's pending, any issues, and whether the item is urgent.
- **View handoffs:** Filter handoffs by department or show only items that haven't been acknowledged.
- **Acknowledge:** The incoming shift can mark a handoff as read with their name and a timestamp, creating a record that the information was actually seen.
- **Dashboard:** View at-a-glance counts of total, unacknowledged, and open urgent handoffs.

## Running It

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Then start the application:

```bash
streamlit run app.py
```

No database setup is required. The application uses SQLite, stored locally in `handoffs.db`, which is created automatically the first time the app runs.

## Design Choices Worth Knowing

### SQLite Over a Hosted Database

SQLite keeps the entire application runnable with a single command and eliminates the need to provision a separate database server.

**Trade-off:** This version is designed to run on a single machine. See [What I'd Add With More Time](#what-id-add-with-more-time) for how this could be expanded for a real team.

### Explicit Acknowledgment

Rather than simply tracking whether someone opened a page, the application requires the incoming employee to provide their name and explicitly acknowledge the handoff.

This creates a clearer record that important information was actually received.

### Separate Urgent Flag

Urgency is intentionally separate from the free-text issues field. This prevents an important handoff from being buried among routine updates.

## What I'd Add With More Time

- **Shared hosting:** Allow multiple people on different devices to access and update the same data in real time.
- **Employee accounts:** Replace the free-text name field with simple employee login accounts.
- **Notifications:** Send optional SMS or email notifications when an urgent handoff is submitted.
- **Shift history:** Provide a department-specific history view to identify recurring issues over time.
