from random import choice

from telethon import events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import PeerChannel, ReactionEmoji

from bot import app

reactions = [
    "👍",
    "👎",
    "❤",
    "🔥",
    "🥰",
    "👏",
    "😁",
    "🤔",
    "🤯",
    "😱",
    "🤬",
    "😢",
    "🎉",
    "🤩",
    "🤮",
    "💩",
    "🙏",
    "👌",
    "🕊",
    "🤡",
    "🥱",
    "🥴",
    "😍",
    "🐳",
    "❤‍🔥",
    "🌚",
    "🌭",
    "💯",
    "🤣",
    "⚡",
    "🍌",
    "🏆",
    "💔",
    "🤨",
    "😐",
    "🍓",
    "🍾",
    "💋",
    "🖕",
    "😈",
    "😴",
    "😭",
    "🤓",
    "👻",
    "👨‍💻",
    "👀",
    "🎃",
    "🙈",
    "😇",
    "😨",
    "🤝",
    "✍",
    "🤗",
    "🫡",
    "🎅",
    "🎄",
    "☃",
    "💅",
    "🤪",
    "🗿",
    "🆒",
    "💘",
    "🙉",
    "🦄",
    "😘",
    "💊",
    "🙊",
    "😎",
    "👾",
    "🤷‍♂",
    "🤷",
    "🤷‍♀",
    "😡",
]


@app.on(events.NewMessage(func=lambda e: isinstance(e.message.peer_id, PeerChannel)))
async def react(event):
    reaction = [ReactionEmoji(emoticon=choice(reactions))]
    await event.client(
        SendReactionRequest(
            peer=await event.get_chat(),
            msg_id=event.id,
            reaction=reaction,
        )
    )
