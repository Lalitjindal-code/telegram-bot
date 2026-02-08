"""
🌐 Wiki Club SATI Bot
A Telegram bot for Wiki Club SATI - Promoting Open Knowledge

Features:
- Personal reminders
- Club events listing
- Wiki editing resources
- Random tips & facts
- Quick Wikimedia links
"""

import os
import json
import random
import logging
from datetime import datetime, timedelta
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Import configuration
from config import (
    BOT_TOKEN, TIMEZONE, CLUB_NAME, CLUB_TAGLINE, CLUB_COLLEGE, LINKS,
    EVENTS_FILE, RESOURCES_FILE, TIPS_FILE, FACTS_FILE, USERS_FILE, LOGO_FILE
)

# ============================================
# LOGGING SETUP
# ============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# SCHEDULER SETUP
# ============================================

scheduler = AsyncIOScheduler(timezone=TIMEZONE)

# ============================================
# DATA LOADING HELPERS
# ============================================

def load_json(file_path):
    """Load data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON: {file_path}")
        return []


def save_json(file_path, data):
    """Save data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save JSON: {e}")


# ============================================
# USER TRACKING
# ============================================

def is_new_user(user_id: int) -> bool:
    """Check if user is new (first time using bot)"""
    users = load_json(USERS_FILE)
    if not isinstance(users, dict):
        users = {"users": []}
    return str(user_id) not in [str(u.get('id')) for u in users.get('users', [])]


def register_user(user) -> bool:
    """Register a new user, returns True if new user"""
    users = load_json(USERS_FILE)
    if not isinstance(users, dict):
        users = {"users": []}
    
    user_ids = [str(u.get('id')) for u in users.get('users', [])]
    
    if str(user.id) not in user_ids:
        users['users'].append({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'joined_at': datetime.now().isoformat()
        })
        save_json(USERS_FILE, users)
        logger.info(f"🆕 New user registered: {user.id} ({user.username})")
        return True
    return False


# ============================================
# REMINDER FUNCTIONS
# ============================================

async def send_reminder(bot, chat_id, message):
    """Send scheduled reminder"""
    try:
        await bot.send_message(
            chat_id=chat_id, 
            text=f"⏰ *Reminder from Wiki Club SATI*\n\n{message}",
            parse_mode="Markdown"
        )
        logger.info(f"✅ Reminder sent to {chat_id}")
    except Exception as e:
        logger.error(f"❌ Failed to send reminder: {e}")


