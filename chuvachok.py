import telebot
from telebot import types
from telebot.types import InlineKeyboardButton

bot = telebot.TeleBot('8336492357:AAFaNP2Fh01sry8PqdxMXIZCTHTPA5-HExc')
channel_id = '@ch_vch'


#ПРОВЕРКА ПОДПИСЧКИ НА КАНАЛ
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    try:
        chat_member = bot.get_chat_member(channel_id, user_id)
        print(f"Статус пользователя {user_id}: {chat_member.status}")

        if chat_member.status == 'left':

            markup = types.InlineKeyboardMarkup()
            sub_but = InlineKeyboardButton('Подписаться на канал', url='https://t.me/ch_vch')
            ch_but = InlineKeyboardButton('Я подписался!', callback_data="check_subscription")
            markup.add(sub_but, ch_but)

            bot.send_message(message.chat.id,f'Не, {message.from_user.first_name}, слушай, так не пойдет😡!\nСначала подпишись, а потом поговорим🤓', reply_markup = markup)

        else:
            bot.send_message(message.chat.id,f'Отлично, {message.from_user.first_name}, рад тебя видеть!')
            bot.send_message(message.chat.id, 'Я Чувачок, я вижу, что ты наш папищек!')
            bot.send_message(message.chat.id, 'Хочешь чем-то поделиться или спросить? Я готов тебя выслушать!')

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Ошибка при проверке подписки.")

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")


def check_subscription(call):
    user_id = call.from_user.id

    try:
        chat_member = bot.get_chat_member(channel_id, user_id)

        if chat_member.status == 'left':
            # Если все еще не подписан
            bot.answer_callback_query(
                call.id,
                "❌ Ты еще не подписался! Нажми на кнопку 'Подписаться на канал'",
                show_alert=True
            )
        else:
            # Если подписался
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"✅ Супер, {call.from_user.first_name}! Теперь ты с нами!\n\n"
                     "Я Чувачок, рад тебя видеть!\nХочешь чем-то поделиться или спросить?\nЯ готов тебя выслушать!"
            )

    except Exception as e:
        print(f"Ошибка при проверке: {e}")
        bot.answer_callback_query(call.id, "❌ Ошибка проверки подписки")






bot.polling(none_stop=True)



# добавить в случае не подписки кнопку, чтобы подписаться
# добавить сбор инфы о пользователе
# добавить кнопки
#