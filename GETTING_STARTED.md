# 🚀 Getting Started in 5 Minutes

The absolute quickest way to get your dashboard running!

## Step 1: Install (1 minute)

```bash
cd /home/rhemi/rhemi-dashborad
pip install -r requirements.txt
```

## Step 2: Set Password (1 minute)

```bash
python generate_password.py
# Enter a password when prompted
# Copy the hash that appears
```

## Step 3: Configure (1 minute)

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

Paste your password hash and add your OpenAI API key:
```
PASSWORD_HASH=pbkdf2_sha256$29000$...paste_your_hash_here...
OPENAI_API_KEY=sk-...your_key_here...
```

Save and exit.

## Step 4: Add Sample Data (30 seconds)

```bash
python seed_data.py
```

## Step 5: Run! (30 seconds)

```bash
streamlit run app.py
```

**That's it!** 🎉

The app will open in your browser at `http://localhost:8501`

Login with the password you chose in Step 2.

---

## What to Do Next?

### Explore Sample Data (5 minutes)
1. Click through all 7 pages in the sidebar
2. See sample tasks, journals, habits, and notes
3. Try clicking "Generate AI Summary" buttons
4. Check out the Analytics and Reports pages

### Start Using Your Own Data (10 minutes)
1. Go to Daily Dashboard
2. Write your first journal entry
3. Set today's 3 priorities
4. Rate your mood/energy/stress
5. Add a real task in Tasks page
6. Create your first habit

### Customize (optional)
1. Edit `.streamlit/config.toml` to change colors
2. Clear sample data: `rm data/*.json`
3. Add your own project tags
4. Set up your habits

---

## Quick Commands

| Command | What it does |
|---------|-------------|
| `streamlit run app.py` | Start the app |
| `python seed_data.py` | Add sample data |
| `python generate_password.py` | Create new password hash |
| `cp -r data/ backup/` | Backup your data |

---

## Troubleshooting

**Can't install packages?**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**OpenAI API not working?**
- Skip AI features for now, or
- Set up local LLM instead

**Forgot your password?**
```bash
python generate_password.py
# Update .env with new hash
```

---

## 📚 More Info

- **INSTALLATION.md** - Detailed setup guide
- **FEATURES.md** - All features explained  
- **QUICK_REFERENCE.md** - Commands and tips
- **README.md** - Full documentation

---

**Enjoy your Personal Dashboard! 🎯**

*Built for managing your daily life and startup in one place.*
