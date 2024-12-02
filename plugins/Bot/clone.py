import re 
import asyncio
from telethon import events
from telethon import TelegramClient
from bot import app

def is_token(event):
    if event.is_private:
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
        client = TelegramClient(f"bot_{token[:10]}", app.api_id, app.api_hash)
        try:
            await client.start(bot_token=token)
            await app._add_available_handlers(client)
            app.clients.append(client)
        except Exception as e:
            err_name = type(e).__name__
            await msg.edit(f"**{err_name}**: {str(e)}")
            await asyncio.sleep(2)
        
    
