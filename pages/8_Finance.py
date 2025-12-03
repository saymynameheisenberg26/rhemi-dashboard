"""
Finance Tracker
Track income, expenses, budget, and startup burn rate
"""
import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import check_password
from utils.db import finance_db, get_setting, set_setting
from tinydb import Query
import pandas as pd


# Page config
st.set_page_config(
    page_title="Finance Tracker",
    page_icon="💰",
    layout="wide"
)

# Authentication
if not check_password():
    st.stop()

st.title("💰 Finance Tracker")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Transactions", "📊 Budget", "🔥 Burn Rate", "📈 Analytics"])

Q = Query()


with tab1:
    st.markdown("### 💳 Add Transaction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("add_transaction"):
            trans_date = st.date_input("Date", value=date.today())
            
            trans_type = st.selectbox("Type", ["Expense", "Income"])
            
            trans_amount = st.number_input(
                "Amount ($)",
                min_value=0.01,
                step=0.01,
                format="%.2f"
            )
            
            trans_category = st.selectbox(
                "Category",
                ["Food & Dining", "Transportation", "Shopping", "Bills & Utilities", 
                 "Healthcare", "Entertainment", "Education", "Salary", "Freelance",
                 "Investment", "Business Revenue", "Other"] if trans_type == "Income" 
                else ["Food & Dining", "Transportation", "Shopping", "Bills & Utilities",
                      "Healthcare", "Entertainment", "Education", "Business Expense",
                      "Software & Tools", "Marketing", "Office", "Other"]
            )
            
            trans_description = st.text_input("Description", placeholder="What was this for?")
            
            trans_tags = st.text_input("Tags (comma-separated)", placeholder="e.g., startup, personal")
            
            submitted = st.form_submit_button("➕ Add Transaction", use_container_width=True)
            
            if submitted and trans_amount > 0:
                tags_list = [t.strip() for t in trans_tags.split(",") if t.strip()]
                
                finance_db.insert({
                    "date": trans_date.strftime("%Y-%m-%d"),
                    "type": trans_type.lower(),
                    "amount": float(trans_amount),
                    "category": trans_category,
                    "description": trans_description,
                    "tags": tags_list,
                    "created_at": datetime.now().isoformat()
                })
                
                st.success(f"✅ {trans_type} of ${trans_amount:.2f} added!")
                st.rerun()
    
    with col2:
        # Quick stats
        today_str = date.today().strftime("%Y-%m-%d")
        month_start = date.today().replace(day=1).strftime("%Y-%m-%d")
        
        all_transactions = finance_db.get_all()
        this_month = [t for t in all_transactions if t.get("date", "") >= month_start]
        
        income_this_month = sum([t.get("amount", 0) for t in this_month if t.get("type") == "income"])
        expenses_this_month = sum([t.get("amount", 0) for t in this_month if t.get("type") == "expense"])
        
        st.metric("💵 Income (This Month)", f"${income_this_month:,.2f}")
        st.metric("💸 Expenses (This Month)", f"${expenses_this_month:,.2f}")
        st.metric("📊 Net", f"${income_this_month - expenses_this_month:,.2f}")
    
    st.markdown("---")
    st.markdown("### 📋 Recent Transactions")
    
    # Filter options
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        filter_type = st.selectbox("Filter by type", ["All", "Income", "Expense"])
    
    with col_f2:
        filter_timeframe = st.selectbox("Timeframe", ["This Month", "Last 30 Days", "Last 90 Days", "All Time"])
    
    with col_f3:
        filter_category = st.selectbox("Category", ["All"] + list(set([t.get("category") for t in all_transactions])))
    
    # Apply filters
    filtered = all_transactions.copy()
    
    if filter_type != "All":
        filtered = [t for t in filtered if t.get("type") == filter_type.lower()]
    
    if filter_category != "All":
        filtered = [t for t in filtered if t.get("category") == filter_category]
    
    if filter_timeframe == "This Month":
        filtered = [t for t in filtered if t.get("date", "") >= month_start]
    elif filter_timeframe == "Last 30 Days":
        cutoff = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        filtered = [t for t in filtered if t.get("date", "") >= cutoff]
    elif filter_timeframe == "Last 90 Days":
        cutoff = (date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
        filtered = [t for t in filtered if t.get("date", "") >= cutoff]
    
    # Display transactions
    if filtered:
        # Sort by date descending
        sorted_trans = sorted(filtered, key=lambda x: x.get("date", ""), reverse=True)
        
        for trans in sorted_trans[:20]:  # Show last 20
            col_a, col_b, col_c, col_d = st.columns([1, 2, 1, 1])
            
            with col_a:
                st.markdown(f"**{trans.get('date')}**")
            
            with col_b:
                icon = "💵" if trans.get("type") == "income" else "💸"
                st.markdown(f"{icon} {trans.get('description', 'No description')}")
                st.caption(f"{trans.get('category')}")
            
            with col_c:
                amount = trans.get('amount', 0)
                color = "green" if trans.get("type") == "income" else "red"
                st.markdown(f":{color}[${amount:,.2f}]")
            
            with col_d:
                if st.button("🗑️", key=f"del_trans_{trans.doc_id}"):
                    finance_db.remove(trans.doc_id)
                    st.rerun()
    else:
        st.info("No transactions found. Add your first transaction above!")


with tab2:
    st.markdown("### 📊 Budget Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Set Monthly Budget")
        
        budget_amount = st.number_input(
            "Total Monthly Budget ($)",
            min_value=0.0,
            value=float(get_setting("monthly_budget", 3000)),
            step=100.0
        )
        
        if st.button("Save Budget"):
            set_setting("monthly_budget", budget_amount)
            st.success("Budget saved!")
        
        st.markdown("---")
        
        # Category budgets
        st.markdown("#### Category Budgets")
        
        categories = ["Food & Dining", "Transportation", "Shopping", "Bills & Utilities",
                     "Healthcare", "Entertainment", "Business Expense", "Other"]
        
        category_budgets = {}
        for cat in categories:
            budget = st.number_input(
                f"{cat} ($)",
                min_value=0.0,
                value=float(get_setting(f"budget_{cat}", 0)),
                step=50.0,
                key=f"budget_{cat}"
            )
            category_budgets[cat] = budget
        
        if st.button("Save Category Budgets"):
            for cat, amount in category_budgets.items():
                set_setting(f"budget_{cat}", amount)
            st.success("Category budgets saved!")
    
    with col2:
        st.markdown("#### This Month's Budget Status")
        
        month_start = date.today().replace(day=1).strftime("%Y-%m-%d")
        this_month = [t for t in finance_db.get_all() if t.get("date", "") >= month_start and t.get("type") == "expense"]
        
        total_spent = sum([t.get("amount", 0) for t in this_month])
        
        budget = float(get_setting("monthly_budget", 3000))
        remaining = budget - total_spent
        percentage = (total_spent / budget * 100) if budget > 0 else 0
        
        st.metric("Total Budget", f"${budget:,.2f}")
        st.metric("Spent", f"${total_spent:,.2f}")
        st.metric("Remaining", f"${remaining:,.2f}")
        
        st.progress(min(percentage / 100, 1.0))
        
        if percentage > 100:
            st.error("⚠️ Over budget!")
        elif percentage > 80:
            st.warning("⚠️ Approaching budget limit")
        else:
            st.success("✅ Within budget")
        
        st.markdown("---")
        
        # Category breakdown
        st.markdown("#### Spending by Category")
        
        category_spending = {}
        for trans in this_month:
            cat = trans.get("category", "Other")
            category_spending[cat] = category_spending.get(cat, 0) + trans.get("amount", 0)
        
        if category_spending:
            df = pd.DataFrame(list(category_spending.items()), columns=["Category", "Spent"])
            df = df.sort_values("Spent", ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)


with tab3:
    st.markdown("### 🔥 Startup Burn Rate Calculator")
    
    st.info("💡 Burn rate is how fast you're spending money. Critical for startups!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Current Metrics")
        
        runway_months = st.number_input("Runway (months)", min_value=0, value=int(get_setting("runway_months", 12)))
        
        cash_on_hand = st.number_input(
            "Cash on hand ($)",
            min_value=0.0,
            value=float(get_setting("cash_on_hand", 50000)),
            step=1000.0
        )
        
        monthly_revenue = st.number_input(
            "Monthly Revenue ($)",
            min_value=0.0,
            value=float(get_setting("monthly_revenue", 0)),
            step=100.0
        )
        
        monthly_expenses = st.number_input(
            "Monthly Expenses ($)",
            min_value=0.0,
            value=float(get_setting("monthly_expenses", 5000)),
            step=100.0
        )
        
        if st.button("Save Metrics"):
            set_setting("runway_months", runway_months)
            set_setting("cash_on_hand", cash_on_hand)
            set_setting("monthly_revenue", monthly_revenue)
            set_setting("monthly_expenses", monthly_expenses)
            st.success("Metrics saved!")
    
    with col2:
        st.markdown("#### 📊 Analysis")
        
        # Calculate burn rate
        net_burn = monthly_expenses - monthly_revenue
        
        st.metric("💸 Net Burn Rate", f"${net_burn:,.2f}/month")
        st.metric("💵 Monthly Revenue", f"${monthly_revenue:,.2f}")
        st.metric("📉 Monthly Expenses", f"${monthly_expenses:,.2f}")
        
        # Calculate runway
        if net_burn > 0:
            calculated_runway = cash_on_hand / net_burn
            st.metric("⏱️ Runway", f"{calculated_runway:.1f} months")
            
            if calculated_runway < 3:
                st.error("🚨 Critical: Less than 3 months runway!")
            elif calculated_runway < 6:
                st.warning("⚠️ Warning: Less than 6 months runway")
            else:
                st.success("✅ Healthy runway")
        else:
            st.success("🎉 Profitable! (Revenue > Expenses)")
        
        st.markdown("---")
        
        # Projections
        st.markdown("#### 📈 6-Month Projection")
        
        projection_data = []
        current_cash = cash_on_hand
        
        for month in range(6):
            current_cash -= net_burn
            projection_data.append({
                "Month": f"Month {month + 1}",
                "Cash": max(current_cash, 0)
            })
        
        df_proj = pd.DataFrame(projection_data)
        st.line_chart(df_proj.set_index("Month"))
        
        if projection_data[-1]["Cash"] <= 0:
            st.error("⚠️ Projected to run out of cash!")


with tab4:
    st.markdown("### 📈 Financial Analytics")
    
    time_range = st.selectbox("Time range", ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "All Time"])
    
    # Calculate cutoff date
    if time_range == "Last 30 Days":
        cutoff = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    elif time_range == "Last 90 Days":
        cutoff = (date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
    elif time_range == "Last 6 Months":
        cutoff = (date.today() - timedelta(days=180)).strftime("%Y-%m-%d")
    elif time_range == "Last Year":
        cutoff = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    else:
        cutoff = "2000-01-01"
    
    all_trans = finance_db.search(Q.date >= cutoff)
    
    if all_trans:
        # Income vs Expenses over time
        st.markdown("#### 💰 Income vs Expenses")
        
        # Group by month
        monthly_data = {}
        for trans in all_trans:
            month = trans.get("date", "")[:7]  # YYYY-MM
            if month not in monthly_data:
                monthly_data[month] = {"income": 0, "expense": 0}
            
            amount = trans.get("amount", 0)
            if trans.get("type") == "income":
                monthly_data[month]["income"] += amount
            else:
                monthly_data[month]["expense"] += amount
        
        df_monthly = pd.DataFrame([
            {"Month": month, "Income": data["income"], "Expenses": data["expense"]}
            for month, data in sorted(monthly_data.items())
        ])
        
        st.line_chart(df_monthly.set_index("Month"))
        
        # Summary stats
        total_income = sum([t.get("amount", 0) for t in all_trans if t.get("type") == "income"])
        total_expenses = sum([t.get("amount", 0) for t in all_trans if t.get("type") == "expense"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Income", f"${total_income:,.2f}")
        
        with col2:
            st.metric("Total Expenses", f"${total_expenses:,.2f}")
        
        with col3:
            st.metric("Net", f"${total_income - total_expenses:,.2f}")
        
        st.markdown("---")
        
        # Spending by category
        st.markdown("#### 📊 Spending Breakdown")
        
        category_data = {}
        for trans in all_trans:
            if trans.get("type") == "expense":
                cat = trans.get("category", "Other")
                category_data[cat] = category_data.get(cat, 0) + trans.get("amount", 0)
        
        if category_data:
            df_cat = pd.DataFrame(list(category_data.items()), columns=["Category", "Amount"])
            df_cat = df_cat.sort_values("Amount", ascending=False)
            
            st.bar_chart(df_cat.set_index("Category"))
        
        st.markdown("---")
        
        # Income sources
        st.markdown("#### 💵 Income Sources")
        
        income_data = {}
        for trans in all_trans:
            if trans.get("type") == "income":
                cat = trans.get("category", "Other")
                income_data[cat] = income_data.get(cat, 0) + trans.get("amount", 0)
        
        if income_data:
            df_income = pd.DataFrame(list(income_data.items()), columns=["Source", "Amount"])
            df_income = df_income.sort_values("Amount", ascending=False)
            
            st.dataframe(df_income, use_container_width=True, hide_index=True)
    else:
        st.info("No financial data yet. Start tracking your transactions!")


st.markdown("---")
st.caption("💡 Tip: Track every transaction to get accurate insights into your financial health!")
