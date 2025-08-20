# VILLAIN_MUSIC/plugins/banall.py

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus
import asyncio

CONFIRM_TEXT = "confirm"  # /banall confirm

async def _is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    try:
        m = await client.get_chat_member(chat_id, user_id)
        return m.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)
    except Exception:
        return False

def _human_name(u):
    if not u: 
        return "user"
    if u.first_name: 
        return f"{u.first_name} {u.last_name or ''}".strip()
    return u.username or str(u.id)

@Client.on_message(filters.command(["banall"]) & filters.group)
async def ban_all_cmd(client: Client, message: Message):
    chat = message.chat
    if chat.type not in (ChatType.SUPERGROUP, ChatType.GROUP):
        return await message.reply_text("यह कमांड सिर्फ़ groups में चलता है.")

    user = message.from_user
    if not user or not await _is_admin(client, chat.id, user.id):
        return await message.reply_text("सिर्फ़ group owner/admin ही यह कमांड चला सकते हैं.")

    args = message.text.split(maxsplit=1)
    arg = args[1].strip().lower() if len(args) > 1 else ""

    # Preview mode
    if arg == "preview":
        total = 0
        protected = 0
        async for member in client.get_chat_members(chat.id):
            st = member.status
            if st in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR) or member.user.is_bot:
                protected += 1
                continue
            total += 1
        return await message.reply_text(
            f"Preview:\n• Ban होने वाले members (approx): {total}\n"
            f"• Skip (admins/owner/bots): {protected}\n\n"
            f"Execute करने के लिए: `/banall {CONFIRM_TEXT}`",
            quote=True
        )

    # Require explicit confirmation
    if arg != CONFIRM_TEXT:
        return await message.reply_text(
            f"⚠️ यह **mass-ban** action है.\n"
            f"पहले preview देखो: `/banall preview`\n"
            f"Execute करने के लिए टाइप करो: `/banall {CONFIRM_TEXT}`",
            quote=True
        )

    await message.reply_text("🚨 Mass-ban शुरू… admins/owner/bots को skip किया जाएगा. कृपया इंतज़ार करें.", quote=True)

    banned = 0
    skipped = 0
    failed = 0

    # Gentle rate limit to avoid flood-wait
    RATE_DELAY = 0.35  # seconds; tweak as needed

    async for member in client.get_chat_members(chat.id):
        try:
            # Skip protected members
            if member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR) or member.user.is_bot:
                skipped += 1
                continue
            # Avoid banning self or the command invoker by mistake
            if member.user.id in (user.id, (await client.get_me()).id):
                skipped += 1
                continue

            await client.ban_chat_member(chat.id, member.user.id)
            banned += 1
            await asyncio.sleep(RATE_DELAY)
        except Exception:
            failed += 1
            # small backoff in case of FLOOD_WAIT or transient errors
            await asyncio.sleep(RATE_DELAY + 0.2)

    await message.reply_text(
        f"✅ Done.\n• Banned: {banned}\n• Skipped (admins/owner/bots/self): {skipped}\n• Failed: {failed}",
        quote=True
    )

@Client.on_message(filters.command(["unbanall"]) & filters.group)
async def unban_all_cmd(client: Client, message: Message):
    """Use with extreme care: unbans everyone who is currently banned (doesn't re-add them)."""
    chat = message.chat
    user = message.from_user

    if not user or not await _is_admin(client, chat.id, user.id):
        return await message.reply_text("सिर्फ़ group owner/admin ही यह कमांड चला सकते हैं.")

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or args[1].strip().lower() != CONFIRM_TEXT:
        return await message.reply_text(
            f"यह mass-unban action है. चलाने के लिए लिखो: `/unbanall {CONFIRM_TEXT}`", quote=True
        )

    await message.reply_text("♻️ Mass-unban शुरू…", quote=True)

    unbanned = 0
    failed = 0
    RATE_DELAY = 0.35

    try:
        async for banned_user in client.get_chat_members(chat.id, filter="banned"):
            try:
                await client.unban_chat_member(chat.id, banned_user.user.id)
                unbanned += 1
                await asyncio.sleep(RATE_DELAY)
            except Exception:
                failed += 1
                await asyncio.sleep(RATE_DELAY + 0.2)
    except Exception:
        failed += 1

    await message.reply_text(f"✅ Unban done.\n• Unbanned: {unbanned}\n• Failed: {failed}", quote=True)
        
