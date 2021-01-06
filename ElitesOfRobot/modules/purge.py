import time, asyncio

from ElitesOfRobot import client, telethon, SUDO_USERS
from ElitesOfRobot.modules.helper_funcs.extraction import get_user
from ElitesOfRobot.modules.helper_funcs.telethon.chatstatus import can_delete_messages

from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError


# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    async for user in client.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in SUDO_USERS:
            admin = True
            break
    return admin


#purge
async def purge(event):
    chat = event.chat_id
    start = time.perf_counter()
    msgs = []

    if not await is_administrator(user_id=event.sender_id, message=event) and event.from_id not in [1087968824]:                           
        await event.reply("You're Not An Admin!")
        return

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to purge the message")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await event.client.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []

        try:
            await event.client.delete_messages(chat, msgs)
        except:
            pass
        time_ = time.perf_counter() - start
        del_res = await event.client.send_message(
            event.chat_id, f"Purged {count} Messages In {time_:0.2f} Secs."
        )

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = "Failed to delete messages.\n"
        text += "Messages maybe too old or I'm not admin! or dont have delete rights!"
        del_res = await event.respond(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()


#del
async def delete_msg(event):

    if not await is_administrator(user_id=event.sender_id, message=event) and event.from_id not in [1087968824]:
        await event.reply("You're not an admin!")
        return

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to delete the message")
        return

    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to some message to delete it.")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    rm = [msg, to_delete]
    await event.client.delete_messages(chat, rm)


__help__ = """
Deleting messages made easy with this command. Bot purges \
messages all together or individually.

*Admin only:*
 - /del: Deletes the message you replied to
 - /purge: Deletes all messages between this and the replied to message.
"""


__mod_name__ = "Purges"


PURGE_HANDLER = purge, events.NewMessage(pattern="^[!/]purge$")
DEL_HANDLER = delete_msg, events.NewMessage(pattern="^[!/]del$")

telethon.add_event_handler(*PURGE_HANDLER)
telethon.add_event_handler(*DEL_HANDLER)


__command_list__ = ["del", "purge"]

__handlers__ = [PURGE_HANDLER, DEL_HANDLER]
