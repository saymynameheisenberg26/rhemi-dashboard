"""
Gratitude & Reflection
Daily gratitude, wins, lessons learned, and celebrations
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import gratitude_db
from utils.ai import get_ai_response
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Gratitude & Wins",
    page_icon="🙏",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("🙏 Gratitude & Reflection")

# Tabs
tab1, tab2, tab3 = st.tabs(["✍️ Today's Reflection", "📚 Past Reflections", "📊 Insights"])

today = date.today()
today_str = today.strftime("%Y-%m-%d")

Q = Query()


def get_gratitude_entry(date_obj):
    """Get gratitude entry for a specific date."""
    date_str = date_obj.strftime("%Y-%m-%d") if isinstance(date_obj, date) else date_obj
    result = gratitude_db.search(Q.date == date_str)
    return result[0] if result else None


def save_gratitude_entry(date_obj, data):
    """Save or update gratitude entry."""
    date_str = date_obj.strftime("%Y-%m-%d") if isinstance(date_obj, date) else date_obj
    
    existing = get_gratitude_entry(date_str)
    
    data["date"] = date_str
    data["updated_at"] = datetime.now().isoformat()
    
    if existing:
        gratitude_db.update(data, existing.doc_id)
    else:
        gratitude_db.insert(data)


with tab1:
    st.markdown("### 🌟 Today's Reflection")
    
    st.info("💡 Taking time for gratitude and reflection improves mental health and happiness!")
    
    # Get today's entry
    today_entry = get_gratitude_entry(today)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🙏 Gratitude")
        
        gratitude_1 = st.text_input(
            "What are you grateful for today? (1)",
            value=today_entry.get("gratitude_1", "") if today_entry else "",
            placeholder="e.g., Good health, supportive team, progress on project",
            key="grat1"
        )
        
        gratitude_2 = st.text_input(
            "What are you grateful for today? (2)",
            value=today_entry.get("gratitude_2", "") if today_entry else "",
            placeholder="e.g., A great conversation, learning opportunity",
            key="grat2"
        )
        
        gratitude_3 = st.text_input(
            "What are you grateful for today? (3)",
            value=today_entry.get("gratitude_3", "") if today_entry else "",
            placeholder="e.g., Family time, beautiful weather",
            key="grat3"
        )
        
        st.markdown("---")
        
        st.markdown("#### 🎯 Wins of the Day")
        
        wins = st.text_area(
            "What did you accomplish or succeed at today?",
            value=today_entry.get("wins", "") if today_entry else "",
            height=150,
            placeholder="Big or small - celebrate your wins!\n\ne.g., Closed a deal, fixed a bug, had a great workout, helped someone",
            key="wins"
        )
    
    with col2:
        st.markdown("#### 📚 Lessons Learned")
        
        lessons = st.text_area(
            "What did you learn today?",
            value=today_entry.get("lessons", "") if today_entry else "",
            height=120,
            placeholder="New skills, insights, mistakes that taught you something",
            key="lessons"
        )
        
        st.markdown("---")
        
        st.markdown("#### 💪 Challenges Overcome")
        
        challenges = st.text_area(
            "What challenges did you face and how did you handle them?",
            value=today_entry.get("challenges", "") if today_entry else "",
            height=120,
            placeholder="Difficult situations, obstacles, how you persevered",
            key="challenges"
        )
        
        st.markdown("---")
        
        st.markdown("#### ✨ Tomorrow's Intention")
        
        intention = st.text_input(
            "What's your main focus for tomorrow?",
            value=today_entry.get("intention", "") if today_entry else "",
            placeholder="e.g., Be more patient, ship the feature, connect with team",
            key="intention"
        )
    
    # Mood/satisfaction
    st.markdown("---")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        happiness = st.slider(
            "😊 Overall Happiness Today",
            1, 10,
            today_entry.get("happiness", 7) if today_entry else 7,
            key="happiness"
        )
    
    with col_m2:
        satisfaction = st.slider(
            "✅ Life Satisfaction",
            1, 10,
            today_entry.get("satisfaction", 7) if today_entry else 7,
            key="satisfaction"
        )
    
    # Save button
    if st.button("💾 Save Reflection", use_container_width=True):
        reflection_data = {
            "gratitude_1": gratitude_1,
            "gratitude_2": gratitude_2,
            "gratitude_3": gratitude_3,
            "wins": wins,
            "lessons": lessons,
            "challenges": challenges,
            "intention": intention,
            "happiness": happiness,
            "satisfaction": satisfaction
        }
        
        save_gratitude_entry(today, reflection_data)
        st.success("✅ Reflection saved! Keep up the great practice!")
        st.rerun()
    
    # AI reflection
    st.markdown("---")
    
    if st.button("🤖 Generate Reflection Insight"):
        if gratitude_1 or wins or lessons:
            with st.spinner("Generating insight..."):
                prompt = f"""Based on today's reflection:

