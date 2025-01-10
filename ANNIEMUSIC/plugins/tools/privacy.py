from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from ANNIEMUSIC import app
import config

TEXT = f"""
```🔒ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ ғᴏʀ {app.username}``` !

**ʏᴏᴜʀ ᴘʀɪᴠᴀᴄʏ ɪs ɪᴍᴘᴏʀᴛᴀɴᴛ ᴛᴏ ᴜs. ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ʜᴏᴡ ᴡᴇ ᴄᴏʟʟᴇᴄᴛ, ᴜsᴇ, ᴀɴᴅ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ᴅᴀᴛᴀ, ᴘʟᴇᴀsᴇ ʀᴇᴠɪᴇᴡ ᴏᴜʀ ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ ʜᴇʀᴇ** : [ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ](https://telegra.ph/Privacy-Policy-for-01-10).

**ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴏʀ ᴄᴏɴᴄᴇʀɴs, ғᴇᴇʟ ғʀᴇᴇ ᴛᴏ ʀᴇᴀᴄʜ ᴏᴜᴛ ᴛᴏ ᴏᴜʀ** [sᴜᴘᴘᴏʀᴛ ᴛᴇᴀᴍ ](https://t.me/THUNDERBOLTFANTASY).
"""

@app.on_message(filters.command("privacy"))
async def privacy(client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "𝑉𝑖𝑒𝑤 𝑃𝑟𝑖𝑣𝑎𝑐𝑦 𝑃𝑜𝑙𝑖𝑐𝑦", url="https://telegra.ph/Privacy-Policy-for-01-10"
                )
            ]
        ]
    )
    await message.reply_text(
        TEXT, 
        reply_markup=keyboard, 
        parse_mode=ParseMode.MARKDOWN, 
        disable_web_page_preview=True
    )
