import os
import importlib
import asyncio
import logging
import sys
from telethon import events, Button
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from logging.handlers import RotatingFileHandler
from config import API_ID, API_HASH, TOKENS

from bot import app


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


@app.on(events.NewMessage(pattern="^/start", func=lambda e: e.is_private))
@app.on(events.CallbackQuery(pattern=r"home"))
async def start(event):
    message = """Hello {user} 👋,
I am an {me} 🤖. I can give reactions to posts in your channel! 🎉

To learn how to use me or how to set me up, click the button below for my usage instructions 📜👇.
    """
    sender = await event.get_sender()
    me = await event.client.get_me()
    user_name = f"{sender.first_name} {sender.last_name or ''}".strip()
    me_mention = f"[{me.first_name}](tg://user?id={me.id})"
    mention = f"[{user_name}](tg://user?id={sender.id})"
    button = [[Button.inline("How to set me up! 💛", data=b"setup")]]

    if isinstance(event, events.CallbackQuery.Event):
        await event.edit(message.format(user=mention, me=me_mention), buttons=button)
    elif isinstance(event, events.NewMessage.Event):
        await event.respond(message.format(user=mention, me=me_mention), buttons=button)


@app.on(events.CallbackQuery(pattern=r"setup"))
async def setup(event):
    txt = "Due to Telegram restrictions, one bot can give one reaction to your post. Below are some bots. Add these to your channel [make sure to promote them as admins but without any rights. If you don't promote them, they will still work]:\n"
    for client in app.clients:
        txt += f"@{(await client.get_me()).username}\n"
    button = [[Button.inline("Back", data=b"home")]]
    await event.edit(txt, buttons=button)


@app.on(events.NewMessage(func=lambda e: isinstance(e.from_id, PeerChannel)))
async def handle_channel_messages(event):
    log.info(f"Received a message in a channel: {event.message.message}")


if __name__ == "__main__":
    if not API_ID or not API_HASH or not TOKENS or not isinstance(TOKENS, list) or len(TOKENS) == 0:
        log.error("❌ Invalid configuration! Please ensure 'API_ID', 'API_HASH', and 'TOKENS' are correctly set in 'config.py'.")
        sys.exit(1)

    for root, _, files in os.walk("plugins"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                module_path = os.path.join(root, file).replace(os.sep, ".").removesuffix(".py")
                importlib.import_module(module_path)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.start())
