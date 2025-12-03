"""
Calendar View
Monthly calendar with events, tasks, and deadlines
"""
import streamlit as st
from datetime import datetime, date, timedelta
import calendar as cal
from utils.auth import check_password
from utils.db import events_db, tasks_db, goals_db
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Calendar",
    page_icon="📅",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("📅 Calendar")

# Tabs
tab1, tab2, tab3 = st.tabs(["📅 Month View", "➕ Add Event", "📋 Agenda"])

Q = Query()

# Initialize session state
if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = date.today().month

if "calendar_year" not in st.session_state:
    st.session_state.calendar_year = date.today().year


with tab1:
    st.markdown("### 📅 Monthly Calendar")
    
    # Month/Year selector
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
    
    with col1:
        if st.button("◀"):
            if st.session_state.calendar_month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year -= 1
            else:
                st.session_state.calendar_month -= 1
            st.rerun()
    
    with col2:
        month_name = cal.month_name[st.session_state.calendar_month]
        st.markdown(f"### {month_name} {st.session_state.calendar_year}")
    
    with col3:
        pass
    
    with col4:
        if st.button("Today"):
            st.session_state.calendar_month = date.today().month
            st.session_state.calendar_year = date.today().year
            st.rerun()
    
    with col5:
        if st.button("▶"):
            if st.session_state.calendar_month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year += 1
            else:
                st.session_state.calendar_month += 1
            st.rerun()
    
    st.markdown("---")
    
    # Get events and tasks for this month
    month_start = date(st.session_state.calendar_year, st.session_state.calendar_month, 1)
    
    if st.session_state.calendar_month == 12:
        month_end = date(st.session_state.calendar_year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(st.session_state.calendar_year, st.session_state.calendar_month + 1, 1) - timedelta(days=1)
    
    # Fetch data
    all_events = events_db.get_all()
    all_tasks = tasks_db.get_all()
    all_goals = goals_db.get_all()
    
    # Filter by month
    month_events = [e for e in all_events 
                    if month_start.isoformat() <= e.get("date", "") <= month_end.isoformat()]
    
    month_tasks = [t for t in all_tasks 
                   if t.get("deadline") and month_start.isoformat() <= t.get("deadline", "") <= month_end.isoformat()]
    
    month_goals = [g for g in all_goals 
                   if g.get("deadline") and month_start.isoformat() <= g.get("deadline", "") <= month_end.isoformat()]
    
    # Create calendar grid
    month_cal = cal.monthcalendar(st.session_state.calendar_year, st.session_state.calendar_month)
    
    # Display calendar
    st.markdown("### 🗓️")
    
    # Days of week header
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"**{day}**")
    
    # Calendar days
    for week in month_cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown("")
                else:
                    current_date = date(st.session_state.calendar_year, st.session_state.calendar_month, day)
                    date_str = current_date.isoformat()
                    
                    # Check if today
                    is_today = current_date == date.today()
                    
                    # Count items
                    day_events = [e for e in month_events if e.get("date") == date_str]
                    day_tasks = [t for t in month_tasks if t.get("deadline") == date_str]
                    day_goals = [g for g in month_goals if g.get("deadline") == date_str]
                    
                    total_items = len(day_events) + len(day_tasks) + len(day_goals)
                    
                    # Display day
                    if is_today:
                        st.markdown(f"**:blue[{day}]**")
                    else:
                        st.markdown(f"{day}")
                    
                    # Display indicators
                    if total_items > 0:
                        st.caption(f"📌 {total_items}")
                        
                        # Show first few items
                        for event in day_events[:2]:
                            st.caption(f"• {event.get('title', '')[:15]}")
                        for task in day_tasks[:2]:
                            st.caption(f"✅ {task.get('title', '')[:15]}")
    
    st.markdown("---")
    
    # Legend
    col_leg1, col_leg2, col_leg3 = st.columns(3)
    
    with col_leg1:
        st.caption("📌 Events")
    
    with col_leg2:
        st.caption("✅ Task Deadlines")
    
    with col_leg3:
        st.caption("🎯 Goal Deadlines")


