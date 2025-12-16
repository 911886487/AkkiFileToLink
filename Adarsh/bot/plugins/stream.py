# (c) Adarsh-Goel
import os
import asyncio
from urllib.parse import quote_plus

from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Adarsh.bot import StreamBot
from Adarsh.vars import Var
from Adarsh.utils.database import db
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.file_properties import (
    get_name,
    get_hash,
    get_media_file_size
)

# ================= CONFIG =================

MY_PASS = os.environ.get("MY_PASS", None)
pass_dict = {}

# ================= PRIVATE CHAT HANDLER =================

@StreamBot.on_message(
    filters.private & (filters.document | filters.video | filters.audio | filters.photo),
    group=4
)
async def private_receive_handler(c: Client, m: Message):

    # ---- Save user to DB ----
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"👤 New User Joined\n\n"
            f"Name: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
            f"ID: `{m.from_user.id}`",
            disable_web_page_preview=True
        )

    try:
        # ---- Forward file to bin channel ----
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        stream_link = (
            f"{Var.URL}watch/{log_msg.id}/"
            f"{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        )
        online_link = (
            f"{Var.URL}{log_msg.id}/"
            f"{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        )

        text = (
            "<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n"
            f"<b>📂 File name :</b> <i>{get_name(log_msg)}</i>\n\n"
            f"<b>📦 File size :</b> <i>{humanbytes(get_media_file_size(m))}</i>\n\n"
            f"<b>📥 Download :</b> <i>{online_link}</i>\n\n"
            f"<b>🖥 Watch :</b> <i>{stream_link}</i>\n\n"
            "<b>🚸 NOTE :</b> Link won't expire until deleted"
        )

        await log_msg.reply_text(
            text=(
                f"**Requested by:** [{m.from_user.first_name}]"
                f"(tg://user?id={m.from_user.id})\n"
                f"**User ID:** `{m.from_user.id}`\n"
                f"**Stream Link:** {stream_link}"
            ),
            disable_web_page_preview=True,
            quote=True
        )

        await m.reply_text(
            text=text,
            disable_web_page_preview=True,
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("◉ STREAM ◉", url=stream_link),
                        InlineKeyboardButton("● DOWNLOAD ●", url=online_link),
                    ]
                ]
            )
        )

    except FloodWait as e:
        await asyncio.sleep(e.x)

# ================= CHANNEL HANDLER =================

@StreamBot.on_message(
    filters.channel & ~filters.group &
    (filters.document | filters.video | filters.photo) &
    ~filters.forwarded,
    group=-1
)
async def channel_receive_handler(bot: Client, broadcast: Message):

    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return

    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)

        stream_link = (
            f"{Var.URL}watch/{log_msg.id}/"
            f"{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        )
        online_link = (
            f"{Var.URL}{log_msg.id}/"
            f"{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        )

        await log_msg.reply_text(
            text=(
                f"**Channel:** `{broadcast.chat.title}`\n"
                f"**Channel ID:** `{broadcast.chat.id}`\n"
                f"**Stream URL:** {stream_link}"
            ),
            quote=True
        )

        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("◉ STREAM ◉", url=stream_link),
                        InlineKeyboardButton("● DOWNLOAD ●", url=online_link),
                    ]
                ]
            )
        )

    except FloodWait as e:
        await asyncio.sleep(e.x)

    except Exception as err:
        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"❌ **ERROR:** `{err}`",
            disable_web_page_preview=True
        )
