from pyUltroid.functions.welcome_db import *
from telegraph import upload_file as uf
from telethon.utils import get_display_name, pack_bot_file_id

from . import *


@ultroid_cmd(pattern="setwelcome")
async def setwel(event):
    x = await eor(event, get_string("com_1"))
    r = await event.get_reply_message()
    if event.is_private:
        return await eod(x, "Please use this in a group and not PMs!", time=10)
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await bot.download_media(r.media)
            variable = uf(dl)
            m = "https://telegra.ph" + variable[0]
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eod(x, "`Unsupported Media`")
            else:
                dl = await bot.download_media(r.media)
                variable = uf(dl)
                m = "https://telegra.ph" + variable[0]
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            add_welcome(event.chat_id, r.message, m)
        else:
            add_welcome(event.chat_id, None, m)
        await eor(x, "`Welcome note saved`")
    elif r.text:
        add_welcome(event.chat_id, r.message, None)
        await eor(x, "`Welcome note saved`")
    else:
        await eod(x, "`Reply to message which u want to set as welcome`")


@ultroid_cmd(pattern="clearwelcome$")
async def clearwel(event):
    if not get_welcome(event.chat_id):
        await eod(event, "`No welcome was set!`", time=5)
    delete_welcome(event.chat_id)
    await eod(event, "`Welcome Note Deleted`")


@ultroid_cmd(pattern="getwelcome$")
async def listwel(event):
    wel = get_welcome(event.chat_id)
    if not wel:
        await eod(event, "`No welcome was set!`", time=5)
    msgg = wel["welcome"]
    med = wel["media"]
    await event.reply(f"**Welcome Note in this chat**\n\n`{msgg}`", file=med)
    await event.delete()


@ultroid_bot.on(events.ChatAction())
async def _(event):
    wel = get_welcome(event.chat_id)
    if wel:
        if event.user_joined or event.user_added:
            user = await event.get_user()
            chat = await event.get_chat()
            title = chat.title if chat.title else "this chat"
            pp = await event.client.get_participants(chat)
            count = len(pp)
            mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
            name = user.first_name
            last = user.last_name
            if last:
                fullname = f"{name} {last}"
            else:
                fullname = name
            uu = user.username
            if uu:
                username = f"@{uu}"
            else:
                username = mention
            msgg = wel["welcome"]
            med = wel["media"]
            userid = user.id
            await event.reply(
                msgg.format(
                    mention=mention,
                    title=title,
                    count=count,
                    name=name,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                ),
                file=med,
            )
