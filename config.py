"""
Wiki Club SATI Bot - Configuration
"""
import os

# ============================================
# BOT CONFIGURATION
# ============================================

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable is not set!")

# Timezone for scheduler
TIMEZONE = os.environ.get("TZ", "Asia/Kolkata")

# ============================================
# CLUB BRANDING
# ============================================

CLUB_NAME = "Wiki Club SATI"
CLUB_TAGLINE = "Promoting Open Knowledge 📚"
CLUB_COLLEGE = "Samrat Ashok Technological Institute, Vidisha"

# Social Links
LINKS = {
    "meta_page": "https://meta.wikimedia.org/wiki/Wiki_Club_SATI",
    "wikipedia": "https://www.wikipedia.org/",
    "hindi_wikipedia": "https://hi.wikipedia.org/",
    "commons": "https://commons.wikimedia.org/",
    "instagram": "https://instagram.com/wikiclubsati",
}

# ============================================
# FILE PATHS
# ============================================

import pathlib

BASE_DIR = pathlib.Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

EVENTS_FILE = DATA_DIR / "events.json"
RESOURCES_FILE = DATA_DIR / "resources.json"
TIPS_FILE = DATA_DIR / "tips.json"
FACTS_FILE = DATA_DIR / "facts.json"
USERS_FILE = DATA_DIR / "users.json"
LOGO_FILE = ASSETS_DIR / "logo.png"
