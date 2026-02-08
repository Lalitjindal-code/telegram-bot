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

## ⚡ Step 2: Keep It Alive (Important!)

Render's Free Web Services "sleep" after 15 minutes of inactivity. To prevent this, use a free monitoring service to "ping" your bot.

1. Once deployed, Render will give you a URL (e.g., `https://schedula-bot.onrender.com`).
2. Go to **[UptimeRobot](https://uptimerobot.com/)** (it's free).
3. Click **Add New Monitor**.
4. Settings:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Schedula Bot
   - **URL**: `https://schedula-bot.onrender.com` (Your Render URL)
   - **Monitoring Interval**: 5 minutes
5. Click **Create Monitor**.

✅ **Done!** UptimeRobot will ping your bot every 5 minutes, keeping it awake 24/7 for free.

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
