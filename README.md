# Shift Handoff Notes

A structured handoff tool for any workplace where work continues across a
shift change — hospitals, warehouses, retail, restaurants, security,
manufacturing. Most of these teams currently hand off verbally, on a
sticky note, or in a shared notebook, which means things get missed:
a patient detail, a pending delivery, a piece of equipment that needs
attention. This gives every shift a structured place to leave that
information, and gives the next shift a clear, filterable view of what's
open — with urgent items flagged separately from routine updates.

## Why this, specifically

A bad shift handoff isn't just an inconvenience — in healthcare it can mean
a missed medication follow-up; in a warehouse, a safety issue nobody flags;
in retail, a customer promise nobody keeps. This tool doesn't try to
replace judgment or communication between coworkers — it just makes sure
the information survives the handoff instead of depending on someone
remembering to mention it.

## Try it immediately

The app comes pre-loaded with two example handoffs (a nursing floor and a
warehouse receiving team) so you can see how it works without needing a
second person to hand off to. Open "View Handoffs" after starting the app
to see them.

## Features

- **Submit a handoff**: what was completed, what's pending, any issues, and an urgent flag
- **View handoffs**: filter by department, or show only what hasn't been acknowledged yet
- **Acknowledge**: the incoming shift marks a handoff as read, with their name and a timestamp — so there's a record it was actually seen, not just left in a queue
- **Dashboard**: at-a-glance counts of total, unacknowledged, and open urgent handoffs

## Running it

```bash
pip install -r requirements.txt
streamlit run app.py
```

No database setup required — it uses SQLite, stored locally in
`handoffs.db`, which is created automatically on first run.

## Design choices worth knowing

- **SQLite over a hosted database:** keeps the whole thing runnable with a
  single command. No server to provision. Trade-off: this version is
  single-machine — see "What I'd add" below for how a real team would use it.
- **Explicit acknowledgment instead of "seen" tracking:** requiring a name
  and an action (not just opening the page) creates actual accountability
  that an urgent item was received, not just displayed.
- **Urgent flag is separate from the free-text issues field:** so a truly
  urgent handoff can't get buried in a long list of routine ones.

## What I'd add with more time

- Shared hosting so multiple people on different devices see the same data
  in real time (this version runs locally per machine)
- Simple login per employee instead of a free-text name field
- Optional notifications (SMS/email) when an urgent handoff is submitted
- Shift-to-shift history view for a single department, to spot recurring issues over time
