import asyncio
import importlib
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from bot import app
from config import API_HASH, API_ID, TOKENS

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

log = logging.getLogger("Bot")

if __name__ == "__main__":
    if (
        not API_ID
        or not API_HASH
        or not TOKENS
        or not isinstance(TOKENS, list)
        or len(TOKENS) == 0
    ):
        log.error(
            "❌ Invalid configuration! Please ensure 'API_ID', 'API_HASH', and 'TOKENS' are correctly set in 'config.py'."
        )
        sys.exit(1)

    app.load_plugins()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.start())
