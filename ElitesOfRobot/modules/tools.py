import time
import requests
import datetime
import platform

from time import sleep
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from spamwatch import __version__ as __sw__
from pythonping import ping as ping3

from telegram import __version__
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CommandHandler, run_async, Filters, CallbackContext

from ElitesOfRobot import since_time_start, dispatcher, OWNER_ID
from ElitesOfRobot.modules.helper_funcs.filters import CustomFilters
from ElitesOfRobot.modules.helper_funcs.alternate import typing_action
# get current time - ping
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

@run_async
def ping(update: Update, context: CallbackContext):
    msg = update.effective_message

    start_time = time.time()
    message = msg.reply_text("Pinging")
    end_time = time.time()
    message.edit_text("Pinging.")
    message.edit_text("Pinging..")
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    uptime = get_readable_time((time.time() - since_time_start))

    message.edit_text("Pinging...")
    message.edit_text(
        "PONG!!\n"
        "<b>Time Taken :</b> <code>{}</code>\n"
        "<b>Service Uptime :</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode=ParseMode.HTML)


@run_async
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
            update.effective_message.reply_text("I Left That Chat!")
        except TelegramError:
            update.effective_message.reply_text("I Could Not Leave That Group(Dunno Why Tho).")
    else:
        update.effective_message.reply_text("Send A Valid Chat ID")



@run_async
@typing_action
def get_bot_ip(update, context):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    res = requests.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)




@run_async
@typing_action
def system_status(update, context):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    status = "<b>======[ SYSTEM INFO ]======</b>\n\n"
    status += "<b>System Uptime:</b> <code>" + str(uptime) + "</code>\n"

    uname = platform.uname()
    status += "<b>System:</b> <code>" + str(uname.system) + "</code>\n"
    status += "<b>Node name:</b> <code>" + str(uname.node) + "</code>\n"
    status += "<b>Release:</b> <code>" + str(uname.release) + "</code>\n"
    status += "<b>Version:</b> <code>" + str(uname.version) + "</code>\n"
    status += "<b>Machine:</b> <code>" + str(uname.machine) + "</code>\n"
    status += "<b>Processor:</b> <code>" + str(uname.processor) + "</code>\n\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += "<b>CPU usage:</b> <code>" + str(cpu) + " %</code>\n"
    status += "<b>Ram usage:</b> <code>" + str(mem[2]) + " %</code>\n"
    status += "<b>Storage used:</b> <code>" + str(disk[3]) + " %</code>\n\n"
    status += "<b>Python version:</b> <code>" + python_version() + "</code>\n"
    status += "<b>Library version:</b> <code>" + str(__version__) + "</code>\n"
    status += "<b>Spamwatch API:</b> <code>" + str(__sw__) + "</code>\n"
    context.bot.sendMessage(update.effective_chat.id, status, parse_mode=ParseMode.HTML)


PING_HANDLER = CommandHandler("ping", ping, filters=CustomFilters.sudo_filter)
LEAVE_HANDLER = CommandHandler("leave", leave, filters=CustomFilters.sudo_filter)
IP_HANDLER = CommandHandler("ip", get_bot_ip, filters=Filters.chat(OWNER_ID))
SYS_STATUS_HANDLER = CommandHandler(
    "sysinfo", system_status, filters=CustomFilters.sudo_filter
)


dispatcher.add_handler(PING_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(IP_HANDLER) 
dispatcher.add_handler(SYS_STATUS_HANDLER)
