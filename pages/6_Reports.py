"""
Weekly & Monthly Reports
Auto-generated progress reports with AI insights
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import tasks_db, journal_db, habits_db
from utils.ai import generate_weekly_report, generate_monthly_report
import pandas as pd


# Page config
st.set_page_config(
    page_title="Reports",
    page_icon="📋",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("📋 Progress Reports")

# Tabs
tab1, tab2 = st.tabs(["📅 Weekly Report", "📆 Monthly Report"])


def get_week_range(weeks_ago=0):
    """Get start and end date for a week."""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday() + (weeks_ago * 7))
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week


def get_month_range(months_ago=0):
    """Get start and end date for a month."""
    today = date.today()
    
    # Calculate target month
    target_month = today.month - months_ago
    target_year = today.year
    
    while target_month < 1:
        target_month += 12
        target_year -= 1
    
    # Start of month
    start_of_month = date(target_year, target_month, 1)
    
    # End of month
    if target_month == 12:
        end_of_month = date(target_year + 1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = date(target_year, target_month + 1, 1) - timedelta(days=1)
    
    return start_of_month, end_of_month


with tab1:
    st.markdown("### 📅 Weekly Report")
    
    # Week selector
    week_options = {
        "This Week": 0,
        "Last Week": 1,
        "2 Weeks Ago": 2,
        "3 Weeks Ago": 3,
        "4 Weeks Ago": 4
    }
    
    selected_week = st.selectbox("Select week", list(week_options.keys()))
    weeks_ago = week_options[selected_week]
    
    start_date, end_date = get_week_range(weeks_ago)
    
    st.markdown(f"**{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}**")
    st.markdown("---")
    
    # Gather data for the week
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    # Tasks
    all_tasks = tasks_db.get_all()
    week_tasks_completed = [
        t for t in all_tasks
        if t.get("status") == "done"
        and t.get("completed_at")
        and start_str <= t.get("completed_at", "9999")[:10] <= end_str
    ]
    
    # Journal
    all_journals = journal_db.get_all()
    week_journals = [
        j for j in all_journals
        if start_str <= j.get("date", "") <= end_str
    ]
    
    # Habits
    all_habits = habits_db.get_all()
    week_habit_completions = 0
    
    for habit in all_habits:
        entries = habit.get("entries", [])
        week_entries = [
            e for e in entries
            if start_str <= e.get("date", "") <= end_str
            and e.get("completed")
        ]
        week_habit_completions += len(week_entries)
    
    # Mood average
    journals_with_mood = [j for j in week_journals if j.get("mood")]
    avg_mood = sum([j.get("mood", 0) for j in journals_with_mood]) / len(journals_with_mood) if journals_with_mood else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Tasks Completed", len(week_tasks_completed))
    
    with col2:
        st.metric("📝 Journal Entries", len(week_journals))
    
    with col3:
        st.metric("🎯 Habit Completions", week_habit_completions)
    
    with col4:
        st.metric("😊 Avg Mood", f"{avg_mood:.1f}/10" if avg_mood > 0 else "N/A")
    
    st.markdown("---")
    
    # Task breakdown
    st.markdown("### ✅ Tasks This Week")
    
    if week_tasks_completed:
        task_df = []
        for task in week_tasks_completed:
            completed_date = datetime.fromisoformat(task.get("completed_at")).strftime("%b %d")
            task_df.append({
                "Task": task.get("title"),
                "Priority": task.get("priority", "low"),
                "Completed": completed_date
            })
        
        df = pd.DataFrame(task_df)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No tasks completed this week.")
    
    st.markdown("---")
    
    # Mood trend
    if journals_with_mood:
        st.markdown("### 😊 Mood Trend")
        
        mood_data = []
        for journal in sorted(week_journals, key=lambda x: x.get("date", "")):
            if journal.get("mood"):
                mood_data.append({
                    "Date": journal.get("date"),
                    "Mood": journal.get("mood", 0)
                })
        
        if mood_data:
            df_mood = pd.DataFrame(mood_data)
            st.line_chart(df_mood.set_index("Date"))
    
    st.markdown("---")
    
    # AI-generated summary
    st.markdown("### 🤖 AI Weekly Summary")
    
    if st.button("✨ Generate Weekly Summary", use_container_width=True):
        with st.spinner("Generating summary..."):
            summary = generate_weekly_report(
                week_journals,
                len(week_tasks_completed),
                all_habits,
                avg_mood
            )
            st.success(summary)


with tab2:
    st.markdown("### 📆 Monthly Report")
    
    # Month selector
    month_options = {
        "This Month": 0,
        "Last Month": 1,
        "2 Months Ago": 2,
        "3 Months Ago": 3
    }
    
    selected_month = st.selectbox("Select month", list(month_options.keys()))
    months_ago = month_options[selected_month]
    
    start_date, end_date = get_month_range(months_ago)
    
    st.markdown(f"**{start_date.strftime('%B %Y')}**")
    st.markdown("---")
    
    # Gather data for the month
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    # Tasks
    all_tasks = tasks_db.get_all()
    month_tasks_completed = [
        t for t in all_tasks
        if t.get("status") == "done"
        and t.get("completed_at")
        and start_str <= t.get("completed_at", "9999")[:10] <= end_str
    ]
    
    month_tasks_created = [
        t for t in all_tasks
        if t.get("created_at")
        and start_str <= t.get("created_at", "9999")[:10] <= end_str
    ]
    
    # Journal
    all_journals = journal_db.get_all()
    month_journals = [
        j for j in all_journals
        if start_str <= j.get("date", "") <= end_str
    ]
    
    # Habits
    all_habits = habits_db.get_all()
    month_habit_completions = 0
    habits_created = 0
    
    for habit in all_habits:
        # Check if created this month
        if habit.get("created_at") and start_str <= habit.get("created_at")[:10] <= end_str:
            habits_created += 1
        
        # Count completions
        entries = habit.get("entries", [])
        month_entries = [
            e for e in entries
            if start_str <= e.get("date", "") <= end_str
            and e.get("completed")
        ]
        month_habit_completions += len(month_entries)
    
    # Mood average
    journals_with_mood = [j for j in month_journals if j.get("mood")]
    avg_mood = sum([j.get("mood", 0) for j in journals_with_mood]) / len(journals_with_mood) if journals_with_mood else 0
    
    avg_energy = sum([j.get("energy", 0) for j in journals_with_mood]) / len(journals_with_mood) if journals_with_mood else 0
    avg_stress = sum([j.get("stress", 0) for j in journals_with_mood]) / len(journals_with_mood) if journals_with_mood else 0
    
    # Display metrics
    st.markdown("### 📊 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Tasks Completed", len(month_tasks_completed))
    
    with col2:
        st.metric("📝 Journal Entries", len(month_journals))
    
    with col3:
        st.metric("🎯 Habit Completions", month_habit_completions)
    
    with col4:
        st.metric("➕ New Habits", habits_created)
    
    st.markdown("---")
    
    # Productivity graph
    st.markdown("### 📈 Productivity Graph")
    
    # Tasks completed by week
    weekly_productivity = {}
    for task in month_tasks_completed:
        if task.get("completed_at"):
            completed_date = datetime.fromisoformat(task.get("completed_at")).date()
            week_num = completed_date.strftime("Week %U")
            weekly_productivity[week_num] = weekly_productivity.get(week_num, 0) + 1
    
    if weekly_productivity:
        df_prod = pd.DataFrame(list(weekly_productivity.items()), columns=["Week", "Tasks"])
        st.bar_chart(df_prod.set_index("Week"))
    else:
        st.info("No task data for this month.")
    
    st.markdown("---")
    
    # Mood graph
    st.markdown("### 😊 Mood & Wellbeing")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.metric("😊 Avg Mood", f"{avg_mood:.1f}/10" if avg_mood > 0 else "N/A")
    
    with col_m2:
        st.metric("⚡ Avg Energy", f"{avg_energy:.1f}/10" if avg_energy > 0 else "N/A")
    
    with col_m3:
        st.metric("😰 Avg Stress", f"{avg_stress:.1f}/10" if avg_stress > 0 else "N/A")
    
    if journals_with_mood:
        mood_data = []
        for journal in sorted(month_journals, key=lambda x: x.get("date", "")):
            if journal.get("mood"):
                mood_data.append({
                    "Date": journal.get("date"),
                    "Mood": journal.get("mood", 0),
                    "Energy": journal.get("energy", 0),
                    "Stress": journal.get("stress", 0)
                })
        
        if mood_data:
            df_mood = pd.DataFrame(mood_data)
            st.line_chart(df_mood.set_index("Date"))
    
    st.markdown("---")
    
    # Journal summary
    st.markdown("### 📝 Journal Summary")
    
    if month_journals:
        total_words = sum([len(j.get("content", "").split()) for j in month_journals])
        st.metric("Total Words Written", total_words)
    
    st.markdown("---")
    
    # AI-generated monthly summary
    st.markdown("### 🤖 AI Monthly Summary")
    
    if st.button("✨ Generate Monthly Summary", use_container_width=True):
        with st.spinner("Generating comprehensive summary..."):
            stats = f"""
Tasks Completed: {len(month_tasks_completed)}
Tasks Created: {len(month_tasks_created)}
Journal Entries: {len(month_journals)}
Habit Completions: {month_habit_completions}
New Habits: {habits_created}
Average Mood: {avg_mood:.1f}/10
Average Energy: {avg_energy:.1f}/10
Average Stress: {avg_stress:.1f}/10
"""
            summary = generate_monthly_report(stats)
            st.success(summary)


st.markdown("---")
st.caption("💡 Tip: Review your reports regularly to track progress and adjust your goals!")
