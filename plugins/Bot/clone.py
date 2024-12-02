import asyncio
import re

from telethon import TelegramClient, events

from bot import app


def is_token(event):
    if not event.is_private:
        return False
    match = re.findall(r"\d{9,10}:[A-Za-z0-9_-]{35}", event.text)
    if match:
        return True
    return False


@app.on(events.NewMessage(func=is_token))
async def clone_bot(event):
    match = re.findall(r"\d{9,10}:[A-Za-z0-9_-]{35}", event.text)
    if match:
        msg = await event.reply("Wait...")
    else:
        return
    for token in match:
        if token in app.tokens:
            await msg.reply(f"Looks like on this token {token} already a bot running")
            continue
        client = TelegramClient(f"bot_{token[:10]}", app.api_id, app.api_hash)
        try:
            await client.start(bot_token=token)
            await app._add_available_handlers(client)
            app.clients.append(client)
            app.tokens.append(token)
            await msg.edit(f"Your bot is live as @{(await client.get_me()).username}")
        except Exception as e:
            err_name = type(e).__name__
            await msg.edit(f"**{err_name}**: {str(e)}")
            await asyncio.sleep(2)
