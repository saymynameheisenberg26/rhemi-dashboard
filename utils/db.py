"""Database utilities using TinyDB for local JSON storage."""
import os
from datetime import datetime, date
from tinydb import TinyDB, Query
from pathlib import Path
import json


# Ensure data directory exists
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


class Database:
    """Simple database wrapper for TinyDB."""
    
    def __init__(self, name):
        self.db = TinyDB(DATA_DIR / f"{name}.json", indent=2)
    
    def insert(self, data):
        """Insert a document."""
        return self.db.insert(data)
    
    def get_all(self):
        """Get all documents."""
        return self.db.all()
    
    def update(self, data, doc_id):
        """Update a document by ID."""
        return self.db.update(data, doc_ids=[doc_id])
    
    def remove(self, doc_id):
        """Remove a document by ID."""
        return self.db.remove(doc_ids=[doc_id])
    
    def search(self, query):
        """Search documents."""
        return self.db.search(query)
    
    def clear(self):
        """Clear all documents."""
        return self.db.truncate()


# Database instances
tasks_db = Database("tasks")
journal_db = Database("journal")
habits_db = Database("habits")
notes_db = Database("notes")
settings_db = Database("settings")
health_db = Database("health")
finance_db = Database("finance")
contacts_db = Database("contacts")
gratitude_db = Database("gratitude")
goals_db = Database("goals")
events_db = Database("events")


def get_setting(key, default=None):
    """Get a setting value."""
    Q = Query()
    result = settings_db.search(Q.key == key)
    if result:
        return result[0].get("value", default)
    return default


def set_setting(key, value):
    """Set a setting value."""
    Q = Query()
    existing = settings_db.search(Q.key == key)
    if existing:
        settings_db.update({"value": value}, existing[0].doc_id)
    else:
        settings_db.insert({"key": key, "value": value})


def get_journal_entry(entry_date):
    """Get journal entry for a specific date."""
    Q = Query()
    date_str = entry_date.strftime("%Y-%m-%d") if isinstance(entry_date, date) else entry_date
    result = journal_db.search(Q.date == date_str)
    return result[0] if result else None


def save_journal_entry(entry_date, content, mood=None, energy=None, stress=None):
    """Save or update a journal entry."""
    Q = Query()
    date_str = entry_date.strftime("%Y-%m-%d") if isinstance(entry_date, date) else entry_date
    
    data = {
        "date": date_str,
        "content": content,
        "mood": mood,
        "energy": energy,
        "stress": stress,
        "updated_at": datetime.now().isoformat()
    }
    
    existing = journal_db.search(Q.date == date_str)
    if existing:
        journal_db.update(data, existing[0].doc_id)
        return existing[0].doc_id
    else:
        return journal_db.insert(data)


def get_tasks_by_status(status=None):
    """Get tasks filtered by status."""
    if status:
        Q = Query()
        return tasks_db.search(Q.status == status)
    return tasks_db.get_all()


def get_tasks_for_date(target_date):
    """Get tasks for a specific date."""
    Q = Query()
    date_str = target_date.strftime("%Y-%m-%d") if isinstance(target_date, date) else target_date
    return tasks_db.search(Q.date == date_str)


def get_habits_active():
    """Get all active habits."""
    Q = Query()
    return habits_db.search(Q.active == True)


def get_habit_entries(habit_id, start_date=None, end_date=None):
    """Get habit entries for a specific habit."""
    # Habit entries are stored within the habit document
    habit = habits_db.get(doc_id=habit_id)
    if not habit:
        return []
    
    entries = habit.get("entries", [])
    
    if start_date or end_date:
        filtered = []
        for entry in entries:
            entry_date = datetime.fromisoformat(entry["date"]).date()
            if start_date and entry_date < start_date:
                continue
            if end_date and entry_date > end_date:
                continue
            filtered.append(entry)
        return filtered
    
    return entries


def add_habit_entry(habit_id, entry_date, completed=True):
    """Add or update a habit entry."""
    habit = habits_db.get(doc_id=habit_id)
    if not habit:
        return False
    
    date_str = entry_date.strftime("%Y-%m-%d") if isinstance(entry_date, date) else entry_date
    entries = habit.get("entries", [])
    
    # Check if entry already exists
    for i, entry in enumerate(entries):
        if entry["date"] == date_str:
            entries[i]["completed"] = completed
            habits_db.update({"entries": entries}, habit_id)
            return True
    
    # Add new entry
    entries.append({
        "date": date_str,
        "completed": completed
    })
    habits_db.update({"entries": entries}, habit_id)
    return True
