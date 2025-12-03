"""
Habit Tracker
Build and maintain habits with streak tracking and visualization
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import habits_db, add_habit_entry
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="🎯",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("🎯 Habit Tracker")

# Tabs
tab1, tab2, tab3 = st.tabs(["✅ Track Habits", "➕ Manage Habits", "📊 Analytics"])


def calculate_streak(entries):
    """Calculate current streak for a habit."""
    if not entries:
        return 0
    
    # Sort entries by date descending
    sorted_entries = sorted(entries, key=lambda x: x["date"], reverse=True)
    
    streak = 0
    current_date = date.today()
    
    for entry in sorted_entries:
        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
        
        # Check if entry is for current_date and is completed
        if entry_date == current_date and entry.get("completed"):
            streak += 1
            current_date -= timedelta(days=1)
        elif entry_date < current_date:
            # Gap in streak
            break
    
    return streak


def get_completion_rate(entries, days=30):
    """Calculate completion rate for last N days."""
    if not entries:
        return 0
    
    cutoff_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent_entries = [e for e in entries if e["date"] >= cutoff_date and e.get("completed")]
    
    return (len(recent_entries) / days) * 100 if days > 0 else 0


with tab1:
    st.markdown("### ✅ Today's Habits")
    
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    # Get active habits
    Q = Query()
    active_habits = habits_db.search(Q.active == True)
    
    if active_habits:
        for habit in active_habits:
            entries = habit.get("entries", [])
            today_entry = next((e for e in entries if e["date"] == today_str), None)
            is_completed = today_entry.get("completed", False) if today_entry else False
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{habit.get('name')}**")
                st.caption(f"📅 {habit.get('frequency', 'daily').capitalize()}")
            
            with col2:
                streak = calculate_streak(entries)
                st.metric("🔥 Streak", f"{streak} days")
            
            with col3:
                if is_completed:
                    if st.button("✅ Done", key=f"done_{habit.doc_id}", disabled=True):
                        pass
                else:
                    if st.button("⭕ Mark Done", key=f"mark_{habit.doc_id}"):
                        add_habit_entry(habit.doc_id, today, completed=True)
                        st.rerun()
            
            # Progress bar for weekly habits
            if habit.get('frequency') == 'weekly':
                # Calculate this week's progress
                week_start = today - timedelta(days=today.weekday())
                week_entries = [e for e in entries 
                              if e["date"] >= week_start.strftime("%Y-%m-%d") 
                              and e.get("completed")]
                target = habit.get("target", 3)
                progress = min((len(week_entries) / target) * 100, 100)
                st.progress(progress / 100)
                st.caption(f"{len(week_entries)}/{target} times this week")
            
            st.markdown("---")
    else:
        st.info("No active habits. Create your first habit in the 'Manage Habits' tab!")
    
    # Quick add habit
    st.markdown("### ➕ Quick Add Habit")
    
    with st.form("quick_add_habit"):
        new_habit_name = st.text_input("Habit name", placeholder="e.g., Morning meditation")
        new_habit_frequency = st.selectbox("Frequency", ["daily", "weekly"])
        
        if new_habit_frequency == "weekly":
            new_habit_target = st.number_input("Times per week", min_value=1, max_value=7, value=3)
        else:
            new_habit_target = 1
        
        submitted = st.form_submit_button("➕ Add Habit")
        
        if submitted and new_habit_name:
            habits_db.insert({
                "name": new_habit_name,
                "frequency": new_habit_frequency,
                "target": new_habit_target,
                "active": True,
                "created_at": datetime.now().isoformat(),
                "entries": []
            })
            st.success(f"✅ Habit added: {new_habit_name}")
            st.rerun()


with tab2:
    st.markdown("### 📋 Manage Habits")
    
    all_habits = habits_db.get_all()
    
    if all_habits:
        for habit in all_habits:
            with st.expander(f"{'✅' if habit.get('active') else '⏸️'} {habit.get('name')}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Frequency:** {habit.get('frequency', 'daily').capitalize()}")
                    
                    if habit.get('frequency') == 'weekly':
                        st.markdown(f"**Target:** {habit.get('target', 3)} times per week")
                    
                    entries = habit.get("entries", [])
                    streak = calculate_streak(entries)
                    completion_rate = get_completion_rate(entries)
                    
                    st.markdown(f"**Current Streak:** 🔥 {streak} days")
                    st.markdown(f"**30-Day Completion:** {completion_rate:.1f}%")
                    st.markdown(f"**Created:** {datetime.fromisoformat(habit.get('created_at')).strftime('%b %d, %Y')}")
                
                with col2:
                    if habit.get('active'):
                        if st.button("⏸️ Pause", key=f"pause_habit_{habit.doc_id}"):
                            habits_db.update({"active": False}, habit.doc_id)
                            st.rerun()
                    else:
                        if st.button("▶️ Resume", key=f"resume_habit_{habit.doc_id}"):
                            habits_db.update({"active": True}, habit.doc_id)
                            st.rerun()
                    
                    if st.button("🗑️ Delete", key=f"delete_habit_{habit.doc_id}"):
                        habits_db.remove(habit.doc_id)
                        st.success("Habit deleted!")
                        st.rerun()
    else:
        st.info("No habits yet. Add your first habit above!")


with tab3:
    st.markdown("### 📊 Habit Analytics")
    
    all_habits = habits_db.get_all()
    
    if all_habits:
        # Select habit
        habit_names = {h.get("name"): h for h in all_habits}
        selected_habit_name = st.selectbox("Select a habit", list(habit_names.keys()))
        
        if selected_habit_name:
            selected_habit = habit_names[selected_habit_name]
            entries = selected_habit.get("entries", [])
            
            if entries:
                # Stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    streak = calculate_streak(entries)
                    st.metric("🔥 Current Streak", f"{streak} days")
                
                with col2:
                    total_completions = len([e for e in entries if e.get("completed")])
                    st.metric("✅ Total Completions", total_completions)
                
                with col3:
                    completion_rate_7 = get_completion_rate(entries, days=7)
                    st.metric("📊 7-Day Rate", f"{completion_rate_7:.0f}%")
                
                with col4:
                    completion_rate_30 = get_completion_rate(entries, days=30)
                    st.metric("📊 30-Day Rate", f"{completion_rate_30:.0f}%")
                
                st.markdown("---")
                
                # Heatmap (last 90 days)
                st.markdown("### 📅 Habit Heatmap (Last 90 Days)")
                
                # Generate heatmap data
                end_date = date.today()
                start_date = end_date - timedelta(days=89)
                
                heatmap_data = []
                current_date = start_date
                
                while current_date <= end_date:
                    date_str = current_date.strftime("%Y-%m-%d")
                    entry = next((e for e in entries if e["date"] == date_str), None)
                    completed = entry.get("completed", False) if entry else False
                    
                    heatmap_data.append({
                        "Date": date_str,
                        "Completed": 1 if completed else 0,
                        "Day": current_date.strftime("%a"),
                        "Week": current_date.strftime("%U")
                    })
                    
                    current_date += timedelta(days=1)
                
                # Create DataFrame
                df = pd.DataFrame(heatmap_data)
                
                # Pivot for heatmap
                heatmap_pivot = df.pivot(index="Day", columns="Week", values="Completed")
                
                # Display as styled dataframe
                st.dataframe(
                    heatmap_pivot.style.background_gradient(cmap="Greens", vmin=0, vmax=1),
                    use_container_width=True
                )
                
                st.markdown("---")
                
                # Completion trend (last 30 days)
                st.markdown("### 📈 30-Day Trend")
                
                last_30_days = df.tail(30)
                st.bar_chart(last_30_days.set_index("Date")["Completed"])
                
                st.markdown("---")
                
                # Best streak
                st.markdown("### 🏆 Statistics")
                
                # Calculate best streak
                max_streak = 0
                current_streak_calc = 0
                
                sorted_entries = sorted(entries, key=lambda x: x["date"])
                prev_date = None
                
                for entry in sorted_entries:
                    if entry.get("completed"):
                        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                        
                        if prev_date is None or (entry_date - prev_date).days == 1:
                            current_streak_calc += 1
                            max_streak = max(max_streak, current_streak_calc)
                        else:
                            current_streak_calc = 1
                        
                        prev_date = entry_date
                    else:
                        current_streak_calc = 0
                        prev_date = None
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("🏆 Best Streak", f"{max_streak} days")
                
                with col2:
                    days_since_start = (date.today() - datetime.fromisoformat(selected_habit.get("created_at")).date()).days
                    consistency = (total_completions / days_since_start * 100) if days_since_start > 0 else 0
                    st.metric("📊 Overall Consistency", f"{consistency:.1f}%")
            else:
                st.info("No data yet for this habit. Start tracking!")
    else:
        st.info("No habits yet. Create your first habit to see analytics!")


st.markdown("---")
st.caption("💡 Tip: Consistency is key! Track your habits daily to build lasting routines.")
