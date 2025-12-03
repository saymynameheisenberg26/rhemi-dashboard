"""
Progress Analytics
Visualize productivity, mood, habits, and overall progress
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import tasks_db, journal_db, habits_db, health_db, finance_db, gratitude_db, goals_db
from utils.ai import get_ai_response
from tinydb import Query
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import numpy as np


# Page config
st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("📊 Progress Analytics")

# Time range selector
time_range = st.selectbox("Select time range", ["Last 7 days", "Last 30 days", "Last 90 days", "All time"])

# Calculate date range
if time_range == "Last 7 days":
    start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
elif time_range == "Last 30 days":
    start_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
elif time_range == "Last 90 days":
    start_date = (date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
else:
    start_date = "2000-01-01"

st.markdown("---")

# Overview metrics
st.markdown("### 📈 Overview")

col1, col2, col3, col4 = st.columns(4)

# Tasks completed
all_tasks = tasks_db.get_all()
completed_tasks = [t for t in all_tasks 
                   if t.get("status") == "done" 
                   and t.get("completed_at", "9999") >= start_date]

with col1:
    st.metric("✅ Tasks Completed", len(completed_tasks))

# Journal entries
all_journals = journal_db.get_all()
journals_in_range = [j for j in all_journals if j.get("date", "") >= start_date]

with col2:
    st.metric("📝 Journal Entries", len(journals_in_range))

# Active habits
all_habits = habits_db.get_all()
active_habits = [h for h in all_habits if h.get("active")]

with col3:
    st.metric("🎯 Active Habits", len(active_habits))

# Average mood
journals_with_mood = [j for j in journals_in_range if j.get("mood")]
avg_mood = sum([j.get("mood", 0) for j in journals_with_mood]) / len(journals_with_mood) if journals_with_mood else 0

with col4:
    st.metric("😊 Avg Mood", f"{avg_mood:.1f}/10")

st.markdown("---")

# Productivity Analysis
st.markdown("### 📊 Productivity Analysis")

col_prod1, col_prod2 = st.columns(2)

with col_prod1:
    st.markdown("#### Tasks Completed Per Day")
    
    # Generate daily task completion data
    task_data = {}
    for task in completed_tasks:
        if task.get("completed_at"):
            completion_date = datetime.fromisoformat(task.get("completed_at")).date().strftime("%Y-%m-%d")
            task_data[completion_date] = task_data.get(completion_date, 0) + 1
    
    if task_data:
        df_tasks = pd.DataFrame(list(task_data.items()), columns=["Date", "Tasks"])
        df_tasks = df_tasks.sort_values("Date")
        st.line_chart(df_tasks.set_index("Date"))
    else:
        st.info("No task completion data in this range.")

with col_prod2:
    st.markdown("#### Tasks by Priority")
    
    priority_data = {}
    for task in completed_tasks:
        priority = task.get("priority", "low")
        priority_data[priority] = priority_data.get(priority, 0) + 1
    
    if priority_data:
        df_priority = pd.DataFrame(list(priority_data.items()), columns=["Priority", "Count"])
        st.bar_chart(df_priority.set_index("Priority"))
    else:
        st.info("No priority data available.")

st.markdown("---")

# Mood & Wellbeing Analysis
st.markdown("### 😊 Mood & Wellbeing Trends")

journals_with_metrics = [j for j in journals_in_range 
                         if j.get("mood") or j.get("energy") or j.get("stress")]

if journals_with_metrics:
    # Prepare data
    mood_data = []
    for journal in sorted(journals_with_metrics, key=lambda x: x.get("date", "")):
        mood_data.append({
            "Date": journal.get("date"),
            "Mood": journal.get("mood", 0),
            "Energy": journal.get("energy", 0),
            "Stress": journal.get("stress", 0)
        })
    
    df_mood = pd.DataFrame(mood_data)
    
    # Line chart
    st.line_chart(df_mood.set_index("Date")[["Mood", "Energy", "Stress"]])
    
    # Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        avg_mood = df_mood["Mood"].mean()
        st.metric("😊 Average Mood", f"{avg_mood:.1f}/10")
    
    with col_m2:
        avg_energy = df_mood["Energy"].mean()
        st.metric("⚡ Average Energy", f"{avg_energy:.1f}/10")
    
    with col_m3:
        avg_stress = df_mood["Stress"].mean()
        st.metric("😰 Average Stress", f"{avg_stress:.1f}/10")
else:
    st.info("No mood data in this range. Track your mood in the Daily Dashboard!")

st.markdown("---")

# Habit Performance
st.markdown("### 🎯 Habit Performance")

if active_habits:
    habit_performance = []
    
    for habit in active_habits:
        entries = habit.get("entries", [])
        entries_in_range = [e for e in entries 
                           if e.get("date", "") >= start_date 
                           and e.get("completed")]
        
        # Calculate days in range
        days_in_range = (date.today() - datetime.strptime(start_date, "%Y-%m-%d").date()).days
        completion_rate = (len(entries_in_range) / days_in_range * 100) if days_in_range > 0 else 0
        
        habit_performance.append({
            "Habit": habit.get("name"),
            "Completions": len(entries_in_range),
            "Completion Rate": f"{completion_rate:.1f}%"
        })
    
    df_habits = pd.DataFrame(habit_performance)
    st.dataframe(df_habits, use_container_width=True, hide_index=True)
    
    # Bar chart
    st.bar_chart(df_habits.set_index("Habit")["Completions"])
else:
    st.info("No active habits to track.")

st.markdown("---")

# Correlation Insights
st.markdown("### 🔍 AI Insights")

if st.button("✨ Generate Insights", use_container_width=True):
    with st.spinner("Analyzing patterns..."):
        # Gather stats
        stats_text = f"""
