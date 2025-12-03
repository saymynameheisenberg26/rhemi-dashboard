"""
Personal Journal
Daily, weekly, and monthly journal with AI analysis
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import journal_db, get_journal_entry, save_journal_entry
from utils.ai import analyze_journal_entry, generate_journal_summary, extract_goals_from_journal
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Journal",
    page_icon="📝",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("📝 Personal Journal")

# Tabs
tab1, tab2, tab3 = st.tabs(["✍️ Daily Journal", "📅 Past Entries", "📊 Insights"])


with tab1:
    st.markdown("### ✍️ Today's Journal")
    
    today = date.today()
    entry = get_journal_entry(today)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        journal_content = st.text_area(
            "Write about your day...",
            value=entry.get("content", "") if entry else "",
            height=400,
            placeholder="What happened today? How do you feel? What are you thinking about?"
        )
        
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            if st.button("💾 Save Entry", use_container_width=True):
                save_journal_entry(
                    today,
                    journal_content,
                    entry.get("mood") if entry else None,
                    entry.get("energy") if entry else None,
                    entry.get("stress") if entry else None
                )
                st.success("✅ Journal entry saved!")
                st.rerun()
        
        with col_b:
            if st.button("🗑️ Clear", use_container_width=True):
                if entry:
                    save_journal_entry(today, "", None, None, None)
                    st.success("✅ Entry cleared!")
                    st.rerun()
    
    with col2:
        st.markdown("### 🤖 AI Tools")
        
        if journal_content:
            if st.button("🔍 Analyze Entry", use_container_width=True):
                with st.spinner("Analyzing..."):
                    analysis = analyze_journal_entry(journal_content)
                    st.info(analysis)
            
            if st.button("🎯 Extract Goals", use_container_width=True):
                with st.spinner("Extracting goals..."):
                    goals = extract_goals_from_journal(journal_content)
                    st.success(goals)
            
            st.markdown("---")
            
            # Word count
            word_count = len(journal_content.split())
            st.metric("Word Count", word_count)
            
            # Mood tracking (if saved)
            if entry:
                if entry.get("mood"):
                    st.metric("😊 Mood", f"{entry.get('mood')}/10")
                if entry.get("energy"):
                    st.metric("⚡ Energy", f"{entry.get('energy')}/10")
                if entry.get("stress"):
                    st.metric("😰 Stress", f"{entry.get('stress')}/10")
        else:
            st.info("Start writing to use AI tools...")


with tab2:
    st.markdown("### 📅 Past Journal Entries")
    
    # Date selector
    selected_date = st.date_input("Select a date", value=date.today(), max_value=date.today())
    
    if selected_date:
        selected_entry = get_journal_entry(selected_date)
        
        if selected_entry:
            st.markdown(f"#### {selected_date.strftime('%A, %B %d, %Y')}")
            
            # Metrics row
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if selected_entry.get("mood"):
                    st.metric("😊 Mood", f"{selected_entry.get('mood')}/10")
            
            with col2:
                if selected_entry.get("energy"):
                    st.metric("⚡ Energy", f"{selected_entry.get('energy')}/10")
            
            with col3:
                if selected_entry.get("stress"):
                    st.metric("😰 Stress", f"{selected_entry.get('stress')}/10")
            
            st.markdown("---")
            st.markdown(selected_entry.get("content", ""))
            
            # AI Analysis
            if selected_entry.get("content"):
                if st.button("🔍 Analyze This Entry"):
                    with st.spinner("Analyzing..."):
                        analysis = analyze_journal_entry(selected_entry.get("content"))
                        st.info(analysis)
        else:
            st.info(f"No journal entry for {selected_date.strftime('%B %d, %Y')}")
    
    st.markdown("---")
    st.markdown("### 📚 Recent Entries")
    
    # Show last 7 days
    all_entries = journal_db.get_all()
    
    if all_entries:
        # Sort by date descending
        sorted_entries = sorted(all_entries, key=lambda x: x.get("date", ""), reverse=True)
        
        for entry in sorted_entries[:7]:
            entry_date = datetime.strptime(entry.get("date"), "%Y-%m-%d").date()
            
            with st.expander(f"📝 {entry_date.strftime('%A, %B %d, %Y')}"):
                content = entry.get("content", "")
                preview = content[:200] + "..." if len(content) > 200 else content
                st.markdown(preview)
                
                if entry.get("mood") or entry.get("energy") or entry.get("stress"):
                    metrics_text = []
                    if entry.get("mood"):
                        metrics_text.append(f"😊 {entry.get('mood')}/10")
                    if entry.get("energy"):
                        metrics_text.append(f"⚡ {entry.get('energy')}/10")
                    if entry.get("stress"):
                        metrics_text.append(f"😰 {entry.get('stress')}/10")
                    
                    st.caption(" | ".join(metrics_text))
    else:
        st.info("No journal entries yet. Start writing!")


with tab3:
    st.markdown("### 📊 Journal Insights")
    
    all_entries = journal_db.get_all()
    
    if len(all_entries) >= 3:
        # Time range selector
        time_range = st.selectbox("Select time range", ["Last 7 days", "Last 30 days", "All time"])
        
        # Filter entries by time range
        if time_range == "Last 7 days":
            cutoff_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
            filtered_entries = [e for e in all_entries if e.get("date", "") >= cutoff_date]
        elif time_range == "Last 30 days":
            cutoff_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
            filtered_entries = [e for e in all_entries if e.get("date", "") >= cutoff_date]
        else:
            filtered_entries = all_entries
        
        if filtered_entries:
            # Generate AI summary
            if st.button("✨ Generate AI Summary", use_container_width=True):
                with st.spinner("Generating summary..."):
                    summary = generate_journal_summary(filtered_entries)
                    st.success(summary)
            
            st.markdown("---")
            
            # Mood, Energy, Stress trends
            entries_with_metrics = [e for e in filtered_entries 
                                   if e.get("mood") or e.get("energy") or e.get("stress")]
            
            if entries_with_metrics:
                st.markdown("### 📈 Trends")
                
                # Prepare data
                dates = []
                moods = []
                energies = []
                stresses = []
                
                for entry in sorted(entries_with_metrics, key=lambda x: x.get("date", "")):
                    dates.append(entry.get("date"))
                    moods.append(entry.get("mood", 0))
                    energies.append(entry.get("energy", 0))
                    stresses.append(entry.get("stress", 0))
                
                # Create DataFrame
                df = pd.DataFrame({
                    "Date": dates,
                    "Mood": moods,
                    "Energy": energies,
                    "Stress": stresses
                })
                
                # Line chart
                st.line_chart(df.set_index("Date")[["Mood", "Energy", "Stress"]])
                
                # Average metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_mood = sum(moods) / len(moods) if moods else 0
                    st.metric("😊 Avg Mood", f"{avg_mood:.1f}/10")
                
                with col2:
                    avg_energy = sum(energies) / len(energies) if energies else 0
                    st.metric("⚡ Avg Energy", f"{avg_energy:.1f}/10")
                
                with col3:
                    avg_stress = sum(stresses) / len(stresses) if stresses else 0
                    st.metric("😰 Avg Stress", f"{avg_stress:.1f}/10")
            
            st.markdown("---")
            
            # Writing stats
            st.markdown("### ✍️ Writing Statistics")
            
            total_entries = len(filtered_entries)
            total_words = sum([len(e.get("content", "").split()) for e in filtered_entries])
            avg_words = total_words / total_entries if total_entries > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📝 Entries", total_entries)
            
            with col2:
                st.metric("📊 Total Words", total_words)
            
            with col3:
                st.metric("📏 Avg Words/Entry", f"{avg_words:.0f}")
        else:
            st.info("No entries in selected time range.")
    else:
        st.info("Write at least 3 journal entries to see insights!")


st.markdown("---")
st.caption("💡 Tip: Journal regularly to track your thoughts, feelings, and progress over time.")
