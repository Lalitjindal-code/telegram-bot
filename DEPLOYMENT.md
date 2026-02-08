# 🚀 Deployment Guide: Telegram Bot on Render (Free Tier)

This guide walks you through deploying your Telegram bot to run **24/7 for free** on Render.

---

## 📋 Prerequisites

1. ✅ Working bot code (tested locally)
2. ✅ GitHub account
3. ✅ Render account (free): https://render.com
4. ✅ Bot Token from [@BotFather](https://t.me/BotFather)

---

## 🔧 Step 1: Prepare Your Code

### 1.1 Project Structure
Your project should look like this:
```
telegram-bot/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── .gitignore          # Files to ignore
└── README.md           # Documentation
```

### 1.2 Key Code Changes (Already Done ✅)

| Change | Why |
|--------|-----|
| Use `os.environ.get("BOT_TOKEN")` | Never hardcode secrets! |
| Add logging | Debug issues on cloud |
| Add `post_shutdown` | Graceful shutdown |
| Use `drop_pending_updates=True` | Ignore old messages after restart |

---

## 📦 Step 2: Push to GitHub

### 2.1 Initialize Git Repository

Open terminal in your project folder:

```powershell
cd "c:\Users\lalit\skills\project\true\telegram bot"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Telegram reminder bot"
```

### 2.2 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `telegram-reminder-bot`
3. Keep it **Private** (has your bot token reference)
4. Click **Create repository**

### 2.3 Push to GitHub

```powershell
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/telegram-reminder-bot.git
git branch -M main
git push -u origin main
```

---

## ☁️ Step 3: Deploy on Render

### 3.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (easiest)

### 3.2 Create New Background Worker

> ⚠️ **IMPORTANT**: Use **Background Worker**, NOT Web Service!
> Telegram bots don't need HTTP endpoints.

1. Click **New +** → **Background Worker**
2. Connect your GitHub repository
3. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `telegram-reminder-bot` |
| **Region** | Singapore (closest to India) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |
| **Instance Type** | `Free` |

### 3.3 Add Environment Variables

Click **Environment** → **Add Environment Variable**:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | `8515878923:AAHzWb7fhNyebZ9-gCXIplK4lWtrhh9A2pc` |
| `TZ` | `Asia/Kolkata` |
| `PYTHON_VERSION` | `3.11.4` |

> ⚠️ **SECURITY**: Never commit your BOT_TOKEN to GitHub!

### 3.4 Deploy

1. Click **Create Background Worker**
2. Wait for build to complete (2-3 minutes)
3. Check logs to see `🤖 Bot is running...`

---

## ✅ Step 4: Verify Deployment

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Try `/schedule 14:30 Test reminder`
5. Check Render logs for confirmation

---

## 🔄 Updating Your Bot

After making code changes:

```powershell
git add .
git commit -m "Your change description"
git push
```

Render will **automatically redeploy** when you push to `main`.

---

## ⚠️ Common Mistakes & Solutions

### ❌ Mistake 1: Using Web Service instead of Background Worker
**Problem**: Web service expects HTTP requests and will sleep  
**Solution**: Use **Background Worker** for long-running bots

### ❌ Mistake 2: Hardcoding BOT_TOKEN
**Problem**: Token exposed if repo becomes public  
**Solution**: Always use `os.environ.get("BOT_TOKEN")`

### ❌ Mistake 3: Wrong Python version
**Problem**: Dependency errors during build  
**Solution**: Set `PYTHON_VERSION=3.11.4` in environment variables

### ❌ Mistake 4: Missing requirements.txt
**Problem**: `ModuleNotFoundError` on cloud  
**Solution**: Include all dependencies with versions

### ❌ Mistake 5: Using BackgroundScheduler
**Problem**: Async coroutine never awaited  
**Solution**: Use `AsyncIOScheduler` with wrapper function

### ❌ Mistake 6: Scheduler starts before event loop
**Problem**: `RuntimeError: no running event loop`  
**Solution**: Start scheduler in `post_init` callback

### ❌ Mistake 7: No logging
**Problem**: Can't debug issues on cloud  
**Solution**: Use Python's `logging` module

---

## 🆓 Free Tier Limitations (Render)

| Limit | Value |
|-------|-------|
| **Runtime** | Sleeps after 15 min of no activity |
| **RAM** | 512 MB |
| **CPU** | Shared |
| **Bandwidth** | 100 GB/month |

> **Note**: Background Workers on free tier may spin down. For truly 24/7 operation, consider:
> - Render paid tier ($7/month)
> - Railway.app (has free tier with more uptime)
> - Oracle Cloud Free Tier (always free VM)

---

## 🚀 Alternative: Railway.app

Railway offers a simpler deployment experience:

1. Go to https://railway.app
2. **New Project** → **Deploy from GitHub Repo**
3. Select your repository
4. Add environment variables (`BOT_TOKEN`, `TZ`)
5. Railway auto-detects Python and deploys!

**Pros**: Simpler, good free tier  
**Cons**: Limited free hours per month

---

## 📊 Monitoring Your Bot

### View Logs on Render
1. Go to your service dashboard
2. Click **Logs** tab
3. See real-time output

### Add Health Check (Optional)
For production bots, add a `/status` command:

```python
async def status(update, context):
    jobs = scheduler.get_jobs()
    await update.message.reply_text(
        f"✅ Bot is online!\n"
        f"📅 Scheduled jobs: {len(jobs)}"
    )
```

---

## 🎉 Done!

Your bot is now running 24/7 in the cloud. Users can set reminders anytime, and they'll receive notifications even when your PC is off.

**Need help?** Check Render logs for error messages.
