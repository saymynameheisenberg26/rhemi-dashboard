# Quick Reference Guide

## Common Commands

```bash
# First time setup
./setup.sh

# Generate password hash
python generate_password.py

# Seed sample data
python seed_data.py

# Run the app
streamlit run app.py

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## Keyboard Shortcuts (in Streamlit)

- `Ctrl + R` - Rerun the app
- `Ctrl + K` - Open command palette
- `Tab` - Navigate between form fields
- `Enter` - Submit forms

## Data File Locations

All data is stored in the `data/` directory:

```
data/
├── tasks.json      # Your tasks and projects
├── journal.json    # Journal entries
├── habits.json     # Habits and tracking data
├── notes.json      # Notes and ideas
└── settings.json   # App settings
```

## Quick Tips

### Daily Workflow
1. Login to Daily Dashboard
2. Set 3 priorities for the day
3. Track mood/energy/stress
4. Write quick journal entry
5. Check tasks and move them on Kanban
6. Mark habits as done

### Weekly Review
1. Go to Reports → Weekly Report
2. Review completed tasks
3. Check habit streaks
4. Read journal summaries
5. Generate AI insights

### Monthly Planning
1. Go to Reports → Monthly Report
2. Review overall progress
3. Analyze mood trends in Analytics
4. Adjust habits based on data
5. Set new goals in Notes

## AI Features Quick Guide

### Daily Dashboard
- **Generate Daily Summary** - Overview of your day
- **Get Task Suggestions** - What to focus on next

### Journal
- **Analyze Entry** - Emotional tone & themes
- **Extract Goals** - Pull out action items
- **Generate Summary** - Summarize multiple entries

### Tasks
- **AI Task Suggestions** - Prioritization help

### Notes
- **Auto-categorize** - Let AI categorize your notes

### Analytics
- **Generate Insights** - Correlation patterns

### Reports
- **Weekly/Monthly Summaries** - Comprehensive AI analysis

## Troubleshooting

### Can't login?
- Check `.env` has correct `PASSWORD_HASH`
- Regenerate hash with `python generate_password.py`

### AI not working?
- Verify `OPENAI_API_KEY` in `.env`
- Check you have API credits
- Or set `USE_LOCAL_LLM=true` for local model

### Data disappeared?
- Check `data/` folder exists
- Look for backup folders
- Re-run `python seed_data.py` for sample data

### App won't start?
- Activate virtual environment first
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

## Backup & Restore

### Backup
```bash
# Simple copy
cp -r data/ data_backup_$(date +%Y%m%d)/

# Compressed backup
tar -czf backup_$(date +%Y%m%d).tar.gz data/
```

### Restore
```bash
# From copy
cp -r data_backup_20231203/* data/

# From compressed
tar -xzf backup_20231203.tar.gz
```

## Customization

### Change Theme Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#3b82f6"      # Main accent color
backgroundColor = "#ffffff"    # Page background
secondaryBackgroundColor = "#f3f4f6"  # Sidebar/cards
textColor = "#1f2937"         # Text color
```

### Modify AI Prompts
Edit functions in `utils/ai.py` to customize AI responses.

### Add Custom Categories
Modify the category lists in:
- `pages/5_Notes.py` - Note categories
- `pages/1_Tasks.py` - Task tags

## Performance Tips

- Keep completed tasks archive reasonable (delete old ones)
- Limit journal entries in memory (filter by date range)
- Clear old habit entries if too many (>365 days)
- Keep notes organized with tags

## Security Best Practices

1. Never commit `.env` to git
2. Backup `data/` regularly
3. Use a strong password
4. Don't expose to public internet
5. Keep API keys secure
6. Update dependencies periodically

## Common Workflows

### Morning Routine
```
1. Open Daily Dashboard
2. Set 3 priorities
3. Rate mood/energy/stress
4. Quick journal: "What I'm grateful for"
5. Review today's tasks
6. Mark meditation habit complete
```

### End of Day
```
1. Update task statuses
2. Write journal entry
3. Mark completed habits
4. Generate daily AI summary
5. Plan tomorrow's priorities
```

### Weekly Review
```
1. Go to Reports → Weekly
2. Review metrics
3. Generate AI summary
4. Check Analytics for patterns
5. Adjust next week's goals
```

### Monthly Review
```
1. Go to Reports → Monthly
2. Export data (backup)
3. Review all analytics
4. Generate AI insights
5. Set next month's intentions
6. Clean up old tasks/notes
```

---

**Need more help?** Check INSTALLATION.md and README.md