# ============================================
# COMMAND HANDLERS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Welcome message with logo"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    # Check if this is a new user and send special welcome
    is_new = register_user(user)
    
    if is_new:
        # Special first-time welcome message
        first_time_msg = f"""
� *Welcome aboard, {user.first_name}!*

You're the newest member of our Wiki community! 🌟

━━━━━━━━━━━━━━━━━━━━━━
✨ *What is Wiki Club SATI?*
━━━━━━━━━━━━━━━━━━━━━━

We are students from *{CLUB_COLLEGE}* who believe knowledge should be *FREE* for everyone!

🌐 We edit Wikipedia
📷 We upload photos to Wikimedia Commons  
🎓 We organize workshops & photowalks
💡 We promote digital literacy

━━━━━━━━━━━━━━━━━━━━━━
🚀 *Your Wiki Journey Starts Here!*
━━━━━━━━━━━━━━━━━━━━━━

I'll help you:
• 📅 Stay updated on club events
• ⏰ Set personal reminders
• 📚 Learn wiki editing
• 💡 Get daily tips & fun facts

_Let's make knowledge accessible to everyone!_ 🌍
"""
        
        # Send first-time welcome with logo
        if LOGO_FILE.exists():
            try:
                with open(LOGO_FILE, 'rb') as logo:
                    await update.message.reply_photo(
                        photo=logo,
                        caption=first_time_msg,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logger.error(f"Failed to send logo: {e}")
                await update.message.reply_text(first_time_msg, parse_mode="Markdown")
        else:
            await update.message.reply_text(first_time_msg, parse_mode="Markdown")
        
        # Send quick start guide after
        await update.message.reply_text(
            "📌 *Quick Start Commands:*\n\n"
            "• /events - See what's happening\n"
            "• /tip - Get a wiki editing tip\n"
            "• /fact - Learn a fun wiki fact\n"
            "• /help - All commands\n\n"
            "_Try /tip now to get started!_ 💡",
            parse_mode="Markdown"
        )
        return
    
    # Regular welcome for returning users
    welcome_text = f"""
🌐 *Welcome back to {CLUB_NAME}!*
_{CLUB_TAGLINE}_

Hello {user.first_name}! 👋

Good to see you again!

📌 *What can I do for you?*

• /remind `HH:MM message` - Set reminders
• /events - Upcoming club events
• /resources - Learning materials
• /tip - Get wiki editing tips
• /fact - Random Wikipedia fact
• /links - Quick Wikimedia links
• /about - About our club
• /help - All commands

_Keep contributing to open knowledge!_ 🚀
"""
    
    # Send logo first if exists
    if LOGO_FILE.exists():
        try:
            with open(LOGO_FILE, 'rb') as logo:
                await update.message.reply_photo(
                    photo=logo,
                    caption=welcome_text,
                    parse_mode="Markdown"
                )
                return
        except Exception as e:
            logger.error(f"Failed to send logo: {e}")
    
    # Fallback to text only
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = f"""
📚 *{CLUB_NAME} Bot - Commands*

*🔔 Reminders*
/remind `HH:MM message` - Set a reminder
  _Example: /remind 14:30 Submit wiki article_

*📅 Club Info*
/events - View upcoming events
/about - About Wiki Club SATI
/links - Quick Wikimedia links

*📖 Learn & Explore*
/resources - Wiki editing tutorials
/tip - Random editing tip
/fact - Fun Wikipedia fact

*🆘 Help*
/start - Restart the bot
/help - Show this message

⏰ _Timezone: {TIMEZONE}_
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /remind command - Set personal reminders"""
    try:
        if len(context.args) < 2:
            raise ValueError("Not enough arguments")
        
        time_str = context.args[0]
        message = " ".join(context.args[1:])
        
        hour, minute = map(int, time_str.split(":"))
        
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Invalid time")
        
        run_time = datetime.now().replace(
            hour=hour, minute=minute, second=0, microsecond=0
        )
        
        if run_time < datetime.now():
            run_time += timedelta(days=1)
        
        job = scheduler.add_job(
            send_reminder,
            'date',
            run_date=run_time,
            args=[context.bot, update.message.chat_id, message]
        )
        
        logger.info(f"Job {job.id} scheduled for {run_time}")
        
        await update.message.reply_text(
            f"✅ *Reminder Set!*\n\n"
            f"📅 *Time:* {run_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"📝 *Message:* {message}\n\n"
            f"_I'll remind you when it's time!_",
            parse_mode="Markdown"
        )
    
    except (ValueError, IndexError):
        await update.message.reply_text(
            "❌ *Invalid format!*\n\n"
            "*Usage:* `/remind HH:MM message`\n"
            "*Example:* `/remind 14:30 Submit wiki article`",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error scheduling: {e}")
        await update.message.reply_text("❌ Something went wrong. Please try again.")


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /events command - Show upcoming events"""
    events_data = load_json(EVENTS_FILE)
    
    if not events_data:
        await update.message.reply_text(
            "📅 *Upcoming Events*\n\n"
            "_No events scheduled yet. Stay tuned!_",
            parse_mode="Markdown"
        )
        return
    
    # Filter future events and sort by date
    today = datetime.now().strftime("%Y-%m-%d")
    future_events = [e for e in events_data if e.get("date", "") >= today]
    future_events.sort(key=lambda x: x.get("date", ""))
    
    if not future_events:
        await update.message.reply_text(
            "📅 *Upcoming Events*\n\n"
            "_No upcoming events. Check back later!_",
            parse_mode="Markdown"
        )
        return
    
    text = "📅 *Upcoming Wiki Club SATI Events*\n\n"
    
    for event in future_events[:5]:  # Show max 5 events
        text += f"*{event.get('title', 'Event')}*\n"
        text += f"📆 {event.get('date', 'TBD')} at {event.get('time', 'TBD')}\n"
        text += f"📍 {event.get('venue', 'TBD')}\n"
        if event.get('description'):
            text += f"_{event['description']}_\n"
        text += "\n"
    
    text += "_Set a reminder with /remind to not miss out!_"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resources command - Show learning resources"""
    resources_data = load_json(RESOURCES_FILE)
    
    if not resources_data:
        await update.message.reply_text(
            "📚 *Learning Resources*\n\n"
            "_No resources available yet._",
            parse_mode="Markdown"
        )
        return
    
    text = "📚 *Wiki Editing Resources*\n\n"
    
    for resource in resources_data:
        text += f"*{resource.get('title', 'Resource')}*\n"
        text += f"🔗 {resource.get('url', '')}\n"
        if resource.get('description'):
            text += f"_{resource['description']}_\n"
        text += "\n"
    
    text += "_Happy learning! 📖_"
    
    await update.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=True)


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tip command - Random wiki editing tip"""
    tips_data = load_json(TIPS_FILE)
    
    if not tips_data:
        await update.message.reply_text(
            "💡 *Wiki Tip*\n\n"
            "_No tips available yet._",
            parse_mode="Markdown"
        )
        return
    
    random_tip = random.choice(tips_data)
    
    await update.message.reply_text(
        f"💡 *Wiki Editing Tip*\n\n"
        f"{random_tip}\n\n"
        f"_Type /tip for another tip!_",
        parse_mode="Markdown"
    )


async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /fact command - Random Wikipedia fact"""
    facts_data = load_json(FACTS_FILE)
    
    if not facts_data:
        await update.message.reply_text(
            "🌐 *Wiki Fact*\n\n"
            "_No facts available yet._",
            parse_mode="Markdown"
        )
        return
    
    random_fact = random.choice(facts_data)
    
    await update.message.reply_text(
        f"🌐 *Did You Know?*\n\n"
        f"{random_fact}\n\n"
        f"_Type /fact for another fact!_",
        parse_mode="Markdown"
    )


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /links command - Quick Wikimedia links"""
    text = f"""
🔗 *Quick Wikimedia Links*

🌐 *Wikipedia (English)*
{LINKS.get('wikipedia', '')}

🇮🇳 *Wikipedia (Hindi)*
{LINKS.get('hindi_wikipedia', '')}

📷 *Wikimedia Commons*
{LINKS.get('commons', '')}

📋 *Wiki Club SATI Meta Page*
{LINKS.get('meta_page', '')}

📸 *Follow us on Instagram*
{LINKS.get('instagram', '')}

_Start exploring and contributing!_ 🚀
"""
    await update.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=True)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command - About the club"""
    about_text = f"""
📖 *About {CLUB_NAME}*

🏛️ *{CLUB_COLLEGE}*
🌐 Part of the global Wikimedia Movement

*Our Mission:*
Promoting open knowledge and free access to information through Wikimedia projects.

*What We Do:*
• 📝 Wikipedia editing & contributions
• 📷 Wikimedia Commons uploads
• 🖥️ MediaWiki training workshops
• 📸 Cultural photowalks
• 🎓 Student outreach campaigns
• 🎉 Edit-a-thons & competitions

*Skills You'll Gain:*
✓ Research & writing
✓ Digital citizenship
✓ Design thinking
✓ Leadership
✓ Collaboration

*Join Us:*
Open to all SATI students!
Contact any club member or attend our next event.

🔗 {LINKS.get('meta_page', '')}

_{CLUB_TAGLINE}_
"""
    
    # Send with logo if exists
    if LOGO_FILE.exists():
        try:
            with open(LOGO_FILE, 'rb') as logo:
                await update.message.reply_photo(
                    photo=logo,
                    caption=about_text,
                    parse_mode="Markdown"
                )
                return
        except Exception as e:
            logger.error(f"Failed to send logo: {e}")
    
    await update.message.reply_text(about_text, parse_mode="Markdown", disable_web_page_preview=True)


# ============================================
# APPLICATION LIFECYCLE
# ============================================

async def post_init(application):
    """Start scheduler after event loop is running"""
    scheduler.start()
    logger.info("📅 Scheduler started!")


async def post_shutdown(application):
    """Graceful shutdown"""
    scheduler.shutdown()
    logger.info("📅 Scheduler stopped!")


# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to run the bot"""
    logger.info(f"🚀 Starting {CLUB_NAME} Bot...")
    
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )
    
    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("events", events))
    app.add_handler(CommandHandler("resources", resources))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("fact", fact))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("about", about))
    
    logger.info("🤖 Bot is running...")
    
    # Run with polling
    app.run_polling(
        allowed_updates=["message"],
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
