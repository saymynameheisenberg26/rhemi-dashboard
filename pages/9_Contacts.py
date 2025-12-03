"""
Contacts & Network (Social CRM)
Manage relationships, contacts, and follow-ups
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import contacts_db
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Contacts & Network",
    page_icon="👥",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("👥 Contacts & Network")

# Tabs
tab1, tab2, tab3 = st.tabs(["📇 Contacts", "➕ Add Contact", "📊 Network Insights"])

Q = Query()


with tab1:
    st.markdown("### 📇 Your Network")
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search contacts", placeholder="Name, company, or tags...")
    
    with col2:
        all_contacts = contacts_db.get_all()
        categories = list(set([c.get("category", "Other") for c in all_contacts]))
        filter_category = st.selectbox("Category", ["All"] + categories)
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Name", "Last Contact", "Priority"])
    
    # Filter contacts
    filtered = all_contacts.copy()
    
    if search_query:
        filtered = [
            c for c in filtered
            if search_query.lower() in c.get("name", "").lower()
            or search_query.lower() in c.get("company", "").lower()
            or search_query.lower() in " ".join(c.get("tags", [])).lower()
        ]
    
    if filter_category != "All":
        filtered = [c for c in filtered if c.get("category") == filter_category]
    
    # Sort
    if sort_by == "Name":
        filtered = sorted(filtered, key=lambda x: x.get("name", "").lower())
    elif sort_by == "Last Contact":
        filtered = sorted(filtered, key=lambda x: x.get("last_contact", ""), reverse=True)
    elif sort_by == "Priority":
        priority_order = {"high": 3, "medium": 2, "low": 1}
        filtered = sorted(filtered, key=lambda x: priority_order.get(x.get("priority", "low"), 0), reverse=True)
    
    st.markdown(f"**{len(filtered)} contact(s)**")
    st.markdown("---")
    
    # Display contacts
    if filtered:
        for contact in filtered:
            with st.expander(f"👤 {contact.get('name', 'Unknown')} - {contact.get('company', 'No company')}"):
                col_info, col_actions = st.columns([3, 1])
                
                with col_info:
                    # Basic info
                    if contact.get("email"):
                        st.markdown(f"📧 {contact.get('email')}")
                    if contact.get("phone"):
                        st.markdown(f"📱 {contact.get('phone')}")
                    if contact.get("company"):
                        st.markdown(f"🏢 {contact.get('company')} - {contact.get('role', 'N/A')}")
                    
                    # Category and priority
                    st.caption(f"📁 {contact.get('category', 'Other')} | Priority: {contact.get('priority', 'low').upper()}")
                    
                    # Tags
                    if contact.get("tags"):
                        st.caption(f"🏷️ {', '.join(contact.get('tags'))}")
                    
                    # Relationship quality
                    if contact.get("relationship_score"):
                        st.caption(f"💫 Relationship: {contact.get('relationship_score')}/10")
                    
                    # Last contact
                    if contact.get("last_contact"):
                        last_contact = datetime.fromisoformat(contact.get("last_contact"))
                        days_ago = (datetime.now() - last_contact).days
                        st.caption(f"🕐 Last contact: {days_ago} days ago")
                        
                        if days_ago > 90:
                            st.warning("⚠️ Haven't contacted in 90+ days!")
                        elif days_ago > 30:
                            st.info("💡 Consider reaching out soon")
                    
                    # Notes
                    if contact.get("notes"):
                        st.markdown("**Notes:**")
                        st.markdown(contact.get("notes"))
                
                with col_actions:
                    # Update last contact
                    if st.button("✅ Contacted Today", key=f"contact_{contact.doc_id}"):
                        contacts_db.update({"last_contact": datetime.now().isoformat()}, contact.doc_id)
                        st.success("Updated!")
                        st.rerun()
                    
                    # Set follow-up
                    follow_up_date = st.date_input("Follow-up", key=f"followup_{contact.doc_id}")
                    if st.button("Set Reminder", key=f"set_followup_{contact.doc_id}"):
                        contacts_db.update({"follow_up": follow_up_date.isoformat()}, contact.doc_id)
                        st.success("Reminder set!")
                        st.rerun()
                    
                    # Delete
                    if st.button("🗑️ Delete", key=f"del_{contact.doc_id}"):
                        contacts_db.remove(contact.doc_id)
                        st.rerun()
    else:
        st.info("No contacts found. Add your first contact in the 'Add Contact' tab!")
    
    # Follow-ups needed
    st.markdown("---")
    st.markdown("### 📅 Follow-ups Needed")
    
    today_str = date.today().isoformat()
    follow_ups = [c for c in all_contacts if c.get("follow_up") and c.get("follow_up") <= today_str]
    
    if follow_ups:
        for contact in follow_ups:
            st.warning(f"📞 Follow up with **{contact.get('name')}** at {contact.get('company', 'N/A')}")
    else:
        st.success("✅ No pending follow-ups!")


with tab2:
    st.markdown("### ➕ Add New Contact")
    
    with st.form("add_contact"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name*", placeholder="John Doe")
            email = st.text_input("Email", placeholder="john@example.com")
            phone = st.text_input("Phone", placeholder="+1 234 567 8900")
            company = st.text_input("Company", placeholder="Acme Corp")
            role = st.text_input("Role/Title", placeholder="CEO, Engineer, Investor")
        
        with col2:
            category = st.selectbox(
                "Category",
                ["Investor", "Customer", "Partner", "Mentor", "Team", "Friend", "Family", "Other"]
            )
            
            priority = st.selectbox("Priority", ["low", "medium", "high"])
            
            relationship_score = st.slider("Relationship Strength", 1, 10, 5)
            
            tags_input = st.text_input("Tags (comma-separated)", placeholder="startup, tech, networking")
            
            met_where = st.text_input("Met at/through", placeholder="Conference, LinkedIn, Friend intro")
        
        notes = st.text_area("Notes", placeholder="Any important details about this contact...", height=100)
        
        submitted = st.form_submit_button("➕ Add Contact", use_container_width=True)
        
        if submitted and name:
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            
            new_contact = {
                "name": name,
                "email": email,
                "phone": phone,
                "company": company,
                "role": role,
                "category": category,
                "priority": priority,
                "relationship_score": relationship_score,
                "tags": tags,
                "met_where": met_where,
                "notes": notes,
                "created_at": datetime.now().isoformat(),
                "last_contact": datetime.now().isoformat()
            }
            
            contacts_db.insert(new_contact)
            st.success(f"✅ Contact added: {name}")
            st.rerun()


with tab3:
    st.markdown("### 📊 Network Insights")
    
    all_contacts = contacts_db.get_all()
    
    if all_contacts:
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Contacts", len(all_contacts))
        
        with col2:
            high_priority = len([c for c in all_contacts if c.get("priority") == "high"])
            st.metric("⭐ High Priority", high_priority)
        
        with col3:
            avg_relationship = sum([c.get("relationship_score", 0) for c in all_contacts]) / len(all_contacts)
            st.metric("💫 Avg Relationship", f"{avg_relationship:.1f}/10")
        
        with col4:
            # Contacts added this month
            month_start = date.today().replace(day=1).isoformat()
            new_this_month = len([c for c in all_contacts if c.get("created_at", "")[:10] >= month_start])
            st.metric("🆕 This Month", new_this_month)
        
        st.markdown("---")
        
        # Category breakdown
        st.markdown("#### 📁 Contacts by Category")
        
        category_data = {}
        for contact in all_contacts:
            cat = contact.get("category", "Other")
            category_data[cat] = category_data.get(cat, 0) + 1
        
        df_cat = pd.DataFrame(list(category_data.items()), columns=["Category", "Count"])
        df_cat = df_cat.sort_values("Count", ascending=False)
        
        col_chart, col_table = st.columns([2, 1])
        
        with col_chart:
            st.bar_chart(df_cat.set_index("Category"))
        
        with col_table:
            st.dataframe(df_cat, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Relationship quality
        st.markdown("#### 💫 Relationship Quality Distribution")
        
        quality_ranges = {
            "Strong (8-10)": len([c for c in all_contacts if c.get("relationship_score", 0) >= 8]),
            "Good (5-7)": len([c for c in all_contacts if 5 <= c.get("relationship_score", 0) < 8]),
            "Weak (1-4)": len([c for c in all_contacts if c.get("relationship_score", 0) < 5])
        }
        
        df_quality = pd.DataFrame(list(quality_ranges.items()), columns=["Quality", "Count"])
        st.bar_chart(df_quality.set_index("Quality"))
        
        st.markdown("---")
        
        # Contact frequency
        st.markdown("#### 🕐 Last Contact Analysis")
        
        contact_recency = {
            "< 7 days": 0,
            "7-30 days": 0,
            "30-90 days": 0,
            "> 90 days": 0,
            "Never": 0
        }
        
        for contact in all_contacts:
            if contact.get("last_contact"):
                last_contact = datetime.fromisoformat(contact.get("last_contact"))
                days_ago = (datetime.now() - last_contact).days
                
                if days_ago < 7:
                    contact_recency["< 7 days"] += 1
                elif days_ago < 30:
                    contact_recency["7-30 days"] += 1
                elif days_ago < 90:
                    contact_recency["30-90 days"] += 1
                else:
                    contact_recency["> 90 days"] += 1
            else:
                contact_recency["Never"] += 1
        
        df_recency = pd.DataFrame(list(contact_recency.items()), columns=["Last Contact", "Count"])
        st.bar_chart(df_recency.set_index("Last Contact"))
        
        # Actionable insights
        st.markdown("---")
        st.markdown("#### 💡 Actionable Insights")
        
        # Contacts needing attention
        needs_attention = [
            c for c in all_contacts
            if c.get("last_contact")
            and (datetime.now() - datetime.fromisoformat(c.get("last_contact"))).days > 90
            and c.get("priority") in ["high", "medium"]
        ]
        
        if needs_attention:
            st.warning(f"⚠️ {len(needs_attention)} important contact(s) haven't been reached out to in 90+ days")
            for contact in needs_attention[:5]:
                st.markdown(f"- {contact.get('name')} ({contact.get('company', 'N/A')})")
        
        # Strong relationships
        strong_relationships = [c for c in all_contacts if c.get("relationship_score", 0) >= 8]
        st.success(f"✅ {len(strong_relationships)} strong relationship(s) - keep nurturing them!")
        
        # Network growth
        contacts_by_month = {}
        for contact in all_contacts:
            if contact.get("created_at"):
                month = contact.get("created_at")[:7]
                contacts_by_month[month] = contacts_by_month.get(month, 0) + 1
        
        st.markdown("#### 📈 Network Growth Over Time")
        df_growth = pd.DataFrame(list(contacts_by_month.items()), columns=["Month", "New Contacts"])
        df_growth = df_growth.sort_values("Month")
        st.line_chart(df_growth.set_index("Month"))
    
    else:
        st.info("No contacts yet. Start building your network in the 'Add Contact' tab!")


st.markdown("---")
st.caption("💡 Tip: Nurture your relationships by regular check-ins. Strong networks open doors!")
