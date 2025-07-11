from telethon.sync import TelegramClient
from app.scraper.telegram_scraper import CHANNELS, scrape_channel
from app.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN

with TelegramClient("anon", TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
    client.start(bot_token=TELEGRAM_BOT_TOKEN)
    for channel in CHANNELS:
        scrape_channel(client, channel)
