import config
print(config.token)
#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
from random import choice



bot = telebot.TeleBot(config.token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")




@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")
    

@bot.message_handler(commands=['coin'])
def coin_handler(message):
    coin = choice(["ОРЕЛ", "РЕШКА"])
    bot.reply_to(message, coin)

    

    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
#@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)





@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, """\
About EchoBot
EchoBot is a friendly chatbot designed to reflect positive communication.
When you say something kind or nice, EchoBot repeats your exact words back to you.
Its purpose is to promote kindness, positivity, and encouragement through simple mirroring of user messages.""")
    


    
@bot.message_handler(commands=['ban'])
def ban_user(message):
    
    if not message.reply_to_message:
        bot.reply_to(message, "Ответь на сообщение того, кого хочешь забанить.")
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id

    
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status == 'administrator' or user_status == 'creator':
        bot.reply_to(message, "Невозможно забанить администратора.")
        return

    
    
    bot.ban_chat_member(chat_id, user_id)




#@bot.message_handler(func=lambda message: True)
def ban_for_links(message):
    
    if message.text and "https://" in message.text:
        chat_id = message.chat.id
        user_id = message.from_user.id

        
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            return  

        
        bot.ban_chat_member(chat_id, user_id)




        


bot.infinity_polling()