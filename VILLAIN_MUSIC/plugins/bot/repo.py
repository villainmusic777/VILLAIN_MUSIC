from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from VILLAIN_MUSIC import app
from config import BOT_USERNAME
from VILLAIN_MUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """
✰ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐀𝐒𝐓𝐀 𝐑𝐄𝐏𝐎𝐒 ✰
 
✰ 𝐑𝐄𝐏𝐎 𝐓𝐎𝐇 𝐍𝐇𝐈 𝐌𝐈𝐋𝐄𝐆𝐀 𝐁𝐒𝐃𝐊
 
✰ 𝐏𝐇𝐄𝐋𝐄 𝐏𝐀𝐏𝐀 𝐁𝐎𝐋 𝐑𝐄𝐏𝐎 𝐎𝐖𝐍𝐄𝐑 𝐊𝐎

✰ || @ixasta ||
 
✰ 𝐑𝐔𝐍 𝟐𝟒𝐱𝟕 𝐋𝐀𝐆 𝐅𝐑𝐄𝐄 𝐖𝐈𝐓𝐇𝐎𝐔𝐓 𝐒𝐓𝐎𝐏
 
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("ᴧᴅᴅ ϻᴇ ʙᴧʙʏ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton(" ɢʀσᴜᴘ", url="https://t.me/oldskoolgc"),
          InlineKeyboardButton("⋏ 𝛅 𝛕 ⋏", url="https://t.me/ixasta"),
          ],
               [
                InlineKeyboardButton("˹ᴀsᴛᴀ ꭙ sᴜᴘᴘᴏʀᴛ˼", url=f"https://t.me/ixasta1"),
],
[
InlineKeyboardButton("ϻᴧɪη ʙσᴛ", url=f"https://t.me/Laibaamusicbot"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://files.catbox.moe/t3mcsf.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
