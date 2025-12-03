"""
Seed sample data for testing the dashboard
Run this script to populate the database with sample data
"""
from datetime import datetime, date, timedelta
from utils.db import (tasks_db, journal_db, habits_db, notes_db, settings_db,
                      health_db, finance_db, contacts_db, gratitude_db, goals_db, events_db)
import random


def clear_all_data():
    """Clear all existing data."""
    print("🗑️  Clearing existing data...")
    tasks_db.clear()
    journal_db.clear()
    habits_db.clear()
    notes_db.clear()
    settings_db.clear()
    health_db.clear()
    finance_db.clear()
    contacts_db.clear()
    gratitude_db.clear()
    goals_db.clear()
    events_db.clear()
    print("✅ Data cleared!")


def seed_tasks():
    """Seed sample tasks."""
    print("📝 Seeding tasks...")
    
    sample_tasks = [
        {
            "title": "Build MVP for product",
            "description": "Create the minimum viable product for our SaaS platform",
            "status": "doing",
            "priority": "high",
            "deadline": (date.today() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "tags": ["Tech", "Product"],
            "created_at": (datetime.now() - timedelta(days=10)).isoformat(),
            "date": (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")
        },
        {
            "title": "Write blog post about our journey",
            "description": "Share our startup story on Medium",
            "status": "todo",
            "priority": "medium",
            "deadline": (date.today() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "tags": ["Marketing", "Content"],
            "created_at": (datetime.now() - timedelta(days=5)).isoformat(),
            "date": (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")
        },
        {
            "title": "Research competitor pricing",
            "description": "Analyze pricing strategies of top 5 competitors",
            "status": "done",
            "priority": "medium",
            "deadline": None,
            "tags": ["Research", "Marketing"],
            "created_at": (datetime.now() - timedelta(days=8)).isoformat(),
            "completed_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "date": (date.today() - timedelta(days=8)).strftime("%Y-%m-%d")
        },
        {
            "title": "Schedule investor meetings",
            "description": "Set up calls with potential investors",
            "status": "todo",
            "priority": "high",
            "deadline": (date.today() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "tags": ["Fundraising"],
            "created_at": (datetime.now() - timedelta(days=3)).isoformat(),
            "date": (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
        },
        {
            "title": "Update financial projections",
            "description": "Revise Q4 financial forecast",
            "status": "done",
            "priority": "high",
            "deadline": None,
            "tags": ["Finance"],
            "created_at": (datetime.now() - timedelta(days=15)).isoformat(),
            "completed_at": (datetime.now() - timedelta(days=5)).isoformat(),
            "date": (date.today() - timedelta(days=15)).strftime("%Y-%m-%d")
        },
        {
            "title": "Learn React hooks",
            "description": "Complete tutorial on advanced React hooks",
            "status": "todo",
            "priority": "low",
            "deadline": None,
            "tags": ["Learning", "Tech"],
            "created_at": (datetime.now() - timedelta(days=20)).isoformat(),
            "date": (date.today() - timedelta(days=20)).strftime("%Y-%m-%d")
        },
        {
            "title": "Customer interview - User #5",
            "description": "Interview potential customer about pain points",
            "status": "done",
            "priority": "high",
            "deadline": None,
            "tags": ["Product", "Research"],
            "created_at": (datetime.now() - timedelta(days=7)).isoformat(),
            "completed_at": (datetime.now() - timedelta(days=3)).isoformat(),
            "date": (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        },
        {
            "title": "Fix authentication bug",
            "description": "Users reporting login issues on mobile",
            "status": "doing",
            "priority": "high",
            "deadline": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "tags": ["Tech", "Bug"],
            "created_at": datetime.now().isoformat(),
            "date": date.today().strftime("%Y-%m-%d")
        }
    ]
    
    for task in sample_tasks:
        tasks_db.insert(task)
    
    print(f"✅ Seeded {len(sample_tasks)} tasks!")


def seed_journal():
    """Seed sample journal entries."""
    print("📔 Seeding journal entries...")
    
    sample_entries = [
        {
            "date": (date.today() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "content": "Had a great productive day! Finished the MVP mockups and got positive feedback from the team. Feeling energized about the progress we're making. Need to remember to take breaks though - worked 10 hours straight.",
            "mood": 8,
            "energy": 7,
            "stress": 4,
            "updated_at": (datetime.now() - timedelta(days=7)).isoformat()
        },
        {
            "date": (date.today() - timedelta(days=6)).strftime("%Y-%m-%d"),
            "content": "Tough day. Investor call didn't go as planned. They had concerns about our go-to-market strategy. Spent the evening rethinking our approach. Sometimes setbacks lead to better solutions.",
            "mood": 5,
            "energy": 4,
            "stress": 8,
            "updated_at": (datetime.now() - timedelta(days=6)).isoformat()
        },
        {
            "date": (date.today() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "content": "Better today. Had a brainstorming session with the team and came up with a revised strategy. Also did a 30-minute workout in the morning which helped clear my head. Definitely need to make exercise a daily habit.",
            "mood": 7,
            "energy": 6,
            "stress": 5,
            "updated_at": (datetime.now() - timedelta(days=5)).isoformat()
        },
        {
            "date": (date.today() - timedelta(days=4)).strftime("%Y-%m-%d"),
            "content": "Amazing customer interview today! User loved our prototype and gave incredible insights. This is why we're building this product. Moments like these make all the hard work worth it.",
            "mood": 9,
            "energy": 8,
            "stress": 3,
            "updated_at": (datetime.now() - timedelta(days=4)).isoformat()
        },
        {
            "date": (date.today() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "content": "Spent most of the day coding. Fixed several bugs and implemented the new authentication flow. Need to work on better time management - got lost in code and skipped lunch.",
            "mood": 6,
            "energy": 5,
            "stress": 6,
            "updated_at": (datetime.now() - timedelta(days=3)).isoformat()
        },
        {
            "date": (date.today() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "content": "Friday feels! Wrapped up the week strong. Completed the competitor analysis and learned a lot about pricing psychology. Took the evening off to recharge with friends. Work-life balance is crucial.",
            "mood": 8,
            "energy": 7,
            "stress": 3,
            "updated_at": (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            "date": (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "content": "Weekend reflection: Grateful for the progress we've made this month. Sometimes I get caught up in what's not done yet and forget to celebrate small wins. Need to practice more gratitude.",
            "mood": 7,
            "energy": 6,
            "stress": 4,
            "updated_at": (datetime.now() - timedelta(days=1)).isoformat()
        },
        {
            "date": date.today().strftime("%Y-%m-%d"),
            "content": "New week, fresh start! Set three clear priorities for today. Morning meditation helped me feel centered. Ready to tackle that investor pitch deck.",
            "mood": 7,
            "energy": 7,
            "stress": 5,
            "updated_at": datetime.now().isoformat()
        }
    ]
    
    for entry in sample_entries:
        journal_db.insert(entry)
    
    print(f"✅ Seeded {len(sample_entries)} journal entries!")


def seed_habits():
    """Seed sample habits."""
    print("🎯 Seeding habits...")
    
    # Create habits
    habit_1 = habits_db.insert({
        "name": "Morning meditation",
        "frequency": "daily",
        "target": 1,
        "active": True,
        "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
        "entries": []
    })
    
    habit_2 = habits_db.insert({
        "name": "Exercise",
        "frequency": "weekly",
        "target": 3,
        "active": True,
        "created_at": (datetime.now() - timedelta(days=25)).isoformat(),
        "entries": []
    })
    
    habit_3 = habits_db.insert({
        "name": "Read for 30 minutes",
        "frequency": "daily",
        "target": 1,
        "active": True,
        "created_at": (datetime.now() - timedelta(days=20)).isoformat(),
        "entries": []
    })
    
    habit_4 = habits_db.insert({
        "name": "Code review",
        "frequency": "weekly",
        "target": 5,
        "active": True,
        "created_at": (datetime.now() - timedelta(days=15)).isoformat(),
        "entries": []
    })
    
    # Add entries for meditation (high consistency)
    meditation_entries = []
    for i in range(25):
        entry_date = (date.today() - timedelta(days=i)).strftime("%Y-%m-%d")
        completed = random.random() > 0.2  # 80% completion rate
        meditation_entries.append({"date": entry_date, "completed": completed})
    
    habits_db.update({"entries": meditation_entries}, habit_1)
    
    # Add entries for exercise (moderate consistency)
    exercise_entries = []
    for i in range(25):
        entry_date = (date.today() - timedelta(days=i)).strftime("%Y-%m-%d")
        completed = random.random() > 0.6  # 40% completion rate
        exercise_entries.append({"date": entry_date, "completed": completed})
    
    habits_db.update({"entries": exercise_entries}, habit_2)
    
    # Add entries for reading (good consistency)
    reading_entries = []
    for i in range(20):
        entry_date = (date.today() - timedelta(days=i)).strftime("%Y-%m-%d")
        completed = random.random() > 0.35  # 65% completion rate
        reading_entries.append({"date": entry_date, "completed": completed})
    
    habits_db.update({"entries": reading_entries}, habit_3)
    
    # Add entries for code review (work week only)
    code_review_entries = []
    for i in range(15):
        entry_date = (date.today() - timedelta(days=i))
        # Only weekdays
        if entry_date.weekday() < 5:
            completed = random.random() > 0.3  # 70% completion rate on weekdays
            code_review_entries.append({"date": entry_date.strftime("%Y-%m-%d"), "completed": completed})
    
    habits_db.update({"entries": code_review_entries}, habit_4)
    
    print("✅ Seeded 4 habits with entries!")


def seed_notes():
    """Seed sample notes."""
    print("💡 Seeding notes...")
    
    sample_notes = [
        {
            "title": "Product idea: AI-powered task manager",
            "content": "What if we built a task manager that uses AI to predict which tasks you'll actually complete based on your history? Could auto-schedule tasks at optimal times based on your energy patterns.",
            "category": "Idea",
            "tags": ["product", "AI", "productivity"],
            "created_at": (datetime.now() - timedelta(days=12)).isoformat()
        },
        {
            "title": "Meeting notes - Investor call",
            "content": "Key takeaways from call with Sarah:\n- She's interested but wants to see traction\n- Suggested focusing on B2B first\n- Intro to 2 potential customers\n- Follow up in 2 weeks with metrics",
            "category": "Work",
            "tags": ["fundraising", "meetings"],
            "created_at": (datetime.now() - timedelta(days=8)).isoformat()
        },
        {
            "title": "Book notes: The Lean Startup",
            "content": "Key concepts:\n- Build-Measure-Learn loop\n- MVP is about learning, not features\n- Validated learning > vanity metrics\n- Pivot or persevere decisions\n\nNeed to apply this to our product development process.",
            "category": "Learning",
            "tags": ["books", "startup", "methodology"],
            "created_at": (datetime.now() - timedelta(days=15)).isoformat()
        },
        {
            "title": "Personal reflection on work-life balance",
            "content": "Been thinking about burnout lately. Working 12-hour days isn't sustainable. Need to:\n- Set clear work hours\n- Exercise daily\n- Spend quality time with family\n- Say no to non-essential meetings\n\nSuccess means nothing if I'm miserable.",
            "category": "Personal",
            "tags": ["reflection", "health", "balance"],
            "created_at": (datetime.now() - timedelta(days=5)).isoformat()
        },
        {
            "title": "Technical debt to address",
            "content": "TODO list for code cleanup:\n1. Refactor authentication module\n2. Add proper error handling to API\n3. Write tests for payment flow\n4. Update dependencies\n5. Document API endpoints",
            "category": "Todo",
            "tags": ["tech", "coding", "maintenance"],
            "created_at": (datetime.now() - timedelta(days=3)).isoformat()
        },
        {
            "title": "Marketing channel ideas",
            "content": "Channels to explore:\n- Product Hunt launch\n- Indie Hackers community\n- LinkedIn content\n- Guest posts on relevant blogs\n- YouTube tutorials\n- Twitter presence\n\nFocus on content that provides value first.",
            "category": "Idea",
            "tags": ["marketing", "growth", "channels"],
            "created_at": (datetime.now() - timedelta(days=10)).isoformat()
        },
        {
            "title": "Lessons from failed experiment",
            "content": "Tried cold outreach last week - 0% response rate. Learned:\n- Generic messages don't work\n- Need to provide value upfront\n- Warm intros are 10x more effective\n- Better to focus on content marketing\n\nPivoting to inbound strategy instead.",
            "category": "Learning",
            "tags": ["marketing", "experiments", "lessons"],
            "created_at": (datetime.now() - timedelta(days=4)).isoformat()
        }
    ]
    
    for note in sample_notes:
        notes_db.insert(note)
    
    print(f"✅ Seeded {len(sample_notes)} notes!")


def seed_settings():
    """Seed sample settings."""
    print("⚙️  Seeding settings...")
    
    today_str = date.today().strftime("%Y-%m-%d")
    
    settings_db.insert({
        "key": f"priorities_{today_str}",
        "value": [
            "Finish investor pitch deck",
            "Fix authentication bug",
            "Review customer feedback"
        ]
    })
    
    settings_db.insert({
        "key": "theme",
        "value": "light"
    })
    
    print("✅ Seeded settings!")


def seed_health():
    """Seed sample health data."""
    print("🏃 Seeding health data...")
    
    for i in range(14):
        day = date.today() - timedelta(days=i)
        
        health_db.insert({
            "date": day.isoformat(),
            "sleep_hours": random.uniform(5.5, 8.5),
            "sleep_quality": random.randint(6, 10),
            "water_glasses": random.randint(4, 10),
            "exercise_minutes": random.randint(0, 90),
            "exercise_type": random.choice(["Running", "Gym", "Yoga", "Walking", "Swimming"]),
            "meal_quality": random.randint(5, 10),
            "stress_level": random.randint(2, 8),
            "anxiety_level": random.randint(1, 7),
            "meditation_minutes": random.randint(0, 30),
            "notes": random.choice([
                "Felt energized after workout",
                "Need more sleep",
                "Great day overall",
                "Feeling stressed about deadlines",
                ""
            ]),
            "created_at": (datetime.now() - timedelta(days=i)).isoformat()
        })
    
    print("✅ Seeded health data!")


def seed_finance():
    """Seed sample financial data."""
    print("💰 Seeding finance data...")
    
    # Income
    finance_db.insert({
        "date": (date.today() - timedelta(days=5)).isoformat(),
        "type": "income",
        "category": "Revenue",
        "amount": 5000,
        "description": "First customer payment",
        "created_at": (datetime.now() - timedelta(days=5)).isoformat()
    })
    
    # Expenses
    expense_categories = ["Server Costs", "Marketing", "Software", "Office", "Salary", "Misc"]
    
    for i in range(20):
        day = date.today() - timedelta(days=random.randint(0, 30))
        
        finance_db.insert({
            "date": day.isoformat(),
            "type": "expense",
            "category": random.choice(expense_categories),
            "amount": random.randint(50, 1000),
            "description": random.choice([
                "AWS hosting",
                "Facebook ads",
                "Figma subscription",
                "Coworking space",
                "Contractor payment",
                "Office supplies"
            ]),
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        })
    
    # Budgets
    finance_db.insert({
        "type": "budget",
        "category": "Marketing",
        "monthly_limit": 2000,
        "created_at": datetime.now().isoformat()
    })
    
    finance_db.insert({
        "type": "budget",
        "category": "Server Costs",
        "monthly_limit": 500,
        "created_at": datetime.now().isoformat()
    })
    
    print("✅ Seeded finance data!")


def seed_contacts():
    """Seed sample contacts."""
    print("👥 Seeding contacts...")
    
    sample_contacts = [
        {
            "name": "Sarah Johnson",
            "email": "sarah@techventures.com",
            "phone": "+1-555-0101",
            "company": "Tech Ventures",
            "role": "Investor",
            "category": "Investors",
            "relationship_quality": 9,
            "last_contact": (date.today() - timedelta(days=3)).isoformat(),
            "next_followup": (date.today() + timedelta(days=7)).isoformat(),
            "notes": "Very interested in our product. Follow up next week.",
            "created_at": (datetime.now() - timedelta(days=30)).isoformat()
        },
        {
            "name": "Mike Chen",
            "email": "mike@designco.com",
            "phone": "+1-555-0102",
            "company": "DesignCo",
            "role": "Designer",
            "category": "Partners",
            "relationship_quality": 8,
            "last_contact": (date.today() - timedelta(days=10)).isoformat(),
            "next_followup": (date.today() + timedelta(days=14)).isoformat(),
            "notes": "Potential design partner for UI overhaul",
            "created_at": (datetime.now() - timedelta(days=45)).isoformat()
        },
        {
            "name": "Lisa Anderson",
            "email": "lisa@startup.io",
            "phone": "+1-555-0103",
            "company": "Startup.io",
            "role": "Founder",
            "category": "Mentors",
            "relationship_quality": 10,
            "last_contact": (date.today() - timedelta(days=1)).isoformat(),
            "next_followup": (date.today() + timedelta(days=30)).isoformat(),
            "notes": "Amazing mentor. Monthly check-ins.",
            "created_at": (datetime.now() - timedelta(days=90)).isoformat()
        },
        {
            "name": "James Martinez",
            "email": "james@bigcorp.com",
            "phone": "+1-555-0104",
            "company": "BigCorp",
            "role": "VP Product",
            "category": "Customers",
            "relationship_quality": 7,
            "last_contact": (date.today() - timedelta(days=20)).isoformat(),
            "next_followup": (date.today() + timedelta(days=5)).isoformat(),
            "notes": "Needs follow-up on enterprise features",
            "created_at": (datetime.now() - timedelta(days=60)).isoformat()
        }
    ]
    
    for contact in sample_contacts:
        contacts_db.insert(contact)
    
    print("✅ Seeded contacts!")


def seed_gratitude():
    """Seed sample gratitude entries."""
    print("🙏 Seeding gratitude data...")
    
    for i in range(7):
        day = date.today() - timedelta(days=i)
        
        gratitude_db.insert({
            "date": day.isoformat(),
            "gratitude_items": random.sample([
                "My supportive co-founder",
                "Good health",
                "Our first paying customer",
                "Coffee",
                "Beautiful weather today",
                "Progress on the product",
                "Supportive family"
            ], 3),
            "wins": random.choice([
                "Closed our first deal!",
                "Fixed a critical bug",
                "Great feedback from users",
                "Productive team meeting",
                "Finished the pitch deck"
            ]),
            "lessons": random.choice([
                "Need to communicate better with team",
                "Technical debt adds up quickly",
                "Customer feedback is invaluable",
                "Taking breaks improves productivity",
                "Focus on one thing at a time"
            ]),
            "challenges": random.choice([
                "Managing work-life balance",
                "Dealing with technical issues",
                "Finding the right market fit",
                "Hiring challenges",
                "Competing priorities"
            ]),
            "tomorrow_intention": random.choice([
                "Ship the new feature",
                "Reach out to 5 potential customers",
                "Review and refactor code",
                "Plan next sprint",
                "Focus on strategic planning"
            ]),
            "happiness": random.randint(6, 10),
            "satisfaction": random.randint(5, 10),
            "created_at": (datetime.now() - timedelta(days=i)).isoformat()
        })
    
    print("✅ Seeded gratitude data!")


def seed_goals():
    """Seed sample goals."""
    print("🎯 Seeding goals...")
    
    sample_goals = [
        {
            "title": "Reach $10K MRR",
            "description": "Achieve $10,000 in monthly recurring revenue",
            "type": "Long-term Goal",
            "category": "Business",
            "priority": "high",
            "progress": 35,
            "deadline": (date.today() + timedelta(days=180)).isoformat(),
            "created_at": (datetime.now() - timedelta(days=60)).isoformat()
        },
        {
            "title": "Launch Beta Version",
            "description": "Ship beta version to 50 early adopters",
            "type": "Quarterly OKR",
            "category": "Product",
            "priority": "high",
            "progress": 70,
            "key_results": [
                {"result": "Get 50 beta signups", "completed": True},
                {"result": "Ship core features", "completed": True},
                {"result": "Collect feedback from 30 users", "completed": False}
            ],
            "deadline": (date.today() + timedelta(days=45)).isoformat(),
            "created_at": (datetime.now() - timedelta(days=45)).isoformat()
        },
        {
            "title": "Improve Onboarding Flow",
            "description": "Reduce time-to-value for new users",
            "type": "Monthly Goal",
            "category": "Product",
            "priority": "medium",
            "progress": 40,
            "deadline": (date.today() + timedelta(days=20)).isoformat(),
            "created_at": (datetime.now() - timedelta(days=10)).isoformat()
        },
        {
            "title": "Raise Seed Round",
            "description": "Secure $500K seed funding",
            "type": "Milestone",
            "category": "Fundraising",
            "priority": "high",
            "progress": 20,
            "milestones": [
                {"milestone": "Create pitch deck", "completed": True},
                {"milestone": "Identify 20 target investors", "completed": True},
                {"milestone": "Get 10 investor meetings", "completed": False},
                {"milestone": "Receive term sheet", "completed": False}
            ],
            "deadline": (date.today() + timedelta(days=90)).isoformat(),
            "created_at": (datetime.now() - timedelta(days=30)).isoformat()
        }
    ]
    
    for goal in sample_goals:
        goals_db.insert(goal)
    
    print("✅ Seeded goals!")


def seed_events():
    """Seed sample calendar events."""
    print("📅 Seeding events...")
    
    sample_events = [
        {
            "title": "Investor Meeting",
            "date": (date.today() + timedelta(days=3)).isoformat(),
            "time": "14:00:00",
            "type": "Meeting",
            "priority": "high",
            "description": "Pitch meeting with Sarah from Tech Ventures",
            "reminder": True,
            "created_at": datetime.now().isoformat()
        },
        {
            "title": "Product Demo",
            "date": (date.today() + timedelta(days=5)).isoformat(),
            "time": "10:00:00",
            "type": "Meeting",
            "priority": "high",
            "description": "Demo for potential enterprise customer",
            "reminder": True,
            "created_at": datetime.now().isoformat()
        },
        {
            "title": "Team Standup",
            "date": date.today().isoformat(),
            "time": "09:00:00",
            "type": "Meeting",
            "priority": "medium",
            "description": "Daily team sync",
            "reminder": False,
            "created_at": datetime.now().isoformat()
        },
        {
            "title": "Submit Tax Documents",
            "date": (date.today() + timedelta(days=10)).isoformat(),
            "time": "17:00:00",
            "type": "Deadline",
            "priority": "high",
            "description": "Quarterly tax filing deadline",
            "reminder": True,
            "created_at": datetime.now().isoformat()
        }
    ]
    
    for event in sample_events:
        events_db.insert(event)
    
    print("✅ Seeded events!")


def main():
    """Main function to seed all data."""
    print("\n🌱 Starting to seed sample data...\n")
    
    clear_all_data()
    print()
    
    seed_tasks()
    seed_journal()
    seed_habits()
    seed_notes()
    seed_settings()
    seed_health()
    seed_finance()
    seed_contacts()
    seed_gratitude()
    seed_goals()
    seed_events()
    
    print("\n🎉 All sample data seeded successfully!")
    print("\nYou can now run the app with: streamlit run app.py\n")


if __name__ == "__main__":
    main()
