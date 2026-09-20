"""
Shift Handoff Notes

A structured handoff tool for shift-based workplaces (healthcare, retail,
warehouses, restaurants, security, manufacturing) — anywhere work continues
across a shift change and information currently gets passed along verbally,
on paper, or not at all.

Run with: streamlit run app.py
"""

import streamlit as st
import db

st.set_page_config(page_title="Shift Handoff Notes", layout="centered")

db.init_db()
db.seed_example_data()

SHIFT_PERIODS = ["Morning", "Afternoon", "Evening", "Night"]

st.title("Shift Handoff Notes")
st.caption("Structured handoffs between shifts — so nothing gets lost when one person leaves and another takes over.")

page = st.sidebar.radio("Go to", ["New Handoff", "View Handoffs", "Dashboard"])

# ---------------------------------------------------------------------------
# New Handoff
# ---------------------------------------------------------------------------
if page == "New Handoff":
    st.subheader("Submit a handoff note")

    with st.form("new_handoff_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            shift_date = st.date_input("Shift date")
        with col2:
            shift_period = st.selectbox("Shift period", SHIFT_PERIODS)

        department = st.text_input("Department / Team", placeholder="e.g. Nursing - Floor 3, Warehouse - Receiving")
        outgoing_employee = st.text_input("Your name")

        tasks_completed = st.text_area(
            "What did you complete this shift?",
            placeholder="e.g. Restocked shelves 4-7, closed register 2, ran end-of-day report"
        )
        tasks_pending = st.text_area(
            "What's still pending for the next shift?",
            placeholder="e.g. Delivery truck expected by 9am, needs to be signed for"
        )
        issues = st.text_area(
            "Any issues or things to flag?",
            placeholder="e.g. Equipment not working, a customer/patient situation to follow up on"
        )
        is_urgent = st.checkbox("This needs immediate attention from the next shift")
        notes = st.text_area("Anything else worth mentioning?", placeholder="Optional")

        submitted = st.form_submit_button("Submit handoff")

        if submitted:
            if not department or not outgoing_employee:
                st.error("Department and your name are required.")
            else:
                db.add_handoff(
                    shift_date=str(shift_date),
                    shift_period=shift_period,
                    department=department,
                    outgoing_employee=outgoing_employee,
                    tasks_completed=tasks_completed,
                    tasks_pending=tasks_pending,
                    issues=issues,
                    is_urgent=is_urgent,
                    notes=notes,
                )
                st.success("Handoff submitted. The next shift will see this under 'View Handoffs'.")

# ---------------------------------------------------------------------------
# View Handoffs
# ---------------------------------------------------------------------------
elif page == "View Handoffs":
    st.subheader("Recent handoffs")

    departments = ["All"] + db.get_departments()
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_department = st.selectbox("Filter by department", departments)
    with col2:
        only_unacknowledged = st.checkbox("Unacknowledged only")

    handoffs = db.get_handoffs(department=selected_department, only_unacknowledged=only_unacknowledged)

    if not handoffs:
        st.info("No handoffs match this filter.")

    for h in handoffs:
        urgent_tag = "🔴 URGENT — " if h["is_urgent"] and not h["acknowledged"] else ""
        ack_tag = "✅ Acknowledged" if h["acknowledged"] else "⏳ Not yet acknowledged"
        header = f"{urgent_tag}{h['shift_date']} · {h['shift_period']} · {h['department']} — from {h['outgoing_employee']}"

        with st.expander(header):
            st.markdown(f"**Status:** {ack_tag}")
            if h["acknowledged"]:
                st.caption(f"Acknowledged by {h['acknowledged_by']} at {h['acknowledged_at']}")

            if h["tasks_completed"]:
                st.markdown("**Completed this shift:**")
                st.write(h["tasks_completed"])
            if h["tasks_pending"]:
                st.markdown("**Pending for next shift:**")
                st.write(h["tasks_pending"])
            if h["issues"]:
                st.markdown("**Issues flagged:**")
                st.write(h["issues"])
            if h["notes"]:
                st.markdown("**Additional notes:**")
                st.write(h["notes"])

            if not h["acknowledged"]:
                ack_name = st.text_input("Your name (to acknowledge)", key=f"ack_name_{h['id']}")
                if st.button("Mark as acknowledged", key=f"ack_btn_{h['id']}"):
                    if ack_name:
                        db.acknowledge_handoff(h["id"], ack_name)
                        st.rerun()
                    else:
                        st.warning("Enter your name to acknowledge this handoff.")

# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
elif page == "Dashboard":
    st.subheader("Overview")
    counts = db.get_summary_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total handoffs", counts["total"])
    col2.metric("Unacknowledged", counts["unacknowledged"])
    col3.metric("Urgent & open", counts["urgent_open"])

    if counts["urgent_open"] > 0:
        st.warning(f"{counts['urgent_open']} urgent handoff(s) still need attention. Check 'View Handoffs'.")
    else:
        st.success("No open urgent items.")
