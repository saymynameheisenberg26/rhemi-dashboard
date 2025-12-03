# Streamlit Cloud Deployment Guide

## 🚀 How to Deploy to Streamlit Cloud

### Step 1: Deploy Your App

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select:
   - **Repository:** `saymynameheisenberg26/rhemi-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click "Deploy"

### Step 2: Add Environment Variables (.env)

Since `.env` files are not pushed to GitHub (for security), you need to add your environment variables in Streamlit Cloud:

#### Option 1: Using Streamlit Secrets (Recommended)

1. In Streamlit Cloud, go to your app settings (⚙️)
2. Click on "Secrets" in the left sidebar
3. Add your secrets in TOML format:

```toml
# Streamlit secrets.toml format
PASSWORD_HASH = "$pbkdf2-sha256$29000$UKpVKmUMAQDgfM.ZUyolZA$mIUj/33UMpiPme5Md69dJ/Cmokl2RQuwXVym0hlNQVw"

# Optional: Add OpenAI API key if you want AI features
OPENAI_API_KEY = "your_openai_api_key_here"
```

4. Click "Save"
5. Your app will automatically restart with the new secrets

#### Option 2: Update Your Code to Use Streamlit Secrets

The current code uses `os.getenv()` which works locally with `.env` files. For Streamlit Cloud compatibility, the code will need a small update to check both `.env` and Streamlit secrets.

### Step 3: Generate Your Own Password Hash

**For security, you should generate your own password hash!**

Run locally:
```bash
source venv/bin/activate
python3 -c "from passlib.hash import pbkdf2_sha256; print(pbkdf2_sha256.hash('YOUR_SECURE_PASSWORD'))"
```

Copy the output and use it in Streamlit secrets.

### Current Setup

- **Current password:** `your_password`
- **Current hash:** `$pbkdf2-sha256$29000$UKpVKmUMAQDgfM.ZUyolZA$mIUj/33UMpiPme5Md69dJ/Cmokl2RQuwXVym0hlNQVw`

⚠️ **Change this for production!**

### Troubleshooting

**If your app fails to load:**
1. Check the logs in Streamlit Cloud
2. Make sure all secrets are properly formatted (TOML syntax)
3. Ensure PASSWORD_HASH is in quotes
4. The hash should NOT have line breaks

**If you get authentication errors:**
1. Verify the PASSWORD_HASH in secrets matches your hash exactly
2. Make sure there are no extra spaces or quotes around the hash
3. Try regenerating your password hash

### Local Testing

To test locally before deploying:

```bash
cd /home/rhemi/rhemi-dashborad
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Login with: `your_password` (or whatever password you generated a hash for)

---

## 📝 Quick Reference

### Streamlit Secrets Format (copy this to Streamlit Cloud):

```toml
PASSWORD_HASH = "$pbkdf2-sha256$29000$UKpVKmUMAQDgfM.ZUyolZA$mIUj/33UMpiPme5Md69dJ/Cmokl2RQuwXVym0hlNQVw"
OPENAI_API_KEY = "sk-your-key-here"  # Optional
```

### Local .env Format (already created):

```bash
PASSWORD_HASH=$pbkdf2-sha256$29000$UKpVKmUMAQDgfM.ZUyolZA$mIUj/33UMpiPme5Md69dJ/Cmokl2RQuwXVym0hlNQVw
OPENAI_API_KEY=your_openai_api_key_here
```

---

🎉 Your dashboard will be live at: `https://your-app-name.streamlit.app`
