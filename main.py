import asyncio
import re
from telethon import events, Button
from telethon import TelegramClient
import logging
from logging.handlers import RotatingFileHandler
from config import API_ID, API_HASH, TOKENS

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("telethon").setLevel(logging.ERROR)

log = logging.getLogger("Bot")

class You:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.tokens = TOKENS
        self.clients = []

    async def start(self):
        to_start = []
        for token in self.tokens:
            client = TelegramClient(f"bot_{token[:10]}", self.api_id, self.api_hash)
            self.clients.append(client)
            to_start.append(client.start(bot_token=token))
        await asyncio.gather(*to_start)
        log.info("All bots started successfully.")

    async def disconnect(self):
        log.info("Stopping all bots...")
        await asyncio.gather(*(client.disconnect() for client in self.clients))
        log.info("All bots stopped.")

    def on(self, event: events.common.EventBuilder):
        def decorator(f):
            for client in self.clients:
                client.add_event_handler(f, event)
            return f

        return decorator

    def on_msg(self, pattern, **kwargs):
        if isinstance(pattern, str):
            pattern = [pattern]

        pattern = "|".join(pattern)
        pattern = re.compile(rf"^[\/!]({pattern})(?:\s|$)", re.IGNORECASE)
        kwargs['pattern'] = pattern

        def decorator(func):
            for client in self.clients:
                client.add_event_handler(func, events.NewMessage(**kwargs))
            return func

        return decorator

app = You()

async def main():
    if not API_ID:
        log.error("❌ Missing 'API_ID' in the configuration! Please set it in the 'config.py' file.")
        sys.exit(1)
    if not API_HASH:
        log.error("❌ Missing 'API_HASH' in the configuration! Please set it in the 'config.py' file.")
        sys.exit(1)
    if not TOKENS or not isinstance(TOKENS, list) or len(TOKENS) == 0:
        log.error("❌ Missing or invalid 'TOKENS'! Please ensure it is a list of bot tokens in the 'config.py' file.")
        sys.exit(1)
    await app.start()

@app.on(events.CallbackQuery(pattern=r"home"))
@app.on_msg(pattern="start", func=lambda e: e.is_private)
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
    button = [
        [Button.inline("how to set me up! 💛", data=b"setup")]
    ]
    if event.data:
        await event.edit(message.format(user=mention, me=me_mention), buttons=button)
    else:
        await event.respond(message.format(user=mention, me=me_mention), buttons=button)

@app.on(events.CallbackQuery(pattern=r"setup"))
async def setup(event):
    txt = "Due to Telegram restrictions, one bot can give one reaction to your post. Below are some bots. Add these to your channel [make sure to promote them as admins but without any rights. If you don't promote them, they will still work]:\n"
    for client in app.clients:
        txt += f"@{(await client.get_me()).username}\n"
    button = [
        [Button.inline("Back", data="home")]
    ]
    await event.edit(txt, buttons=button)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    #loop.run_forever()
    import time
    while True:
        time.sleep(300)
