# Personal Life & Startup Dashboard

A comprehensive Streamlit dashboard for managing your daily life, startup tasks, journaling, habit tracking, and personal analytics - all running locally on your machine.

## Features

- 🔐 **Local Authentication** - Password-protected access
- 📊 **Daily Dashboard** - Quick overview of today's priorities, mood, and tasks
- ✅ **Task Manager** - Kanban board for managing startup projects
- 📝 **Personal Journal** - Daily, weekly, and monthly reflections with AI analysis
- 🎯 **Habit Tracker** - Build and maintain habits with streak tracking
- 📈 **Analytics** - Visualize your productivity, mood, and progress trends
- 💡 **Notes & Ideas** - Capture and organize your thoughts
- 📋 **Reports** - Auto-generated weekly and monthly summaries

## Installation

1. **Clone or download this project**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment:**
   ```bash
   cp .env.example .env
   ```

4. **Generate a password hash:**
   ```bash
   python -c "from passlib.hash import pbkdf2_sha256; print(pbkdf2_sha256.hash('your_password'))"
   ```
   Copy the output and paste it in `.env` as `PASSWORD_HASH`

5. **Add your OpenAI API key** to `.env` (or configure a local LLM)

6. **Seed sample data (optional):**
   ```bash
   python seed_data.py
   ```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Data Storage

All your data is stored locally in the `/data` folder:
- `tasks.json` - Your tasks and projects
- `journal.json` - Journal entries
- `habits.json` - Habit tracking data
- `notes.json` - Notes and ideas
- `settings.json` - App settings and preferences

## Project Structure

```
rhemi-dashboard/
├── app.py                  # Main app with Daily Dashboard
├── pages/                  # Streamlit pages
│   ├── 1_Tasks.py
│   ├── 2_Journal.py
│   ├── 3_Habits.py
│   ├── 4_Analytics.py
│   ├── 5_Notes.py
│   └── 6_Reports.py
├── utils/                  # Helper modules
│   ├── auth.py
│   ├── db.py
│   └── ai.py
├── data/                   # Local data storage (auto-created)
├── .env                    # Your configuration (not in git)
└── requirements.txt
```

## Security Note

This app is designed for **local personal use only**. Do not expose it to the internet without proper security measures.

## License

Personal use only.