Time Range: {time_range}
Tasks Completed: {len(completed_tasks)}
Journal Entries: {len(journals_in_range)}
Average Mood: {avg_mood:.1f}/10
Active Habits: {len(active_habits)}
"""
        
        prompt = f"""Analyze these personal productivity and wellbeing metrics:

{stats_text}

Provide:
1. One key productivity pattern
2. One insight about mood/wellbeing correlation
3. One actionable recommendation

Keep it under 120 words."""

        insights = get_ai_response(prompt, max_tokens=200)
        st.success(insights)

st.markdown("---")

# Day of week analysis
st.markdown("### 📅 Day of Week Analysis")

col_dow1, col_dow2 = st.columns(2)

with col_dow1:
    st.markdown("#### Most Productive Days")
    
    day_productivity = {}
    for task in completed_tasks:
        if task.get("completed_at"):
            day = datetime.fromisoformat(task.get("completed_at")).strftime("%A")
            day_productivity[day] = day_productivity.get(day, 0) + 1
    
    if day_productivity:
        df_days = pd.DataFrame(list(day_productivity.items()), columns=["Day", "Tasks"])
        
        # Order by day of week
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        df_days["Day"] = pd.Categorical(df_days["Day"], categories=day_order, ordered=True)
        df_days = df_days.sort_values("Day")
        
        st.bar_chart(df_days.set_index("Day"))
    else:
        st.info("Not enough data yet.")

with col_dow2:
    st.markdown("#### Mood by Day")
    
    day_mood = {}
    day_counts = {}
    
    for journal in journals_with_metrics:
        if journal.get("mood") and journal.get("date"):
            day = datetime.strptime(journal.get("date"), "%Y-%m-%d").strftime("%A")
            day_mood[day] = day_mood.get(day, 0) + journal.get("mood", 0)
            day_counts[day] = day_counts.get(day, 0) + 1
    
    if day_mood:
        avg_by_day = {day: day_mood[day] / day_counts[day] for day in day_mood}
        df_mood_days = pd.DataFrame(list(avg_by_day.items()), columns=["Day", "Avg Mood"])
        
        # Order by day of week
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        df_mood_days["Day"] = pd.Categorical(df_mood_days["Day"], categories=day_order, ordered=True)
        df_mood_days = df_mood_days.sort_values("Day")
        
        st.bar_chart(df_mood_days.set_index("Day"))
    else:
        st.info("Not enough mood data yet.")

st.markdown("---")
st.caption("💡 Tip: Track consistently to see meaningful patterns in your data!")

# Advanced Analytics Section
st.markdown("---")
st.markdown("## 🔬 Advanced Analytics")

# Tabs for advanced features
adv_tab1, adv_tab2, adv_tab3, adv_tab4 = st.tabs([
    "📊 Correlation Finder", 
    "🎯 Pattern Recognition", 
    "📈 Predictive Insights",
    "🌐 Holistic Dashboard"
])

with adv_tab1:
    st.markdown("### 📊 Correlation Finder")
    st.caption("Discover relationships between different metrics")
    
    # Prepare correlation data
    correlation_data = []
    
    for journal in journals_in_range:
        if journal.get("mood") and journal.get("energy") and journal.get("stress"):
            entry = {
                "date": journal.get("date"),
                "mood": journal.get("mood", 0),
                "energy": journal.get("energy", 0),
                "stress": journal.get("stress", 0)
            }
            
            # Add health data if available
            health_entries = health_db.get_all()
            health_on_date = next((h for h in health_entries if h.get("date") == journal.get("date")), None)
            
            if health_on_date:
                entry["sleep_hours"] = health_on_date.get("sleep_hours", 0)
                entry["exercise_minutes"] = health_on_date.get("exercise_minutes", 0)
                entry["water_glasses"] = health_on_date.get("water_glasses", 0)
            
            # Add task completion count
            tasks_on_date = [t for t in completed_tasks 
                           if t.get("completed_at") and 
                           datetime.fromisoformat(t.get("completed_at")).date().isoformat() == journal.get("date")]
            entry["tasks_completed"] = len(tasks_on_date)
            
            correlation_data.append(entry)
    
    if len(correlation_data) > 3:
        df_corr = pd.DataFrame(correlation_data)
        
        # Calculate correlations
        st.markdown("#### 🔗 Key Correlations")
        
        numeric_cols = [col for col in df_corr.columns if col != "date"]
        
        if len(numeric_cols) > 1:
            # Create correlation matrix
            corr_matrix = df_corr[numeric_cols].corr()
            
            # Display heatmap using native streamlit
            st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm'), use_container_width=True)
            
            # Find strongest correlations
            st.markdown("#### 💡 Strongest Relationships")
            
            correlations = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    col1, col2 = numeric_cols[i], numeric_cols[j]
                    corr_value = corr_matrix.loc[col1, col2]
                    
                    if abs(corr_value) > 0.3:  # Only show moderate to strong correlations
                        correlations.append({
                            "Metric 1": col1.replace("_", " ").title(),
                            "Metric 2": col2.replace("_", " ").title(),
                            "Correlation": f"{corr_value:.2f}",
                            "Strength": "Strong" if abs(corr_value) > 0.7 else "Moderate"
                        })
            
            if correlations:
                df_corr_insights = pd.DataFrame(correlations)
                df_corr_insights = df_corr_insights.sort_values("Correlation", ascending=False)
                st.dataframe(df_corr_insights, use_container_width=True, hide_index=True)
                
                # Interpretation
                st.markdown("**📖 What this means:**")
                if correlations:
                    top_corr = correlations[0]
                    st.info(f"Your **{top_corr['Metric 1']}** and **{top_corr['Metric 2']}** show a {top_corr['Strength'].lower()} relationship. "
                           f"When one changes, the other tends to change similarly.")
            else:
                st.info("No strong correlations found yet. Keep tracking to discover patterns!")
        else:
            st.info("Not enough data types to calculate correlations.")
    else:
        st.info("Need at least 4 days of combined data to calculate correlations.")

with adv_tab2:
    st.markdown("### 🎯 Pattern Recognition")
    st.caption("Identify recurring patterns in your productivity and wellbeing")
    
    # Best performing days
    st.markdown("#### ⭐ Your Best Days")
    
    if correlation_data and len(correlation_data) > 5:
        df_patterns = pd.DataFrame(correlation_data)
        
        # Create a composite "good day" score
        df_patterns["day_score"] = (
            df_patterns["mood"] * 0.3 +
            df_patterns["energy"] * 0.3 +
            (10 - df_patterns["stress"]) * 0.2 +
            df_patterns["tasks_completed"] * 2
        )
        
        # Get top 5 best days
        top_days = df_patterns.nlargest(5, "day_score")[["date", "mood", "energy", "stress", "tasks_completed", "day_score"]]
        
        st.dataframe(top_days, use_container_width=True, hide_index=True)
        
        # Analyze common factors
        st.markdown("#### 🔍 Common Factors in Best Days")
        
        avg_best_mood = top_days["mood"].mean()
        avg_best_energy = top_days["energy"].mean()
        avg_best_tasks = top_days["tasks_completed"].mean()
        
        col_p1, col_p2, col_p3 = st.columns(3)
        
        with col_p1:
            st.metric("😊 Avg Mood", f"{avg_best_mood:.1f}/10")
        
        with col_p2:
            st.metric("⚡ Avg Energy", f"{avg_best_energy:.1f}/10")
        
        with col_p3:
            st.metric("✅ Avg Tasks", f"{avg_best_tasks:.1f}")
        
        # Sleep pattern analysis (if available)
        if "sleep_hours" in df_patterns.columns:
            avg_sleep_best = top_days["sleep_hours"].mean() if "sleep_hours" in top_days.columns else 0
            avg_sleep_all = df_patterns["sleep_hours"].mean()
            
            st.markdown("#### 😴 Sleep Pattern Insights")
            col_s1, col_s2 = st.columns(2)
            
            with col_s1:
                st.metric("Sleep on Best Days", f"{avg_sleep_best:.1f}h")
            
            with col_s2:
                st.metric("Overall Avg Sleep", f"{avg_sleep_all:.1f}h")
            
            if avg_sleep_best > avg_sleep_all:
                st.success(f"💡 You tend to perform better with {avg_sleep_best - avg_sleep_all:.1f} more hours of sleep!")
    else:
        st.info("Need more data to recognize patterns. Keep tracking!")
    
    # Streak analysis
    st.markdown("#### 🔥 Current Streaks")
    
    if active_habits:
        streaks = []
        
        for habit in active_habits:
            # Calculate current streak
            entries = sorted(habit.get("entries", []), key=lambda x: x.get("date", ""), reverse=True)
            current_streak = 0
            check_date = date.today()
            
            for i in range(30):  # Check last 30 days
                date_str = check_date.isoformat()
                entry = next((e for e in entries if e.get("date") == date_str), None)
                
                if entry and entry.get("completed"):
                    current_streak += 1
                    check_date -= timedelta(days=1)
                else:
                    break
            
            if current_streak > 0:
                streaks.append({
                    "Habit": habit.get("name"),
                    "Streak": f"{current_streak} days 🔥"
                })
        
        if streaks:
            df_streaks = pd.DataFrame(streaks)
            st.dataframe(df_streaks, use_container_width=True, hide_index=True)
        else:
            st.info("No active streaks. Start building one today!")

with adv_tab3:
    st.markdown("### 📈 Predictive Insights")
    st.caption("AI-powered predictions based on your historical data")
    
    if st.button("🔮 Generate Predictions", use_container_width=True):
        with st.spinner("Analyzing trends and generating predictions..."):
            # Gather comprehensive stats
            health_entries = health_db.get_all()
            health_in_range = [h for h in health_entries if h.get("date", "") >= start_date]
            
            finance_entries = finance_db.get_all()
            finance_in_range = [f for f in finance_entries if f.get("date", "") >= start_date]
            
            goals_entries = goals_db.get_all()
            active_goals = [g for g in goals_entries if g.get("progress", 0) < 100]
            
            # Calculate trends
            if len(journals_in_range) > 7:
                recent_mood = [j.get("mood", 0) for j in journals_in_range[-7:] if j.get("mood")]
                older_mood = [j.get("mood", 0) for j in journals_in_range[:-7] if j.get("mood")]
                
                mood_trend = "improving" if (sum(recent_mood)/len(recent_mood) if recent_mood else 0) > (sum(older_mood)/len(older_mood) if older_mood else 0) else "declining"
            else:
                mood_trend = "stable"
            
            stats_text = f"""
