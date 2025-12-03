"""
Tasks & Projects Manager
Kanban board with task management and AI suggestions
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import tasks_db
from utils.ai import generate_task_suggestions
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Tasks & Projects",
    page_icon="✅",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("✅ Tasks & Projects Manager")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Kanban Board", "➕ Add Task", "📊 Projects"])

# Get all tasks
all_tasks = tasks_db.get_all()
Q = Query()


with tab1:
    st.markdown("### 📋 Kanban Board")
    
    # Filter options
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    
    with col_f1:
        filter_priority = st.selectbox("Filter by Priority", ["All", "high", "medium", "low"], key="filter_priority")
    
    with col_f2:
        filter_tag = st.selectbox("Filter by Tag", ["All"] + list(set([tag for t in all_tasks for tag in t.get("tags", [])])), key="filter_tag")
    
    with col_f3:
        sort_by = st.selectbox("Sort by", ["Created", "Deadline", "Priority"], key="sort_by")
    
    # Filter tasks
    filtered_tasks = all_tasks.copy()
    
    if filter_priority != "All":
        filtered_tasks = [t for t in filtered_tasks if t.get("priority") == filter_priority]
    
    if filter_tag != "All":
        filtered_tasks = [t for t in filtered_tasks if filter_tag in t.get("tags", [])]
    
    # Kanban columns
    col_todo, col_doing, col_done = st.columns(3)
    
    with col_todo:
        st.markdown("### 📝 To Do")
        todo_tasks = [t for t in filtered_tasks if t.get("status") == "todo"]
        
        for task in todo_tasks:
            with st.container():
                st.markdown(f"**{task.get('title')}**")
                
                priority_color = "🔴" if task.get('priority') == "high" else "🟡" if task.get('priority') == "medium" else "🟢"
                st.caption(f"{priority_color} {task.get('priority', 'low').upper()}")
                
                if task.get('deadline'):
                    deadline = datetime.fromisoformat(task.get('deadline')).date()
                    days_left = (deadline - date.today()).days
                    if days_left < 0:
                        st.error(f"⚠️ Overdue by {-days_left} days")
                    elif days_left == 0:
                        st.warning("⚠️ Due today")
                    else:
                        st.info(f"📅 Due in {days_left} days")
                
                if task.get('tags'):
                    st.caption(f"🏷️ {', '.join(task.get('tags'))}")
                
                col_a, col_b, col_c = st.columns([1, 1, 1])
                
                with col_a:
                    if st.button("▶️", key=f"start_{task.doc_id}"):
                        tasks_db.update({"status": "doing"}, task.doc_id)
                        st.rerun()
                
                with col_b:
                    if st.button("✅", key=f"done_{task.doc_id}"):
                        tasks_db.update({"status": "done", "completed_at": datetime.now().isoformat()}, task.doc_id)
                        st.rerun()
                
                with col_c:
                    if st.button("🗑️", key=f"del_{task.doc_id}"):
                        tasks_db.remove(task.doc_id)
                        st.rerun()
                
                st.markdown("---")
    
    with col_doing:
        st.markdown("### 🔄 Doing")
        doing_tasks = [t for t in filtered_tasks if t.get("status") == "doing"]
        
        for task in doing_tasks:
            with st.container():
                st.markdown(f"**{task.get('title')}**")
                
                priority_color = "🔴" if task.get('priority') == "high" else "🟡" if task.get('priority') == "medium" else "🟢"
                st.caption(f"{priority_color} {task.get('priority', 'low').upper()}")
                
                if task.get('deadline'):
                    deadline = datetime.fromisoformat(task.get('deadline')).date()
                    days_left = (deadline - date.today()).days
                    if days_left < 0:
                        st.error(f"⚠️ Overdue by {-days_left} days")
                    elif days_left == 0:
                        st.warning("⚠️ Due today")
                    else:
                        st.info(f"📅 Due in {days_left} days")
                
                if task.get('tags'):
                    st.caption(f"🏷️ {', '.join(task.get('tags'))}")
                
                col_a, col_b, col_c = st.columns([1, 1, 1])
                
                with col_a:
                    if st.button("⏸️", key=f"pause_{task.doc_id}"):
                        tasks_db.update({"status": "todo"}, task.doc_id)
                        st.rerun()
                
                with col_b:
                    if st.button("✅", key=f"done2_{task.doc_id}"):
                        tasks_db.update({"status": "done", "completed_at": datetime.now().isoformat()}, task.doc_id)
                        st.rerun()
                
                with col_c:
                    if st.button("🗑️", key=f"del2_{task.doc_id}"):
                        tasks_db.remove(task.doc_id)
                        st.rerun()
                
                st.markdown("---")
    
    with col_done:
        st.markdown("### ✅ Done")
        done_tasks = [t for t in filtered_tasks if t.get("status") == "done"]
        
        for task in done_tasks[-10:]:  # Show last 10 completed
            with st.container():
                st.markdown(f"~~{task.get('title')}~~")
                
                if task.get('completed_at'):
                    completed = datetime.fromisoformat(task.get('completed_at'))
                    st.caption(f"✅ {completed.strftime('%b %d, %Y')}")
                
                col_a, col_b = st.columns([1, 1])
                
                with col_a:
                    if st.button("↩️", key=f"undo_{task.doc_id}"):
                        tasks_db.update({"status": "todo"}, task.doc_id)
                        st.rerun()
                
                with col_b:
                    if st.button("🗑️", key=f"del3_{task.doc_id}"):
                        tasks_db.remove(task.doc_id)
                        st.rerun()
                
                st.markdown("---")
    
    # AI Suggestions
    st.markdown("---")
    if st.button("🤖 Get AI Task Suggestions", use_container_width=True):
        with st.spinner("Analyzing your tasks..."):
            active_tasks = [t for t in all_tasks if t.get("status") in ["todo", "doing"]]
            suggestions = generate_task_suggestions(active_tasks, [])
            st.info(suggestions)


with tab2:
    st.markdown("### ➕ Add New Task")
    
    with st.form("add_task_form"):
        task_title = st.text_input("Task Title*", placeholder="What needs to be done?")
        task_description = st.text_area("Description", placeholder="Add details...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            task_priority = st.selectbox("Priority", ["low", "medium", "high"])
            task_deadline = st.date_input("Deadline", value=None)
        
        with col2:
            task_tags_input = st.text_input("Tags (comma-separated)", placeholder="e.g., Tech, Marketing")
            task_status = st.selectbox("Status", ["todo", "doing", "done"])
        
        submitted = st.form_submit_button("➕ Add Task", use_container_width=True)
        
        if submitted and task_title:
            tags = [tag.strip() for tag in task_tags_input.split(",") if tag.strip()]
            
            new_task = {
                "title": task_title,
                "description": task_description,
                "status": task_status,
                "priority": task_priority,
                "deadline": task_deadline.isoformat() if task_deadline else None,
                "tags": tags,
                "created_at": datetime.now().isoformat(),
                "date": date.today().strftime("%Y-%m-%d")
            }
            
            tasks_db.insert(new_task)
            st.success(f"✅ Task added: {task_title}")
            st.rerun()


with tab3:
    st.markdown("### 📊 Projects Overview")
    
    if all_tasks:
        # Calculate project stats by tags
        all_tags = set([tag for t in all_tasks for tag in t.get("tags", [])])
        
        if all_tags:
            project_stats = []
            
            for tag in all_tags:
                tag_tasks = [t for t in all_tasks if tag in t.get("tags", [])]
                total = len(tag_tasks)
                done = len([t for t in tag_tasks if t.get("status") == "done"])
                progress = (done / total * 100) if total > 0 else 0
                
                project_stats.append({
                    "Project": tag,
                    "Total": total,
                    "Done": done,
                    "In Progress": len([t for t in tag_tasks if t.get("status") == "doing"]),
                    "To Do": len([t for t in tag_tasks if t.get("status") == "todo"]),
                    "Progress": f"{progress:.0f}%"
                })
            
            df = pd.DataFrame(project_stats)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Project details
            st.markdown("---")
            st.markdown("### 🎯 Project Details")
            
            selected_project = st.selectbox("Select a project", list(all_tags))
            
            if selected_project:
                project_tasks = [t for t in all_tasks if selected_project in t.get("tags", [])]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Tasks", len(project_tasks))
                
                with col2:
                    done_count = len([t for t in project_tasks if t.get("status") == "done"])
                    st.metric("Completed", done_count)
                
                with col3:
                    progress = (done_count / len(project_tasks) * 100) if project_tasks else 0
                    st.metric("Progress", f"{progress:.0f}%")
                
                # Progress bar
                st.progress(progress / 100)
                
                # Task list
                st.markdown("#### Tasks in this project:")
                for task in project_tasks:
                    status_emoji = "✅" if task.get("status") == "done" else "🔄" if task.get("status") == "doing" else "📝"
                    priority_emoji = "🔴" if task.get("priority") == "high" else "🟡" if task.get("priority") == "medium" else "🟢"
                    st.markdown(f"{status_emoji} {priority_emoji} **{task.get('title')}** - {task.get('status')}")
        else:
            st.info("No projects yet. Add tags to your tasks to create projects!")
    else:
        st.info("No tasks yet. Add your first task to get started!")


# Stats footer
st.markdown("---")
st.markdown("### 📊 Overall Statistics")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("📝 Total Tasks", len(all_tasks))

with stat_col2:
    done_count = len([t for t in all_tasks if t.get("status") == "done"])
    st.metric("✅ Completed", done_count)

with stat_col3:
    doing_count = len([t for t in all_tasks if t.get("status") == "doing"])
    st.metric("🔄 In Progress", doing_count)

with stat_col4:
    todo_count = len([t for t in all_tasks if t.get("status") == "todo"])
    st.metric("📋 To Do", todo_count)
