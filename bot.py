import importlib
import asyncio
from telethon import TelegramClient
from config import API_ID, API_HASH, TOKENS




class You:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.tokens = TOKENS
        self.clients = [
            TelegramClient(f"bot_{token[:10]}", self.api_id, self.api_hash)
            for token in self.tokens
        ]

    async def start(self):
        for client, token in zip(self.clients, self.tokens):
            await client.start(bot_token=token)
            log.info(f"Bot {(await client.get_me()).username} started successfully.")
        log.info("All bots started successfully.")

        tasks = [client.run_until_disconnected() for client in self.clients]
        await asyncio.gather(*tasks)

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


app = You()