Time Range: {time_range}

Productivity:
- Tasks Completed: {len(completed_tasks)}
- Active Goals: {len(active_goals)}
- Active Habits: {len(active_habits)}

Wellbeing:
- Journal Entries: {len(journals_in_range)}
- Average Mood: {avg_mood:.1f}/10
- Mood Trend: {mood_trend}
- Health Entries: {len(health_in_range)}

Financial:
- Transactions Logged: {len(finance_in_range)}
"""
            
            prompt = f"""Based on these personal metrics, provide predictive insights:

{stats_text}

Provide:
1. One prediction about productivity trends for next week
2. One wellbeing forecast based on current patterns
3. One specific recommendation to improve outcomes

Keep it under 150 words. Be specific and actionable."""
            
            predictions = get_ai_response(prompt, max_tokens=250)
            st.success(predictions)
    
    # Goal progress forecasts
    st.markdown("#### 🎯 Goal Completion Forecasts")
    
    goals_with_deadlines = [g for g in goals_db.get_all() 
                           if g.get("deadline") and g.get("progress", 0) < 100]
    
    if goals_with_deadlines:
        forecasts = []
        
        for goal in goals_with_deadlines:
            deadline = datetime.strptime(goal.get("deadline"), "%Y-%m-%d").date()
            days_remaining = (deadline - date.today()).days
            progress = goal.get("progress", 0)
            
            # Simple forecast: at current rate, will we finish on time?
            if days_remaining > 0:
                remaining_progress = 100 - progress
                if progress > 0:
                    # Estimate based on created date
                    created = datetime.fromisoformat(goal.get("created_at", datetime.now().isoformat())).date()
                    days_elapsed = (date.today() - created).days
                    
                    if days_elapsed > 0:
                        progress_per_day = progress / days_elapsed
                        projected_days = remaining_progress / progress_per_day if progress_per_day > 0 else 999
                        
                        status = "✅ On track" if projected_days <= days_remaining else "⚠️ Behind schedule"
                    else:
                        status = "🆕 Just started"
                else:
                    status = "⚠️ Not started"
                
                forecasts.append({
                    "Goal": goal.get("title"),
                    "Progress": f"{progress}%",
                    "Days Left": days_remaining,
                    "Status": status
                })
        
        if forecasts:
            df_forecasts = pd.DataFrame(forecasts)
            st.dataframe(df_forecasts, use_container_width=True, hide_index=True)
    else:
        st.info("No active goals with deadlines to forecast.")

with adv_tab4:
    st.markdown("### 🌐 Holistic Dashboard")
    st.caption("All your key metrics in one view")
    
    # Overall wellness score
    st.markdown("#### 🎯 Wellness Score")
    
    wellness_components = {}
    
    # Mood score (30%)
    if journals_with_metrics:
        wellness_components["Mood"] = avg_mood * 3  # out of 30
    
    # Productivity score (25%)
    days_in_range = (date.today() - datetime.strptime(start_date, "%Y-%m-%d").date()).days
    tasks_per_day = len(completed_tasks) / days_in_range if days_in_range > 0 else 0
    wellness_components["Productivity"] = min(tasks_per_day * 5, 25)  # out of 25
    
    # Habit consistency (20%)
    if active_habits:
        total_completion = 0
        for habit in active_habits:
            entries_in_range = [e for e in habit.get("entries", []) 
                              if e.get("date", "") >= start_date and e.get("completed")]
            completion_rate = len(entries_in_range) / days_in_range if days_in_range > 0 else 0
            total_completion += completion_rate
        
        avg_habit_completion = total_completion / len(active_habits)
        wellness_components["Habits"] = avg_habit_completion * 20  # out of 20
    
    # Health tracking (15%)
    health_in_range = [h for h in health_db.get_all() if h.get("date", "") >= start_date]
    health_score = (len(health_in_range) / days_in_range * 15) if days_in_range > 0 else 0
    wellness_components["Health Tracking"] = min(health_score, 15)  # out of 15
    
    # Gratitude practice (10%)
    gratitude_in_range = [g for g in gratitude_db.get_all() if g.get("date", "") >= start_date]
    gratitude_score = (len(gratitude_in_range) / days_in_range * 10) if days_in_range > 0 else 0
    wellness_components["Gratitude"] = min(gratitude_score, 10)  # out of 10
    
    total_wellness = sum(wellness_components.values())
    
    # Display wellness score
    col_w1, col_w2 = st.columns([1, 2])
    
    with col_w1:
        st.markdown(f"### {total_wellness:.0f}/100")
        st.caption("Overall Wellness Score")
    
    with col_w2:
        # Breakdown
        for component, score in wellness_components.items():
            max_score = {"Mood": 30, "Productivity": 25, "Habits": 20, "Health Tracking": 15, "Gratitude": 10}
            percentage = (score / max_score[component] * 100) if component in max_score else 0
            st.progress(percentage / 100, text=f"{component}: {score:.0f}/{max_score[component]}")
    
    st.markdown("---")
    
    # Quick stats grid
    st.markdown("#### 📊 Quick Stats")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("📝 Journal Entries", len(journals_in_range))
        st.metric("😊 Mood", f"{avg_mood:.1f}/10")
    
    with stat_col2:
        st.metric("✅ Tasks Done", len(completed_tasks))
        st.metric("🎯 Active Goals", len([g for g in goals_db.get_all() if g.get("progress", 0) < 100]))
    
    with stat_col3:
        st.metric("🔥 Active Habits", len(active_habits))
        st.metric("🏃 Health Logs", len(health_in_range))
    
    with stat_col4:
        expenses = sum([f.get("amount", 0) for f in finance_db.get_all() 
                       if f.get("type") == "expense" and f.get("date", "") >= start_date])
        st.metric("💰 Expenses", f"${expenses:,.0f}")
        st.metric("🙏 Gratitude Days", len(gratitude_in_range))

