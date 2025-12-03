# Installation Guide

This guide will walk you through setting up your Personal Dashboard.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- An OpenAI API key (or local LLM setup)

## Step-by-Step Installation

### 1. Install Dependencies

Using the setup script (Linux/Mac):
```bash
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

Create your `.env` file:
```bash
cp .env.example .env
```

### 3. Generate Password Hash

Run the password generator:
```bash
python generate_password.py
```

Or use this command:
```bash
python -c "from passlib.hash import pbkdf2_sha256; print(pbkdf2_sha256.hash('your_password'))"
```

Copy the output hash.

### 4. Edit .env File

Open `.env` and add:

```bash
# Your password hash from step 3
PASSWORD_HASH=pbkdf2_sha256$29000$...your_hash_here...

# Your OpenAI API key
OPENAI_API_KEY=sk-...your_key_here...
```

To get an OpenAI API key:
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key

### 5. (Optional) Seed Sample Data

To test the app with sample data:
```bash
python seed_data.py
```

This will create:
- Sample tasks across different statuses
- Journal entries for the last week
- Active habits with tracking history
- Notes and ideas
- Sample settings

### 6. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 7. Login

Use the password you set in step 3 to login.

## Troubleshooting

### Import Errors

If you see import errors, make sure you've activated your virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### OpenAI API Errors

If you see AI-related errors:
1. Check that your API key is correct in `.env`
2. Ensure you have API credits available
3. You can use the app without AI features - just skip the AI buttons

### Permission Errors

If you can't run `setup.sh`:
```bash
chmod +x setup.sh
```

### Data Directory

The `data/` folder will be created automatically on first run. All your data is stored there as JSON files:
- `tasks.json` - Your tasks
- `journal.json` - Journal entries
- `habits.json` - Habits and tracking
- `notes.json` - Notes and ideas
- `settings.json` - App settings

## Using Local LLM Instead of OpenAI

If you prefer to use a local LLM:

1. Set up a local LLM server (e.g., Ollama, LocalAI, etc.)
2. Edit `.env`:
```bash
USE_LOCAL_LLM=true
LOCAL_LLM_ENDPOINT=http://localhost:8000/v1
```

## Backup Your Data

Your data is stored in the `data/` folder. To backup:
```bash
# Create a backup
cp -r data/ data_backup_$(date +%Y%m%d)/

# Or compress it
tar -czf dashboard_backup_$(date +%Y%m%d).tar.gz data/
```

## Updating

To update dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## Need Help?

Check the README.md for more information about features and usage.