with tab2:
    st.markdown("### ➕ Add Event")
    
    with st.form("add_event"):
        event_title = st.text_input("Event Title*", placeholder="e.g., Team Meeting, Conference")
        
        col1, col2 = st.columns(2)
        
        with col1:
            event_date = st.date_input("Date", value=date.today())
            event_time = st.time_input("Time", value=datetime.now().time())
        
        with col2:
            event_type = st.selectbox(
                "Type",
                ["Meeting", "Deadline", "Reminder", "Personal", "Work", "Other"]
            )
            
            event_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        event_description = st.text_area("Description", placeholder="Event details, location, attendees...", height=100)
        
        event_reminder = st.checkbox("Set reminder 1 day before")
        
        submitted = st.form_submit_button("➕ Add Event", use_container_width=True)
        
        if submitted and event_title:
            new_event = {
                "title": event_title,
                "date": event_date.isoformat(),
                "time": event_time.isoformat(),
                "type": event_type,
                "priority": event_priority.lower(),
                "description": event_description,
                "reminder": event_reminder,
                "created_at": datetime.now().isoformat()
            }
            
            events_db.insert(new_event)
            st.success(f"✅ Event added: {event_title}")
            st.rerun()


with tab3:
    st.markdown("### 📋 Agenda")
    
    # Time range selector
    view_range = st.selectbox("View", ["Today", "This Week", "Next Week", "This Month", "Next Month"])
    
    # Calculate date range
    today = date.today()
    
    if view_range == "Today":
        start_date = today
        end_date = today
    elif view_range == "This Week":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif view_range == "Next Week":
        start_date = today - timedelta(days=today.weekday()) + timedelta(days=7)
        end_date = start_date + timedelta(days=6)
    elif view_range == "This Month":
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)
    else:  # Next Month
        if today.month == 12:
            start_date = date(today.year + 1, 1, 1)
            end_date = date(today.year + 1, 2, 1) - timedelta(days=1)
        else:
            start_date = date(today.year, today.month + 1, 1)
            if today.month == 11:
                end_date = date(today.year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(today.year, today.month + 2, 1) - timedelta(days=1)
    
    st.markdown(f"**{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}**")
    st.markdown("---")
    
    # Fetch all items in range
    start_str = start_date.isoformat()
    end_str = end_date.isoformat()
    
    range_events = [e for e in events_db.get_all() 
                    if start_str <= e.get("date", "") <= end_str]
    
    range_tasks = [t for t in tasks_db.get_all() 
                   if t.get("deadline") and start_str <= t.get("deadline", "") <= end_str]
    
    range_goals = [g for g in goals_db.get_all() 
                   if g.get("deadline") and start_str <= g.get("deadline", "") <= end_str]
    
    # Organize by date
    agenda_by_date = {}
    
    for event in range_events:
        event_date = event.get("date")
        if event_date not in agenda_by_date:
            agenda_by_date[event_date] = {"events": [], "tasks": [], "goals": []}
        agenda_by_date[event_date]["events"].append(event)
    
    for task in range_tasks:
        task_date = task.get("deadline")
        if task_date not in agenda_by_date:
            agenda_by_date[task_date] = {"events": [], "tasks": [], "goals": []}
        agenda_by_date[task_date]["tasks"].append(task)
    
    for goal in range_goals:
        goal_date = goal.get("deadline")
        if goal_date not in agenda_by_date:
            agenda_by_date[goal_date] = {"events": [], "tasks": [], "goals": []}
        agenda_by_date[goal_date]["goals"].append(goal)
    
    # Display agenda
    if agenda_by_date:
        for date_str in sorted(agenda_by_date.keys()):
            agenda_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            is_today = agenda_date == today
            
            day_name = agenda_date.strftime("%A, %B %d, %Y")
            
            if is_today:
                st.markdown(f"### 📌 {day_name} (Today)")
            else:
                st.markdown(f"### {day_name}")
            
            items = agenda_by_date[date_str]
            
            # Events
            for event in items["events"]:
                priority_icon = "🔴" if event.get("priority") == "high" else "🟡" if event.get("priority") == "medium" else "🟢"
                time_str = event.get("time", "00:00:00")[:5]
                
                col_e1, col_e2 = st.columns([4, 1])
                
                with col_e1:
                    st.markdown(f"📌 {priority_icon} **{event.get('title')}** at {time_str}")
                    if event.get("description"):
                        st.caption(event.get("description"))
                
                with col_e2:
                    if st.button("🗑️", key=f"del_event_{event.doc_id}"):
                        events_db.remove(event.doc_id)
                        st.rerun()
            
            # Tasks
            for task in items["tasks"]:
                priority_icon = "🔴" if task.get("priority") == "high" else "🟡" if task.get("priority") == "medium" else "🟢"
                st.markdown(f"✅ {priority_icon} Task: **{task.get('title')}** (Deadline)")
            
            # Goals
            for goal in items["goals"]:
                st.markdown(f"🎯 Goal: **{goal.get('title')}** (Target date)")
            
            st.markdown("---")
    else:
        st.info(f"No events, tasks, or deadlines in {view_range.lower()}.")


st.markdown("---")
st.caption("💡 Tip: Use the calendar to visualize your schedule and plan ahead!")
