# 🚀 Deployment Guide: Schedula Bot on Render (Free Web Service)

This guide walks you through deploying your Telegram bot to run **24/7 for free** on Render using the "Web Service" trick.

---

## 📋 Prerequisites

1. ✅ GitHub account
2. ✅ Render account: https://render.com
3. ✅ Bot Token from @BotFather

---

## ☁️ Step 1: Deploy on Render

### 1.1 Create New Web Service

1. Go to **[Render Dashboard](https://dashboard.render.com/)**.
2. Click **New +** → **Web Service**.
3. Connect your GitHub repository.

### 1.2 Configure Settings

| Setting | Value |
|---------|-------|
| **Name** | `schedula-bot` |
| **Region** | Singapore (closest to India) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |
| **Instance Type** | **Free** |

### 1.3 Add Environment Variables

Scroll down to **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | `your_bot_token_here` |
| `TZ` | `Asia/Kolkata` |
| `PYTHON_VERSION` | `3.11.4` |

4. Click **Create Web Service**.

---

## ⚡ Step 2: Keep It Alive (UptimeRobot Guide)

Render's Free Web Services "sleep" after 15 minutes of inactivity. To prevent this, use **UptimeRobot** (free) to "ping" your bot every 5 minutes.

### 2.1 Sign Up / Login
1. Go to **[uptimerobot.com](https://uptimerobot.com/)**.
2. Click **"Register for FREE"**.
3. Enter name, email, and password.
4. Verify your email (check spam folder if needed).
5. **Login** to your dashboard.

### 2.2 Create Monitor
1. Click the big green button **"+ Add New Monitor"**.
2. **Monitor Type**: Select `HTTP(s)`.
3. **Friendly Name**: `Schedula Bot` (or anything you like).
4. **URL (or IP)**: Paste your Render URL (e.g., `https://schedula-bot.onrender.com`).
   * *Find this URL at the top of your Render service page (under the name).*
5. **Monitoring Interval**: Change to `5 minutes` (Important!).
6. **Monitor Timeout**: Leave as `30 seconds`.
7. **Select "Alert Contacts To Notify"**: Check your email (optional, if you want down alerts).
8. Click **"Create Monitor"** (and "Create Monitor" again if asked).

### 2.3 Verify
- You should see your monitor listed on the left as "UP" (green) after a few minutes.
- This means UptimeRobot is visiting your bot every 5 mins, keeping it awake 24/7! 🎉

---

## ❓ Other Free Options

| Platform | Free Tier? | Pros/Cons |
|----------|------------|-----------|
| **Render** | ✅ Yes | Needs UptimeRobot trick. Best uptime. |
| **Railway** | ❌ Trial | Only $5 credit upfront, then paid. |
| **Fly.io** | ⚠️ Credit Card | Requires card for free tier. Complex setup. |
| **Oracle Cloud** | ✅ Always Free | Generous, but very hard to sign up. |
| **Glitch** | ❌ Sleepy | Sleeps after 5 mins. Good for testing only. |

**Recommendation:** stick with **Render + UptimeRobot** for the easiest free experience.
