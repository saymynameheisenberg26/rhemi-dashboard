"""
Health & Wellness Tracker
Track sleep, exercise, water intake, meals, and mental health
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import health_db
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Health & Wellness",
    page_icon="💪",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("💪 Health & Wellness Tracker")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Today's Tracking", "📈 Health Analytics", "⚙️ Settings"])

today = date.today()
today_str = today.strftime("%Y-%m-%d")

Q = Query()


def get_health_entry(date_obj):
    """Get health entry for a specific date."""
    date_str = date_obj.strftime("%Y-%m-%d") if isinstance(date_obj, date) else date_obj
    result = health_db.search(Q.date == date_str)
    return result[0] if result else None


def save_health_entry(date_obj, data):
    """Save or update health entry."""
    date_str = date_obj.strftime("%Y-%m-%d") if isinstance(date_obj, date) else date_obj
    
    existing = get_health_entry(date_str)
    
    data["date"] = date_str
    data["updated_at"] = datetime.now().isoformat()
    
    if existing:
        health_db.update(data, existing.doc_id)
    else:
        health_db.insert(data)


with tab1:
    st.markdown("### 📊 Track Your Health Today")
    
    # Get today's entry
    today_entry = get_health_entry(today)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 😴 Sleep")
        sleep_hours = st.number_input(
            "Hours of sleep",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            value=float(today_entry.get("sleep_hours", 7.0)) if today_entry else 7.0,
            key="sleep_hours"
        )
        
        sleep_quality = st.slider(
            "Sleep quality",
            1, 10,
            today_entry.get("sleep_quality", 5) if today_entry else 5,
            key="sleep_quality"
        )
        
        st.markdown("---")
        
        st.markdown("#### 💧 Hydration")
        water_glasses = st.number_input(
            "Glasses of water (8oz each)",
            min_value=0,
            max_value=20,
            value=today_entry.get("water_glasses", 0) if today_entry else 0,
            key="water_glasses"
        )
        
        st.progress(min(water_glasses / 8, 1.0))
        st.caption(f"Goal: 8 glasses | Progress: {water_glasses}/8")
        
        st.markdown("---")
        
        st.markdown("#### 🏃 Exercise")
        exercise_minutes = st.number_input(
            "Minutes of exercise",
            min_value=0,
            max_value=300,
            value=today_entry.get("exercise_minutes", 0) if today_entry else 0,
            key="exercise_minutes"
        )
        
        exercise_type = st.text_input(
            "Type of exercise",
            value=today_entry.get("exercise_type", "") if today_entry else "",
            placeholder="e.g., Running, Yoga, Gym",
            key="exercise_type"
        )
    
    with col2:
        st.markdown("#### 🍎 Meals & Nutrition")
        
        meals_logged = st.multiselect(
            "Meals eaten today",
            ["Breakfast", "Lunch", "Dinner", "Snacks"],
            default=today_entry.get("meals", []) if today_entry else [],
            key="meals"
        )
        
        healthy_meals = st.slider(
            "How healthy were your meals?",
            1, 10,
            today_entry.get("meal_quality", 5) if today_entry else 5,
            help="1 = Fast food, 10 = Very healthy",
            key="meal_quality"
        )
        
        st.markdown("---")
        
        st.markdown("#### 🧠 Mental Health")
        
        stress_level = st.slider(
            "Stress level",
            1, 10,
            today_entry.get("stress_level", 5) if today_entry else 5,
            key="stress_level"
        )
        
        anxiety_level = st.slider(
            "Anxiety level",
            1, 10,
            today_entry.get("anxiety_level", 5) if today_entry else 5,
            key="anxiety_level"
        )
        
        meditation_minutes = st.number_input(
            "Meditation/mindfulness (minutes)",
            min_value=0,
            max_value=120,
            value=today_entry.get("meditation_minutes", 0) if today_entry else 0,
            key="meditation_minutes"
        )
        
        st.markdown("---")
        
        st.markdown("#### 📝 Health Notes")
        health_notes = st.text_area(
            "Any symptoms, observations, or notes",
            value=today_entry.get("notes", "") if today_entry else "",
            height=100,
            placeholder="e.g., Headache, felt energetic, good workout",
            key="health_notes"
        )
    
    # Save button
    if st.button("💾 Save Today's Health Data", use_container_width=True):
        health_data = {
            "sleep_hours": sleep_hours,
            "sleep_quality": sleep_quality,
            "water_glasses": water_glasses,
            "exercise_minutes": exercise_minutes,
            "exercise_type": exercise_type,
            "meals": meals_logged,
            "meal_quality": healthy_meals,
            "stress_level": stress_level,
            "anxiety_level": anxiety_level,
            "meditation_minutes": meditation_minutes,
            "notes": health_notes
        }
        
        save_health_entry(today, health_data)
        st.success("✅ Health data saved!")
        st.rerun()
    
    # Quick stats
    st.markdown("---")
    st.markdown("### 📊 Today's Summary")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("😴 Sleep", f"{sleep_hours}h")
    
    with stat_col2:
        st.metric("💧 Water", f"{water_glasses}/8")
    
    with stat_col3:
        st.metric("🏃 Exercise", f"{exercise_minutes}min")
    
    with stat_col4:
        st.metric("🧘 Meditation", f"{meditation_minutes}min")


with tab2:
    st.markdown("### 📈 Health Analytics")
    
    # Time range
    time_range = st.selectbox("Time range", ["Last 7 days", "Last 30 days", "Last 90 days"])
    
    if time_range == "Last 7 days":
        days = 7
    elif time_range == "Last 30 days":
        days = 30
    else:
        days = 90
    
    cutoff_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    
    # Get health entries
    all_entries = health_db.search(Q.date >= cutoff_date)
    
    if all_entries:
        # Sort by date
        sorted_entries = sorted(all_entries, key=lambda x: x.get("date", ""))
        
        # Prepare data
        dates = []
        sleep_hours_list = []
        sleep_quality_list = []
        water_list = []
        exercise_list = []
        stress_list = []
        anxiety_list = []
        
        for entry in sorted_entries:
            dates.append(entry.get("date"))
            sleep_hours_list.append(entry.get("sleep_hours", 0))
            sleep_quality_list.append(entry.get("sleep_quality", 0))
            water_list.append(entry.get("water_glasses", 0))
            exercise_list.append(entry.get("exercise_minutes", 0))
            stress_list.append(entry.get("stress_level", 0))
            anxiety_list.append(entry.get("anxiety_level", 0))
        
        # Sleep analytics
        st.markdown("#### 😴 Sleep Patterns")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            sleep_df = pd.DataFrame({
                "Date": dates,
                "Hours": sleep_hours_list,
                "Quality": sleep_quality_list
            })
            st.line_chart(sleep_df.set_index("Date"))
        
        with col2:
            avg_sleep = sum(sleep_hours_list) / len(sleep_hours_list) if sleep_hours_list else 0
            avg_quality = sum(sleep_quality_list) / len(sleep_quality_list) if sleep_quality_list else 0
            
            st.metric("Avg Sleep", f"{avg_sleep:.1f}h")
            st.metric("Avg Quality", f"{avg_quality:.1f}/10")
            
            # Sleep goal check
            if avg_sleep >= 7:
                st.success("✅ Meeting sleep goal!")
            else:
                st.warning("⚠️ Need more sleep")
        
        st.markdown("---")
        
        # Hydration & Exercise
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💧 Hydration Trend")
            water_df = pd.DataFrame({"Date": dates, "Glasses": water_list})
            st.bar_chart(water_df.set_index("Date"))
            
            avg_water = sum(water_list) / len(water_list) if water_list else 0
            st.metric("Daily Average", f"{avg_water:.1f} glasses")
        
        with col2:
            st.markdown("#### 🏃 Exercise Activity")
            exercise_df = pd.DataFrame({"Date": dates, "Minutes": exercise_list})
            st.bar_chart(exercise_df.set_index("Date"))
            
            avg_exercise = sum(exercise_list) / len(exercise_list) if exercise_list else 0
            total_exercise = sum(exercise_list)
            st.metric("Daily Average", f"{avg_exercise:.0f} min")
            st.metric("Total", f"{total_exercise} min")
        
        st.markdown("---")
        
        # Mental health
        st.markdown("#### 🧠 Mental Health Trends")
        
        mental_df = pd.DataFrame({
            "Date": dates,
            "Stress": stress_list,
            "Anxiety": anxiety_list
        })
        st.line_chart(mental_df.set_index("Date"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_stress = sum(stress_list) / len(stress_list) if stress_list else 0
            st.metric("Avg Stress", f"{avg_stress:.1f}/10")
        
        with col2:
            avg_anxiety = sum(anxiety_list) / len(anxiety_list) if anxiety_list else 0
            st.metric("Avg Anxiety", f"{avg_anxiety:.1f}/10")
        
        st.markdown("---")
        
        # Correlations
        st.markdown("#### 🔍 Health Insights")
        
        # Sleep vs Stress correlation
        if len(sleep_hours_list) > 5 and len(stress_list) > 5:
            import numpy as np
            correlation = np.corrcoef(sleep_hours_list, stress_list)[0, 1]
            
            if correlation < -0.3:
                st.info("📊 More sleep correlates with lower stress!")
            elif correlation > 0.3:
                st.warning("📊 Higher stress may be affecting your sleep")
        
        # Exercise consistency
        exercise_days = sum(1 for e in exercise_list if e > 0)
        consistency = (exercise_days / len(exercise_list)) * 100 if exercise_list else 0
        
        st.metric("Exercise Consistency", f"{consistency:.0f}%")
        
        if consistency >= 70:
            st.success("🎉 Great consistency!")
        elif consistency >= 40:
            st.info("💪 Good effort, keep it up!")
        else:
            st.warning("⚠️ Try to exercise more regularly")
    
    else:
        st.info("No health data tracked yet. Start tracking in the 'Today's Tracking' tab!")


with tab3:
    st.markdown("### ⚙️ Health Settings & Goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Daily Goals")
        
        sleep_goal = st.number_input("Sleep goal (hours)", min_value=4.0, max_value=12.0, value=8.0, step=0.5)
        water_goal = st.number_input("Water goal (glasses)", min_value=1, max_value=20, value=8)
        exercise_goal = st.number_input("Exercise goal (minutes)", min_value=0, max_value=180, value=30)
        
        if st.button("Save Goals"):
            from utils.db import set_setting
            set_setting("health_sleep_goal", sleep_goal)
            set_setting("health_water_goal", water_goal)
            set_setting("health_exercise_goal", exercise_goal)
            st.success("Goals saved!")
    
    with col2:
        st.markdown("#### 📊 View Past Entries")
        
        selected_date = st.date_input("Select a date", max_value=today)
        
        if selected_date:
            past_entry = get_health_entry(selected_date)
            
            if past_entry:
                st.markdown(f"**{selected_date.strftime('%B %d, %Y')}**")
                st.markdown(f"- Sleep: {past_entry.get('sleep_hours', 0)}h (Quality: {past_entry.get('sleep_quality', 0)}/10)")
                st.markdown(f"- Water: {past_entry.get('water_glasses', 0)} glasses")
                st.markdown(f"- Exercise: {past_entry.get('exercise_minutes', 0)} min ({past_entry.get('exercise_type', 'N/A')})")
                st.markdown(f"- Stress: {past_entry.get('stress_level', 0)}/10")
                st.markdown(f"- Anxiety: {past_entry.get('anxiety_level', 0)}/10")
                
                if past_entry.get("notes"):
                    st.markdown(f"**Notes:** {past_entry.get('notes')}")
            else:
                st.info("No data for this date")


st.markdown("---")
st.caption("💡 Tip: Consistent health tracking helps identify patterns and improve your wellbeing!")
