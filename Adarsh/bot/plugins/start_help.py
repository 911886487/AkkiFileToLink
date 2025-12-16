# (c) Adarsh-Goel

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from Adarsh.bot import StreamBot
from Adarsh.vars import Var
from Adarsh.utils.database import db
from Adarsh.utils.human_readable import humanbytes
from Adarsh.bot.plugins.stream import MY_PASS
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size


# ================= SAFE LOG FUNCTION =================

async def safe_log(bot, text):
    """
    Send log message to BIN_CHANNEL safely
    (will NEVER crash bot)
    """
    if not Var.BIN_CHANNEL:
        return
    try:
        await bot.send_message(Var.BIN_CHANNEL, text)
    except Exception:
        # ignore all BIN_CHANNEL errors
        pass


# ================= START COMMAND =================

@StreamBot.on_message(filters.command("start") & filters.private)
async def start_handler(b, m: Message):

    # ---- Save user ----
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await safe_log(
            b,
            f"#NEW_USER\n\n"
            f"Name: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
            f"ID: `{m.from_user.id}`"
        )

    usr_cmd = m.text.split("_")[-1]

    # ---- Normal /start ----
    if usr_cmd == "/start":
        await m.reply_photo(
            photo="https://files.catbox.moe/he6d75.jpg
",
            caption=(
                "**ʜᴇʟʟᴏ ⚡**\n\n"
                "ɪ ᴀᴍ ᴀ **ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ / ᴠɪᴅᴇᴏ ᴛᴏ ᴘᴇʀᴍᴀɴᴇɴᴛ "
                "ʟɪɴᴋ & sᴛʀᴇᴀᴍ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ.**\n\n"
                "**Use /help for more details**\n\n"
                "**Send me any file / video to see my power ⚡**"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⚡ UPDATES ⚡", url="https://t.me/pirateakki"),
                        InlineKeyboardButton("⚡ SUPPORT ⚡", url="https://t.me/Premium_Plan_buyer_Bot"),
                    ],
                    [
                        InlineKeyboardButton("OWNER", url="https://t.me/Premium_Plan_buyer_Bot"),
                        InlineKeyboardButton("💠 DEVELOPER", url="https://t.me/pirateakki"),
                    ],
                ]
            ),
        )
        return

    # ---- Start with file id ----
    try:
        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, ids=int(usr_cmd))
    except Exception:
        return await m.reply_text("❌ Invalid or expired link.")

    if get_msg.video:
        file_size = humanbytes(get_msg.video.file_size)
        file_name = get_msg.video.file_name
    elif get_msg.document:
        file_size = humanbytes(get_msg.document.file_size)
        file_name = get_msg.document.file_name
    elif get_msg.audio:
        file_size = humanbytes(get_msg.audio.file_size)
        file_name = get_msg.audio.file_name
    else:
        return await m.reply_text("❌ Unsupported file type.")

    stream_link = (
        f"https://{Var.FQDN}/{get_msg.id}"
        if Var.ON_HEROKU or Var.NO_PORT
        else f"http://{Var.FQDN}:{Var.PORT}/{get_msg.id}"
    )

    msg_text = (
        "**⚡ Your link is generated!**\n\n"
        f"📂 **File name:** `{file_name}`\n"
        f"📦 **File size:** `{file_size}`\n\n"
        f"🔗 **Download link:** {stream_link}\n\n"
        "♻️ This link is permanent and won’t expire"
    )

    await m.reply_text(
        msg_text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⚡ DOWNLOAD NOW ⚡", url=stream_link)]]
        ),
    )
