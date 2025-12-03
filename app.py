"""
Personal Life & Startup Dashboard
Main app with Daily Dashboard
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password, logout
from utils.db import (
    tasks_db, journal_db, get_journal_entry, save_journal_entry,
    get_tasks_for_date, get_tasks_by_status, get_setting, set_setting
)
from utils.ai import generate_daily_summary, generate_task_suggestions
from tinydb import Query


# Page config
st.set_page_config(
    page_title="Personal Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication
if not check_password():
    st.stop()


# Sidebar
with st.sidebar:
    st.title("🏠 Personal Dashboard")
    st.markdown("---")
    
    # Theme toggle
    current_theme = get_setting("theme", "light")
    theme_option = st.selectbox(
        "🎨 Theme",
        ["light", "dark"],
        index=0 if current_theme == "light" else 1,
        key="theme_selector"
    )
    
    if theme_option != current_theme:
        set_setting("theme", theme_option)
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Navigation")
    st.page_link("app.py", label="🏠 Daily Dashboard", icon="🏠")
    st.page_link("pages/1_Tasks.py", label="✅ Tasks & Projects", icon="✅")
    st.page_link("pages/2_Journal.py", label="📝 Journal", icon="📝")
    st.page_link("pages/3_Habits.py", label="🎯 Habit Tracker", icon="🎯")
    st.page_link("pages/4_Analytics.py", label="📊 Analytics", icon="📊")
    st.page_link("pages/5_Notes.py", label="💡 Notes & Ideas", icon="💡")
    st.page_link("pages/6_Reports.py", label="📋 Reports", icon="📋")
    
    st.markdown("---")
    st.markdown("### 🆕 New Features")
    st.page_link("pages/7_Health.py", label="💪 Health & Wellness", icon="💪")
    st.page_link("pages/8_Finance.py", label="💰 Finance Tracker", icon="💰")
    st.page_link("pages/9_Contacts.py", label="👥 Contacts & Network", icon="👥")
    st.page_link("pages/10_Gratitude.py", label="🙏 Gratitude & Wins", icon="🙏")
    st.page_link("pages/11_Goals.py", label="🎯 Goals & OKRs", icon="🎯")
    st.page_link("pages/12_Calendar.py", label="📅 Calendar", icon="📅")
    
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()
    
    st.markdown("---")
    st.caption(f"📅 {datetime.now().strftime('%B %d, %Y')}")


# Main content
st.title("🏠 Daily Dashboard")
st.markdown(f"### {datetime.now().strftime('%A, %B %d, %Y')}")

# Today's date
today = date.today()
today_str = today.strftime("%Y-%m-%d")

# Initialize session state
if "daily_priorities" not in st.session_state:
    st.session_state.daily_priorities = get_setting(f"priorities_{today_str}", ["", "", ""])

if "mood" not in st.session_state:
    entry = get_journal_entry(today)
    st.session_state.mood = entry.get("mood", 5) if entry else 5
    st.session_state.energy = entry.get("energy", 5) if entry else 5
    st.session_state.stress = entry.get("stress", 5) if entry else 5


# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ✍️ Quick Add")
    
    with st.expander("📝 Daily Journal", expanded=True):
        entry = get_journal_entry(today)
        journal_text = st.text_area(
            "How was your day?",
            value=entry.get("content", "") if entry else "",
            height=150,
            key="journal_input",
            placeholder="Write about your day, thoughts, feelings..."
        )
        
        if st.button("💾 Save Journal", key="save_journal"):
            save_journal_entry(
                today,
                journal_text,
                st.session_state.mood,
                st.session_state.energy,
                st.session_state.stress
            )
            st.success("✅ Journal saved!")
    
    st.markdown("### 🎯 Today's Priorities")
    
    priority_1 = st.text_input("1️⃣ Priority #1", value=st.session_state.daily_priorities[0], key="p1")
    priority_2 = st.text_input("2️⃣ Priority #2", value=st.session_state.daily_priorities[1], key="p2")
    priority_3 = st.text_input("3️⃣ Priority #3", value=st.session_state.daily_priorities[2], key="p3")
    
    if st.button("💾 Save Priorities"):
        priorities = [priority_1, priority_2, priority_3]
        st.session_state.daily_priorities = priorities
        set_setting(f"priorities_{today_str}", priorities)
        st.success("✅ Priorities saved!")
    
    st.markdown("### 😊 How are you feeling?")
    
    mood = st.slider("😊 Mood", 1, 10, st.session_state.mood, key="mood_slider")
    energy = st.slider("⚡ Energy", 1, 10, st.session_state.energy, key="energy_slider")
    stress = st.slider("😰 Stress", 1, 10, st.session_state.stress, key="stress_slider")
    
    if st.button("💾 Save Feelings"):
        st.session_state.mood = mood
        st.session_state.energy = energy
        st.session_state.stress = stress
        
        entry = get_journal_entry(today)
        save_journal_entry(
            today,
            entry.get("content", "") if entry else "",
            mood, energy, stress
        )
        st.success("✅ Feelings saved!")


with col2:
    st.markdown("### ✅ Tasks")
    
    # Get today's tasks
    Q = Query()
    all_tasks = tasks_db.get_all()
    
    # Filter tasks for today or overdue
    today_tasks = [t for t in all_tasks if t.get("date") == today_str]
    overdue_tasks = [t for t in all_tasks 
                     if t.get("deadline") and t.get("deadline") < today_str 
                     and t.get("status") != "done"]
    
    # Done today
    with st.expander("✅ Done Today", expanded=True):
        done_tasks = [t for t in today_tasks if t.get("status") == "done"]
        
        if done_tasks:
            for task in done_tasks:
                st.markdown(f"- ~~{task.get('title')}~~")
        else:
            st.info("No tasks completed yet today.")
    
    # Tasks remaining
    with st.expander("📋 Tasks Remaining", expanded=True):
        remaining_tasks = [t for t in all_tasks 
                          if t.get("status") in ["todo", "doing"]]
        
        if remaining_tasks:
            for i, task in enumerate(remaining_tasks[:5]):  # Show top 5
                status_icon = "🔴" if task.get("priority") == "high" else "🟡" if task.get("priority") == "medium" else "🟢"
                st.markdown(f"{status_icon} {task.get('title')}")
            
            if len(remaining_tasks) > 5:
                st.caption(f"...and {len(remaining_tasks) - 5} more")
        else:
            st.success("🎉 No tasks remaining!")
    
    # Overdue warning
    if overdue_tasks:
        with st.expander("⚠️ Overdue Tasks", expanded=True):
            for task in overdue_tasks[:3]:
                st.error(f"🔴 {task.get('title')} (Due: {task.get('deadline')})")
    
    # Quick add task
    with st.expander("➕ Quick Add Task"):
        new_task_title = st.text_input("Task title", key="new_task_title")
        new_task_priority = st.selectbox("Priority", ["low", "medium", "high"], key="new_task_priority")
        
        if st.button("➕ Add Task") and new_task_title:
            tasks_db.insert({
                "title": new_task_title,
                "description": "",
                "status": "todo",
                "priority": new_task_priority,
                "date": today_str,
                "created_at": datetime.now().isoformat(),
                "tags": []
            })
            st.success(f"✅ Added: {new_task_title}")
            st.rerun()


# Daily AI Summary
st.markdown("---")
st.markdown("### 🤖 AI Daily Summary")

col_summary, col_suggestions = st.columns([1, 1])

with col_summary:
    if st.button("✨ Generate Daily Summary", use_container_width=True):
        with st.spinner("Analyzing your day..."):
            entry = get_journal_entry(today)
            journal_content = entry.get("content", "") if entry else ""
            
            done_today = [t for t in today_tasks if t.get("status") == "done"]
            remaining = [t for t in all_tasks if t.get("status") in ["todo", "doing"]]
            
            summary = generate_daily_summary(
                journal_content,
                done_today,
                remaining,
                st.session_state.mood,
                st.session_state.energy,
                st.session_state.stress
            )
            
            st.markdown(f"**Daily Insights:**\n\n{summary}")

with col_suggestions:
    if st.button("🎯 Get Task Suggestions", use_container_width=True):
        with st.spinner("Analyzing your tasks..."):
            remaining = [t for t in all_tasks if t.get("status") in ["todo", "doing"]]
            priorities = [p for p in [priority_1, priority_2, priority_3] if p]
            
            suggestions = generate_task_suggestions(remaining, priorities)
            
            st.markdown(f"**Task Suggestions:**\n\n{suggestions}")


# Quick stats
st.markdown("---")
st.markdown("### 📊 Quick Stats")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    done_today_count = len([t for t in today_tasks if t.get("status") == "done"])
    st.metric("✅ Done Today", done_today_count)

with stat_col2:
    remaining_count = len([t for t in all_tasks if t.get("status") in ["todo", "doing"]])
    st.metric("📋 Remaining", remaining_count)

with stat_col3:
    st.metric("😊 Mood", f"{st.session_state.mood}/10")

with stat_col4:
    st.metric("⚡ Energy", f"{st.session_state.energy}/10")


# Footer
st.markdown("---")
st.caption("💡 Tip: Use the sidebar to navigate to other sections of your dashboard.")
