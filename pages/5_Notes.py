"""
Notes & Ideas
Capture and organize thoughts with AI categorization
"""
import streamlit as st
from datetime import datetime
from utils.auth import check_password
from utils.db import notes_db
from utils.ai import categorize_note
from tinydb import Query


# Page config
st.set_page_config(
    page_title="Notes & Ideas",
    page_icon="💡",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("💡 Notes & Ideas")

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 All Notes", "➕ New Note", "🔍 Search"])


with tab1:
    st.markdown("### 📚 All Notes")
    
    # Filter by category
    all_notes = notes_db.get_all()
    
    if all_notes:
        categories = list(set([n.get("category", "Uncategorized") for n in all_notes]))
        categories.insert(0, "All")
        
        selected_category = st.selectbox("Filter by category", categories)
        
        # Filter notes
        if selected_category != "All":
            filtered_notes = [n for n in all_notes if n.get("category") == selected_category]
        else:
            filtered_notes = all_notes
        
        # Sort options
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Title A-Z"])
        
        if sort_by == "Newest First":
            filtered_notes = sorted(filtered_notes, key=lambda x: x.get("created_at", ""), reverse=True)
        elif sort_by == "Oldest First":
            filtered_notes = sorted(filtered_notes, key=lambda x: x.get("created_at", ""))
        else:
            filtered_notes = sorted(filtered_notes, key=lambda x: x.get("title", "").lower())
        
        st.markdown(f"**{len(filtered_notes)} note(s)**")
        st.markdown("---")
        
        # Display notes
        for note in filtered_notes:
            with st.expander(f"💡 {note.get('title', 'Untitled')} - 🏷️ {note.get('category', 'Uncategorized')}"):
                st.markdown(note.get("content", ""))
                
                if note.get("tags"):
                    st.caption(f"Tags: {', '.join(note.get('tags'))}")
                
                created = datetime.fromisoformat(note.get("created_at", datetime.now().isoformat()))
                st.caption(f"Created: {created.strftime('%B %d, %Y at %I:%M %p')}")
                
                col_edit, col_delete = st.columns([1, 1])
                
                with col_delete:
                    if st.button("🗑️ Delete", key=f"del_note_{note.doc_id}"):
                        notes_db.remove(note.doc_id)
                        st.success("Note deleted!")
                        st.rerun()
    else:
        st.info("No notes yet. Create your first note in the 'New Note' tab!")


with tab2:
    st.markdown("### ➕ Create New Note")
    
    with st.form("new_note_form"):
        note_title = st.text_input("Title*", placeholder="Give your note a title...")
        note_content = st.text_area("Content*", height=300, placeholder="Write your thoughts, ideas, or notes...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            note_category = st.selectbox(
                "Category",
                ["Idea", "Todo", "Learning", "Personal", "Work", "Random"]
            )
        
        with col2:
            note_tags_input = st.text_input("Tags (comma-separated)", placeholder="e.g., startup, coding")
        
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            auto_categorize = st.checkbox("Auto-categorize with AI", value=False)
        
        submitted = st.form_submit_button("💾 Save Note", use_container_width=True)
        
        if submitted and note_title and note_content:
            tags = [tag.strip() for tag in note_tags_input.split(",") if tag.strip()]
            
            # Auto-categorize if enabled
            if auto_categorize:
                with st.spinner("Categorizing with AI..."):
                    suggested_category = categorize_note(note_content)
                    # Use AI suggestion if it's one of our categories
                    valid_categories = ["Idea", "Todo", "Learning", "Personal", "Work", "Random"]
                    if suggested_category in valid_categories:
                        note_category = suggested_category
            
            new_note = {
                "title": note_title,
                "content": note_content,
                "category": note_category,
                "tags": tags,
                "created_at": datetime.now().isoformat()
            }
            
            notes_db.insert(new_note)
            st.success(f"✅ Note saved: {note_title}")
            st.rerun()


with tab3:
    st.markdown("### 🔍 Search Notes")
    
    search_query = st.text_input("Search by title or content", placeholder="Enter keywords...")
    
    if search_query:
        all_notes = notes_db.get_all()
        
        # Search in title and content
        matching_notes = [
            n for n in all_notes
            if search_query.lower() in n.get("title", "").lower()
            or search_query.lower() in n.get("content", "").lower()
            or search_query.lower() in " ".join(n.get("tags", [])).lower()
        ]
        
        if matching_notes:
            st.markdown(f"**Found {len(matching_notes)} note(s)**")
            st.markdown("---")
            
            for note in matching_notes:
                with st.expander(f"💡 {note.get('title', 'Untitled')} - 🏷️ {note.get('category', 'Uncategorized')}"):
                    st.markdown(note.get("content", ""))
                    
                    if note.get("tags"):
                        st.caption(f"Tags: {', '.join(note.get('tags'))}")
                    
                    created = datetime.fromisoformat(note.get("created_at", datetime.now().isoformat()))
                    st.caption(f"Created: {created.strftime('%B %d, %Y at %I:%M %p')}")
        else:
            st.info("No notes found matching your search.")
    else:
        st.info("Enter a search term to find notes.")
    
    st.markdown("---")
    st.markdown("### 🏷️ Browse by Tag")
    
    all_notes = notes_db.get_all()
    all_tags = set([tag for n in all_notes for tag in n.get("tags", [])])
    
    if all_tags:
        selected_tag = st.selectbox("Select a tag", sorted(all_tags))
        
        if selected_tag:
            tagged_notes = [n for n in all_notes if selected_tag in n.get("tags", [])]
            
            st.markdown(f"**{len(tagged_notes)} note(s) with tag '{selected_tag}'**")
            
            for note in tagged_notes:
                with st.expander(f"💡 {note.get('title', 'Untitled')}"):
                    st.markdown(note.get("content", ""))
    else:
        st.info("No tags yet. Add tags to your notes to browse by tag!")


# Statistics
st.markdown("---")
st.markdown("### 📊 Statistics")

all_notes = notes_db.get_all()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📝 Total Notes", len(all_notes))

with col2:
    categories = set([n.get("category", "Uncategorized") for n in all_notes])
    st.metric("🏷️ Categories", len(categories))

with col3:
    all_tags = set([tag for n in all_notes for tag in n.get("tags", [])])
    st.metric("🔖 Total Tags", len(all_tags))

st.markdown("---")
st.caption("💡 Tip: Use tags to link related ideas together and make them easier to find!")
