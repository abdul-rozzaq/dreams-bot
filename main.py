from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from helper import *

from config import TOKEN

import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)


bot = Updater(TOKEN)


keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⬅️', callback_data='previus'),
            InlineKeyboardButton('❌', callback_data='delete'),
            InlineKeyboardButton('➡️', callback_data='next'),
        ],
    ]
)


def getMessage(context: CallbackContext, mean: Dream):
    length, index = len(context.chat_data['means']), context.chat_data['mean_index'] + 1
    return f"<b>Id</b>: {mean.id} \n<b>Muallif</b>: {mean.author} \n\n<b>Sarlavha</b>: {mean.title} \n\n<b>Ma'nosi</b>: {mean.meaning}\n\n\n<b>{index}/{length}</b>"
    
     

def start(update: Update, context: CallbackContext):
    user = update.effective_user    
    update.message.reply_text(f'Assalomu alaykum {user.first_name} 👋🏻\n\nSiz bu bot yordamida tushlarning ta\'birini bilishingiz mumkin. Tushingizda nimani ko\'rdingiz?') 


def dreams(update: Update, context: CallbackContext):

    loader = update.message.reply_text("<i>Yuklanmoqda ...</i>", parse_mode='HTML')
    
    message = update.message.text
    means = getMeans(message)
    
    context.chat_data['means'] = means
    context.chat_data['mean_index'] = 0
    
    loader.delete()
    
    if len(means) != 0:
        mean = context.chat_data['means'][context.chat_data['mean_index']]
        
        return update.message.reply_text(getMessage(context, mean), parse_mode='HTML', reply_markup=keyboard)

    else:
        return update.message.reply_text(f"<b>{message}</b> mavzusida hech qanday ma'lumot topilmadi 😔", parse_mode='HTML',)
    

def inlineHandler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    chat_data = context.chat_data
    
    if query.data == 'next':
        index = chat_data['mean_index']
        means = chat_data['means']
        
        if index != len(means) - 1:
            chat_data['mean_index'] += 1
            mean = means[chat_data['mean_index']]
            
        else:
            chat_data['mean_index'] = 0
            mean = means[0]
          
    elif query.data == 'previus':
        index = chat_data['mean_index']
        means = chat_data['means']
        
        if index !=  0:
            chat_data['mean_index'] -= 1
            mean = means[chat_data['mean_index']]
            
        else:
            chat_data['mean_index'] = len(means) - 1
            mean = means[-1]
       
    elif query.data == 'delete':
        query.delete_message()
        
        return

    return query.edit_message_text(getMessage(context, mean), parse_mode='HTML', reply_markup=keyboard)


bot.dispatcher.add_handler(CommandHandler('start', start))
bot.dispatcher.add_handler(MessageHandler(Filters.text, dreams))

bot.dispatcher.add_handler(CallbackQueryHandler(inlineHandler))

bot.start_polling()
bot.idle()