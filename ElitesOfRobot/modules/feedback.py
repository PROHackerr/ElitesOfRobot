import html

from telegram import Chat, Update, ParseMode
from telegram.ext import run_async, CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from ElitesOfRobot.modules.disable import DisableAbleCommandHandler
from ElitesOfRobot.modules.helper_funcs.extraction import extract_user_and_text, extract_text
from ElitesOfRobot import dispatcher, SUPPORT_CHAT



@run_async
def feedback(update: Update, context: CallbackContext):
  message = update.effective_message
  chat = update.effective_chat
  name = update.effective_user.first_name
  args = context.args
  user_id, reason = extract_user_and_text(message, args)
  feedbak = extract_text(message)

  feed_text = f"#FEEDBACK \n\n{context.bot.first_name}'s New Feedback From [{name}](tg://user?id={user_id}) \nUser ID: `{user_id}`  \n"
  
  if chat.username and chat.type == Chat.SUPERGROUP:
          feed_link = feed_text + f"Message Link: [Here](https://t.me/{chat.username}/{message.message_id}) \n\n• Feedback : ↧ \n{feedbak}"                                    

  else:
        feed_link = feed_text + f"\n• Feedback : ↧ \n{feedbak}"
  

  context.bot.send_message(-1001175341127, feed_link, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
 
  reply_text=f"Thank-You For Giving Us Your Feedback ;)"
  message.reply_text(reply_text, 
                     reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="You Can See Your Feedback Here", 
                                                                       url="t.me/{}".format(SUPPORT_CHAT))]]))
                                               

FEED_HANDLE = DisableAbleCommandHandler("feedback", feedback)

dispatcher.add_handler(FEED_HANDLE)
