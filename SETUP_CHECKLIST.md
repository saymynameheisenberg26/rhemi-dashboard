# 🚀 First-Time Setup Checklist

Follow these steps to get your Personal Dashboard up and running!

## ☑️ Pre-Installation

- [ ] Python 3.8+ installed
- [ ] pip installed
- [ ] Terminal/command prompt access
- [ ] Text editor ready (VS Code, Sublime, etc.)

## ☑️ Installation Steps

### 1. Dependencies
- [ ] Run `./setup.sh` (Linux/Mac) or manually install
- [ ] Verify no errors in installation
- [ ] Virtual environment created (`venv/` folder exists)

### 2. Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Open `.env` in text editor

### 3. Password Setup
- [ ] Run `python generate_password.py`
- [ ] Choose a strong password
- [ ] Copy the generated hash
- [ ] Paste hash into `.env` as `PASSWORD_HASH=...`

### 4. OpenAI API (or skip for local LLM)
- [ ] Get API key from https://platform.openai.com/
- [ ] Paste into `.env` as `OPENAI_API_KEY=sk-...`
- [ ] OR set up local LLM and configure endpoint

### 5. Test Installation
- [ ] Run `python seed_data.py` to add sample data
- [ ] Run `streamlit run app.py`
- [ ] App opens in browser at http://localhost:8501
- [ ] Login with your password
- [ ] See sample data in dashboard

## ☑️ First Use

### Explore the App
- [ ] Navigate through all 7 sections using sidebar
- [ ] Check Daily Dashboard features
- [ ] View sample tasks on Kanban board
- [ ] Read sample journal entries
- [ ] Check habit tracker
- [ ] View analytics graphs
- [ ] Browse sample notes
- [ ] Generate a weekly report

### Start Using Your Own Data
- [ ] (Optional) Clear sample data: Delete files in `data/`
- [ ] Write your first journal entry
- [ ] Add your first real task
- [ ] Create your first habit
- [ ] Set today's 3 priorities
- [ ] Track your mood/energy/stress

### Try AI Features
- [ ] Generate a daily summary
- [ ] Get task suggestions
- [ ] Analyze a journal entry
- [ ] Auto-categorize a note
- [ ] Generate weekly insights

## ☑️ Personalization

- [ ] Adjust theme colors in `.streamlit/config.toml`
- [ ] Add your project tags to tasks
- [ ] Create your personal habit list
- [ ] Set up your note categories
- [ ] Customize daily priorities

## ☑️ Best Practices Setup

### Daily Routine
- [ ] Bookmark http://localhost:8501
- [ ] Set reminder to open dashboard each morning
- [ ] Plan time for evening journal entry
- [ ] Schedule habit tracking time

### Data Management
- [ ] Create backup folder: `mkdir backups/`
- [ ] Set calendar reminder for weekly backup
- [ ] Test backup: `cp -r data/ backups/backup_test/`
- [ ] Test restore: `cp -r backups/backup_test/* data/`

### Security
- [ ] Verify `.env` is in `.gitignore`
- [ ] Keep API keys secure
- [ ] Use strong password
- [ ] Don't expose app to internet

## ☑️ Optional Enhancements

- [ ] Set up cron job for auto-backup (Linux/Mac)
- [ ] Create desktop shortcut to run app
- [ ] Configure local LLM for offline AI
- [ ] Customize AI prompts in `utils/ai.py`
- [ ] Add your own metrics/trackers

## 🎯 Next Steps

Once setup is complete:

1. **Week 1**: Use daily, get familiar with features
2. **Week 2**: Review your first weekly report
3. **Week 3**: Analyze patterns in analytics
4. **Week 4**: Generate first monthly report
5. **Ongoing**: Iterate on your personal system

## ❓ Having Issues?

### Installation Problems
1. Check Python version: `python --version`
2. Try reinstalling: `pip install -r requirements.txt --force-reinstall`
3. Check error messages carefully
4. See INSTALLATION.md for detailed help

### Login Problems
1. Verify `.env` exists and has `PASSWORD_HASH`
2. Regenerate hash with `python generate_password.py`
3. Ensure no extra spaces in `.env`
4. Check terminal for error messages

### AI Not Working
1. Verify API key in `.env`
2. Check OpenAI account has credits
3. Test with smaller requests first
4. Consider using local LLM instead

### Data Issues
1. Check `data/` folder exists
2. Verify JSON files are valid
3. Try re-running `seed_data.py`
4. Check file permissions

## 📚 Documentation

- **README.md** - Project overview
- **INSTALLATION.md** - Detailed install guide
- **FEATURES.md** - Complete feature list
- **QUICK_REFERENCE.md** - Commands and tips

## ✅ You're All Set!

When all boxes are checked, you're ready to:
- Track your daily life
- Manage your startup tasks
- Journal with AI insights
- Build lasting habits
- Analyze your progress
- Generate meaningful reports

**Welcome to your Personal Dashboard! 🎉**

---

*Remember: This is YOUR system. Customize it to fit YOUR workflow!*
