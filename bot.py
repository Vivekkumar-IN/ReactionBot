import asyncio
import importlib
import os

from telethon import TelegramClient, events

from config import API_HASH, API_ID, TOKENS


class Bot:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.tokens = TOKENS
        self.clients = [
            TelegramClient(f"bot_{token[:10]}", self.api_id, self.api_hash)
            for token in self.tokens
        ]
        self.handlers = []

    async def start(self):
        for client, token in zip(self.clients, self.tokens):
            await client.start(bot_token=token)
            await self._add_available_handlers(client)

            print(f"Bot {(await client.get_me()).username} started successfully.")
        print("All bots started successfully.")

        tasks = [client.run_until_disconnected() for client in self.clients]
        await asyncio.gather(*tasks)

    async def _add_available_handlers(self, client):
        for func, event in self.handlers:
            client.add_event_handler(func, event)

    async def disconnect(self):
        print("Stopping all bots...")
        await asyncio.gather(*(client.disconnect() for client in self.clients))
        print("All bots stopped.")

    def on(self, event: events.common.EventBuilder):
        def decorator(f):
            self.handlers.append((f, event))
            return f

        return decorator

    def load_plugins():
        plugins = {}
        for root, _, files in os.walk("plugins"):
            category = os.path.basename(root)
            plugins[category] = {}
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    module_path = (
                        os.path.join(root, file)
                        .replace(os.sep, ".")
                        .removesuffix(".py")
                    )
                    module = importlib.import_module(module_path)
                    plugins[category][file[:-3]] = module
        return plugins


app = Bot()
