import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from loguru import logger
from app.config import TELEGRAM_API_ID, TELEGRAM_API_HASH

# Setup logging
LOG_FILE = "logs/scraper.log"
logger.add(LOG_FILE, rotation="500 KB")

# Channels to scrape
CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

# Path to save scraped data
RAW_DATA_PATH = "data/raw/telegram_messages"

# Create directory if it doesn't exist
os.makedirs(RAW_DATA_PATH, exist_ok=True)


def scrape_channel(client, channel_url):
    """Scrape messages from a public Telegram channel and save them as JSON."""
    try:
        logger.info(f"Scraping channel: {channel_url}")
        channel = client.get_entity(channel_url)

        messages_data = []
        for message in client.iter_messages(channel, limit=100):
            messages_data.append({
                "id": message.id,
                "date": str(message.date),
                "message": message.message,
                "sender_id": getattr(message.sender_id, 'user_id', None),
                "media": isinstance(message.media, MessageMediaPhoto)
            })

        # Create file path
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        channel_name = channel.username or "unknown_channel"
        file_path = os.path.join(RAW_DATA_PATH, f"{date_str}_{channel_name}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved {len(messages_data)} messages to {file_path}")

    except Exception as e:
        logger.error(f"Failed to scrape {channel_url}: {str(e)}")
