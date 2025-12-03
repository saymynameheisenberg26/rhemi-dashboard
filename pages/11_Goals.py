"""
Goals & OKRs (Objectives and Key Results)
Set and track long-term goals, quarterly OKRs, and milestones
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import goals_db
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Goals & OKRs",
    page_icon="🎯",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("🎯 Goals & OKRs")

# Tabs
tab1, tab2, tab3 = st.tabs(["🎯 Active Goals", "➕ Add Goal/OKR", "📊 Progress Overview"])

Q = Query()


with tab1:
    st.markdown("### 🎯 Your Active Goals")
    
    # Filter
    goal_type_filter = st.selectbox("Filter by type", ["All", "Long-term Goal", "Quarterly OKR", "Monthly Goal", "Milestone"])
    
    all_goals = goals_db.get_all()
    active_goals = [g for g in all_goals if g.get("status") != "completed"]
    
    if goal_type_filter != "All":
        active_goals = [g for g in active_goals if g.get("type") == goal_type_filter]
    
    if active_goals:
        for goal in active_goals:
            with st.expander(f"{'🎯' if goal.get('type') == 'Long-term Goal' else '📅' if goal.get('type') == 'Quarterly OKR' else '📌'} {goal.get('title')}"):
                col_info, col_progress = st.columns([2, 1])
                
                with col_info:
                    st.markdown(f"**Type:** {goal.get('type', 'Goal')}")
                    
                    if goal.get('description'):
                        st.markdown(f"**Description:** {goal.get('description')}")
                    
                    if goal.get('deadline'):
                        deadline = datetime.fromisoformat(goal.get('deadline')).date()
                        days_left = (deadline - date.today()).days
                        
                        if days_left < 0:
                            st.error(f"⚠️ Overdue by {-days_left} days")
                        elif days_left == 0:
                            st.warning("⚠️ Due today!")
                        else:
                            st.info(f"📅 {days_left} days remaining")
                    
                    # Key Results (for OKRs)
                    if goal.get('key_results'):
                        st.markdown("**Key Results:**")
                        for i, kr in enumerate(goal.get('key_results', [])):
                            kr_progress = kr.get('progress', 0)
                            st.markdown(f"{i+1}. {kr.get('description')} - {kr_progress}%")
                            st.progress(kr_progress / 100)
                    
                    # Milestones
                    if goal.get('milestones'):
                        st.markdown("**Milestones:**")
                        for milestone in goal.get('milestones', []):
                            status = "✅" if milestone.get('completed') else "⏳"
                            st.markdown(f"{status} {milestone.get('title')}")
                
                with col_progress:
                    # Progress
                    progress = goal.get('progress', 0)
                    st.metric("Progress", f"{progress}%")
                    st.progress(progress / 100)
                    
                    # Update progress
                    new_progress = st.slider(
                        "Update progress",
                        0, 100,
                        progress,
                        key=f"progress_{goal.doc_id}"
                    )
                    
                    if st.button("💾 Update", key=f"update_{goal.doc_id}"):
                        goals_db.update({"progress": new_progress}, goal.doc_id)
                        st.success("Updated!")
                        st.rerun()
                    
                    # Mark complete
                    if st.button("✅ Complete", key=f"complete_{goal.doc_id}"):
                        goals_db.update({
                            "status": "completed",
                            "progress": 100,
                            "completed_at": datetime.now().isoformat()
                        }, goal.doc_id)
                        st.success("Goal completed! 🎉")
                        st.rerun()
                    
                    # Delete
                    if st.button("🗑️ Delete", key=f"delete_{goal.doc_id}"):
                        goals_db.remove(goal.doc_id)
                        st.rerun()
    else:
        st.info("No active goals. Set your first goal in the 'Add Goal/OKR' tab!")


with tab2:
    st.markdown("### ➕ Create New Goal or OKR")
    
    goal_type = st.selectbox(
        "Goal Type",
        ["Long-term Goal", "Quarterly OKR", "Monthly Goal", "Milestone"]
    )
    
    st.info(f"💡 **{goal_type}:** " + {
        "Long-term Goal": "Big vision goals (6 months to 5 years)",
        "Quarterly OKR": "Objectives with measurable Key Results (3 months)",
        "Monthly Goal": "Short-term targets (1 month)",
        "Milestone": "Specific achievement or checkpoint"
    }[goal_type])
    
    with st.form("add_goal"):
        title = st.text_input("Goal Title*", placeholder="e.g., Launch MVP, Reach $10k MRR")
        
        description = st.text_area(
            "Description",
            placeholder="What does success look like? Why is this important?",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            deadline = st.date_input(
                "Target Deadline",
                value=date.today() + timedelta(days=90)
            )
            
            category = st.selectbox(
                "Category",
                ["Personal", "Startup", "Health", "Financial", "Learning", "Career", "Relationships", "Other"]
            )
        
        with col2:
            initial_progress = st.slider("Initial Progress (%)", 0, 100, 0)
            
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        # OKR specific
        if goal_type == "Quarterly OKR":
            st.markdown("#### Key Results (measurable outcomes)")
            
            kr1 = st.text_input("Key Result 1", placeholder="e.g., Acquire 100 users")
            kr1_metric = st.number_input("KR1 Target Value", min_value=0, value=100, key="kr1_val")
            
            kr2 = st.text_input("Key Result 2", placeholder="e.g., Reach 50% user retention")
            kr2_metric = st.number_input("KR2 Target Value", min_value=0, value=50, key="kr2_val")
            
            kr3 = st.text_input("Key Result 3 (optional)", placeholder="e.g., Ship 3 major features")
            kr3_metric = st.number_input("KR3 Target Value", min_value=0, value=0, key="kr3_val") if kr3 else 0
        
        # Milestones
        st.markdown("#### Milestones (optional)")
        milestones_text = st.text_area(
            "Add milestones (one per line)",
            placeholder="- Complete user research\n- Build prototype\n- Launch beta",
            height=100
        )
        
        submitted = st.form_submit_button("🎯 Create Goal", use_container_width=True)
        
        if submitted and title:
            # Parse milestones
            milestones = []
            if milestones_text:
                for line in milestones_text.split("\n"):
                    line = line.strip().lstrip("-•*")
                    if line:
                        milestones.append({
                            "title": line,
                            "completed": False
                        })
            
            # Build key results for OKR
            key_results = []
            if goal_type == "Quarterly OKR":
                if kr1:
                    key_results.append({
                        "description": kr1,
                        "target": kr1_metric,
                        "progress": 0
                    })
                if kr2:
                    key_results.append({
                        "description": kr2,
                        "target": kr2_metric,
                        "progress": 0
                    })
                if kr3:
                    key_results.append({
                        "description": kr3,
                        "target": kr3_metric,
                        "progress": 0
                    })
            
            new_goal = {
                "type": goal_type,
                "title": title,
                "description": description,
                "deadline": deadline.isoformat(),
                "category": category,
                "priority": priority.lower(),
                "progress": initial_progress,
                "status": "active",
                "key_results": key_results,
                "milestones": milestones,
                "created_at": datetime.now().isoformat()
            }
            
            goals_db.insert(new_goal)
            st.success(f"✅ {goal_type} created: {title}")
            st.rerun()


with tab3:
    st.markdown("### 📊 Goals Progress Overview")
    
    all_goals = goals_db.get_all()
    
    if all_goals:
        # Overall metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            active = len([g for g in all_goals if g.get("status") != "completed"])
            st.metric("🎯 Active Goals", active)
        
        with col2:
            completed = len([g for g in all_goals if g.get("status") == "completed"])
            st.metric("✅ Completed", completed)
        
        with col3:
            avg_progress = sum([g.get("progress", 0) for g in all_goals if g.get("status") != "completed"]) / active if active > 0 else 0
            st.metric("📊 Avg Progress", f"{avg_progress:.0f}%")
        
        with col4:
            high_priority = len([g for g in all_goals if g.get("priority") == "high" and g.get("status") != "completed"])
            st.metric("⭐ High Priority", high_priority)
        
        st.markdown("---")
        
        # Goals by category
        st.markdown("#### 📁 Goals by Category")
        
        category_data = {}
        for goal in all_goals:
            cat = goal.get("category", "Other")
            if cat not in category_data:
                category_data[cat] = {"active": 0, "completed": 0}
            
            if goal.get("status") == "completed":
                category_data[cat]["completed"] += 1
            else:
                category_data[cat]["active"] += 1
        
        df_cat = pd.DataFrame([
            {"Category": cat, "Active": data["active"], "Completed": data["completed"]}
            for cat, data in category_data.items()
        ])
        
        st.dataframe(df_cat, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Progress visualization
        st.markdown("#### 📈 Goal Progress")
        
        active_goals = [g for g in all_goals if g.get("status") != "completed"]
        
        if active_goals:
            progress_data = []
            for goal in active_goals:
                progress_data.append({
                    "Goal": goal.get("title")[:30],
                    "Progress": goal.get("progress", 0)
                })
            
            df_progress = pd.DataFrame(progress_data)
            st.bar_chart(df_progress.set_index("Goal"))
        
        st.markdown("---")
        
        # Upcoming deadlines
        st.markdown("#### ⏰ Upcoming Deadlines")
        
        goals_with_deadlines = [g for g in active_goals if g.get("deadline")]
        goals_with_deadlines = sorted(goals_with_deadlines, key=lambda x: x.get("deadline", ""))
        
        if goals_with_deadlines:
            for goal in goals_with_deadlines[:5]:
                deadline = datetime.fromisoformat(goal.get("deadline")).date()
                days_left = (deadline - date.today()).days
                
                col_a, col_b, col_c = st.columns([2, 1, 1])
                
                with col_a:
                    st.markdown(f"**{goal.get('title')}**")
                
                with col_b:
                    st.markdown(f"{deadline.strftime('%b %d, %Y')}")
                
                with col_c:
                    if days_left < 0:
                        st.error(f"{-days_left}d overdue")
                    elif days_left <= 7:
                        st.warning(f"{days_left}d left")
                    else:
                        st.info(f"{days_left}d left")
        
        st.markdown("---")
        
        # Completed goals
        st.markdown("#### 🏆 Recent Completions")
        
        completed_goals = [g for g in all_goals if g.get("status") == "completed"]
        completed_goals = sorted(completed_goals, key=lambda x: x.get("completed_at", ""), reverse=True)
        
        if completed_goals:
            for goal in completed_goals[:5]:
                completed_date = datetime.fromisoformat(goal.get("completed_at")).strftime("%b %d, %Y")
                st.success(f"✅ {goal.get('title')} - Completed on {completed_date}")
        else:
            st.info("No completed goals yet. Keep working towards your goals!")
        
        st.markdown("---")
        
        # Goal insights
        st.markdown("#### 💡 Insights")
        
        # On track vs behind
        on_track = 0
        behind = 0
        
        for goal in active_goals:
            if goal.get("deadline"):
                deadline = datetime.fromisoformat(goal.get("deadline")).date()
                total_days = (deadline - datetime.fromisoformat(goal.get("created_at")).date()).days
                days_passed = (date.today() - datetime.fromisoformat(goal.get("created_at")).date()).days
                
                expected_progress = (days_passed / total_days * 100) if total_days > 0 else 0
                actual_progress = goal.get("progress", 0)
                
                if actual_progress >= expected_progress * 0.8:  # Within 80% of expected
                    on_track += 1
                else:
                    behind += 1
        
        col_i1, col_i2 = st.columns(2)
        
        with col_i1:
            st.metric("✅ On Track", on_track)
        
        with col_i2:
            st.metric("⚠️ Behind Schedule", behind)
        
        if behind > on_track and behind > 0:
            st.warning("💡 Consider reviewing your goals and adjusting priorities or deadlines.")
        elif on_track > 0:
            st.success("🎉 Great progress! Keep up the momentum!")
    
    else:
        st.info("No goals yet. Set your first goal to start tracking progress!")


st.markdown("---")
st.caption("💡 Tip: Review your goals weekly and update progress regularly. Small consistent steps lead to big achievements!")