Gratitude: {gratitude_1}, {gratitude_2}, {gratitude_3}
Wins: {wins}
Lessons: {lessons}
Challenges: {challenges}

Provide:
1. A brief encouraging comment
2. One pattern or theme you notice
3. One suggestion for tomorrow

Keep it under 100 words, warm and supportive."""

                insight = get_ai_response(prompt, max_tokens=200)
                st.success(insight)
        else:
            st.warning("Fill in at least one section to get AI insights!")


with tab2:
    st.markdown("### 📚 Past Reflections")
    
    # Date selector
    selected_date = st.date_input("Select a date", value=date.today(), max_value=date.today())
    
    if selected_date:
        past_entry = get_gratitude_entry(selected_date)
        
        if past_entry:
            st.markdown(f"#### {selected_date.strftime('%A, %B %d, %Y')}")
            
            # Metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("😊 Happiness", f"{past_entry.get('happiness', 0)}/10")
            
            with col2:
                st.metric("✅ Satisfaction", f"{past_entry.get('satisfaction', 0)}/10")
            
            st.markdown("---")
            
            # Content
            if past_entry.get("gratitude_1") or past_entry.get("gratitude_2") or past_entry.get("gratitude_3"):
                st.markdown("**🙏 Gratitude:**")
                if past_entry.get("gratitude_1"):
                    st.markdown(f"- {past_entry.get('gratitude_1')}")
                if past_entry.get("gratitude_2"):
                    st.markdown(f"- {past_entry.get('gratitude_2')}")
                if past_entry.get("gratitude_3"):
                    st.markdown(f"- {past_entry.get('gratitude_3')}")
                st.markdown("")
            
            if past_entry.get("wins"):
                st.markdown("**🎯 Wins:**")
                st.markdown(past_entry.get("wins"))
                st.markdown("")
            
            if past_entry.get("lessons"):
                st.markdown("**📚 Lessons:**")
                st.markdown(past_entry.get("lessons"))
                st.markdown("")
            
            if past_entry.get("challenges"):
                st.markdown("**💪 Challenges:**")
                st.markdown(past_entry.get("challenges"))
                st.markdown("")
            
            if past_entry.get("intention"):
                st.markdown(f"**✨ Intention:** {past_entry.get('intention')}")
        else:
            st.info(f"No reflection for {selected_date.strftime('%B %d, %Y')}")
    
    st.markdown("---")
    st.markdown("### 📅 Recent Reflections")
    
    # Show last 7 days
    all_entries = gratitude_db.get_all()
    
    if all_entries:
        sorted_entries = sorted(all_entries, key=lambda x: x.get("date", ""), reverse=True)
        
        for entry in sorted_entries[:7]:
            entry_date = datetime.strptime(entry.get("date"), "%Y-%m-%d").date()
            
            with st.expander(f"🌟 {entry_date.strftime('%A, %B %d, %Y')} - Happiness: {entry.get('happiness', 0)}/10"):
                if entry.get("wins"):
                    st.markdown(f"**🎯 Wins:** {entry.get('wins')[:100]}...")
                
                gratitudes = [entry.get("gratitude_1"), entry.get("gratitude_2"), entry.get("gratitude_3")]
                gratitudes = [g for g in gratitudes if g]
                if gratitudes:
                    st.markdown(f"**🙏 Grateful for:** {', '.join(gratitudes)}")
    else:
        st.info("No reflections yet. Start your gratitude practice today!")


with tab3:
    st.markdown("### 📊 Gratitude & Happiness Insights")
    
    all_entries = gratitude_db.get_all()
    
    if len(all_entries) >= 3:
        # Time range
        time_range = st.selectbox("Time range", ["Last 7 days", "Last 30 days", "All time"])
        
        if time_range == "Last 7 days":
            cutoff = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        elif time_range == "Last 30 days":
            cutoff = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        else:
            cutoff = "2000-01-01"
        
        filtered = [e for e in all_entries if e.get("date", "") >= cutoff]
        
        if filtered:
            # Prepare data
            dates = []
            happiness_scores = []
            satisfaction_scores = []
            
            for entry in sorted(filtered, key=lambda x: x.get("date", "")):
                dates.append(entry.get("date"))
                happiness_scores.append(entry.get("happiness", 0))
                satisfaction_scores.append(entry.get("satisfaction", 0))
            
            # Happiness & Satisfaction trends
            st.markdown("#### 😊 Happiness & Satisfaction Trends")
            
            df = pd.DataFrame({
                "Date": dates,
                "Happiness": happiness_scores,
                "Satisfaction": satisfaction_scores
            })
            
            st.line_chart(df.set_index("Date"))
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_happiness = sum(happiness_scores) / len(happiness_scores)
                st.metric("😊 Avg Happiness", f"{avg_happiness:.1f}/10")
            
            with col2:
                avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
                st.metric("✅ Avg Satisfaction", f"{avg_satisfaction:.1f}/10")
            
            with col3:
                consistency = len(filtered)
                st.metric("📝 Reflections", consistency)
            
            st.markdown("---")
            
            # Gratitude word cloud data
            st.markdown("#### 🙏 Common Themes in Gratitude")
            
            all_gratitudes = []
            for entry in filtered:
                all_gratitudes.extend([
                    entry.get("gratitude_1", ""),
                    entry.get("gratitude_2", ""),
                    entry.get("gratitude_3", "")
                ])
            
            all_gratitudes = [g for g in all_gratitudes if g]
            
            if all_gratitudes:
                st.markdown("**Recent gratitudes:**")
                for grat in all_gratitudes[-10:]:
                    st.markdown(f"- {grat}")
            
            st.markdown("---")
            
            # Wins summary
            st.markdown("#### 🎯 Recent Wins")
            
            wins_list = [e.get("wins", "") for e in filtered if e.get("wins")]
            
            if wins_list:
                for win in wins_list[-5:]:
                    st.success(f"✨ {win[:150]}...")
            
            st.markdown("---")
            
            # Lessons learned
            st.markdown("#### 📚 Key Lessons")
            
            lessons_list = [e.get("lessons", "") for e in filtered if e.get("lessons")]
            
            if lessons_list:
                for lesson in lessons_list[-5:]:
                    st.info(f"💡 {lesson[:150]}...")
            
            st.markdown("---")
            
            # Streak
            st.markdown("#### 🔥 Reflection Streak")
            
            # Calculate streak
            streak = 0
            current_date = today
            
            while True:
                date_str = current_date.strftime("%Y-%m-%d")
                if any(e.get("date") == date_str for e in all_entries):
                    streak += 1
                    current_date -= timedelta(days=1)
                else:
                    break
            
            st.metric("Current Streak", f"{streak} days")
            
            if streak >= 30:
                st.success("🎉 Amazing! 30+ day streak!")
            elif streak >= 7:
                st.success("✅ Great! One week streak!")
            elif streak > 0:
                st.info(f"💪 Keep going! {7 - streak} more days to a week!")
            
            # AI summary
            st.markdown("---")
            
            if st.button("✨ Generate AI Summary"):
                with st.spinner("Analyzing your reflections..."):
                    recent_gratitudes = ", ".join(all_gratitudes[-10:])
                    recent_wins = " | ".join(wins_list[-3:])
                    
                    prompt = f"""Analyze these recent reflections:

Recent gratitudes: {recent_gratitudes}
Recent wins: {recent_wins}
Average happiness: {avg_happiness:.1f}/10
Reflection consistency: {consistency} entries

Provide:
1. One major theme or pattern
2. One strength you notice
3. One encouraging insight

Keep it under 100 words, warm and insightful."""

                    summary = get_ai_response(prompt, max_tokens=200)
                    st.success(summary)
        else:
            st.info("No reflections in selected time range.")
    else:
        st.info("Write at least 3 reflections to see insights!")


st.markdown("---")
st.caption("💡 Tip: Daily gratitude practice is scientifically proven to increase happiness and reduce stress!")
