import telebot
from telebot import types
from telebot.types import InlineKeyboardButton
import sqlite3

bot = telebot.TeleBot('8336492357:AAFaNP2Fh01sry8PqdxMXIZCTHTPA5-HExc')
channel_id = '@ch_vch'
user_states = {}
ADMIN_CHAT_IDS = [294829811,727302720]
#ОСНОВНОЕ МЕНЮ
def show_main_menu(chat_id, first_name):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📰 Предложить пост')
    btn2 = types.KeyboardButton('📝 Задать вопрос')
    markup.add(btn1, btn2)
    bot.send_message(chat_id,'Есть вопросы?', reply_markup=markup)

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

            show_main_menu(message.chat.id, message.from_user.first_name)

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
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ Супер, {call.from_user.first_name}! Теперь ты с нами!\nЯ Чувачок, рад тебя видеть!\nХочешь чем-то поделиться или спросить?\nЯ готов тебя выслушать!")
            show_main_menu(call.message.chat.id, call.from_user.first_name)

    except Exception as e:
        print(f"Ошибка при проверке: {e}")
        bot.answer_callback_query(call.id, "❌ Ошибка проверки подписки")


#ОБРАБОТКА КНОПКИ ЗАДАТЬ ВОПРОС
@bot.message_handler(func=lambda message: message.text == '📝 Задать вопрос')
def suggest_question(message):
    if user_states.get(message.from_user.id) in ['waiting_question', 'waiting_post']:
        bot.send_message(message.chat.id, '❌ Ты уже в процессе отправки! Дождись завершения.')
        return

    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, '⌛ Готов слушать...', reply_markup=remove_markup)

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), text varchar(1000))')
    conn.commit()
    cur.close()
    conn.close()
    user_states[message.from_user.id] = 'waiting_question'

    bot.send_message(message.chat.id,'Слушаю тебя, чувачок. Задавай свой вопрос!')

#ОБРАБОТКА текста пользователя
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_question')
def check_waiting_question(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    if message.from_user.username:
        user_name = f"@{message.from_user.username}"

#ОТЛАДКА
    print("─" * 50)
    print('Дорогие админы, какой-то папищек вам что-то прислал!')
    print("─" * 50)
    print('Его зовут:', user_name)
    print('Написал он:', message.text)
    print("─" * 50)

    admin_message = (
        f"📰 НОВЫЙ ПОСТ ОТ ПОДПИСЧИКА\n\n"
        f"👤 Пользователь: {user_name}\n"
        f"📝 Текст:\n{message.text}"
    )

    try:
        for admin_id in ADMIN_CHAT_IDS:
            bot.send_message(admin_id, admin_message)
            print(f"✅ Сообщение отправлено админу {admin_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки админу: {e}")

    cur.execute('INSERT INTO users (name, text) VALUES (?, ?)', (user_name, message.text))
    conn.commit()
    cur.close()
    conn.close()

    del user_states[user_id]
    bot.send_message(message.chat.id, '✅ Спасибо! Админы обязательно прочитают твое сообщение!')

    show_main_menu(message.chat.id, message.from_user.first_name)

#ОБРАБОТКА КНОПКИ ПРЕДЛОЖИТЬ ПОСТ
@bot.message_handler(func=lambda message: message.text == '📰 Предложить пост')
def suggest_post(message):
    if user_states.get(message.from_user.id) in ['waiting_question', 'waiting_post']:
        bot.send_message(message.chat.id, '❌ Ты уже в процессе отправки! Дождись завершения.')
        return
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, '⌛ Готов слушать...', reply_markup=remove_markup)

    conn = sqlite3.connect('database2.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, user_name TEXT, content_type TEXT, text TEXT, file_id TEXT)')
    conn.commit()
    cur.close()
    conn.close()

    user_states[message.from_user.id] = 'waiting_post'

    bot.send_message(message.chat.id,'Присылай свой пост!')
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'], func=lambda message: user_states.get(message.from_user.id) == 'waiting_post')
def check_waiting_post(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if message.from_user.username:
        user_name = f"@{message.from_user.username}"

    conn = sqlite3.connect('database2.sql')
    cur = conn.cursor()

    content_type = message.content_type
    text_content = message.text or message.caption or ''
    file_id = None

    # Получаем file_id в зависимости от типа контента
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
    elif message.content_type == 'video':
        file_id = message.video.file_id
    elif message.content_type == 'document':
        file_id = message.document.file_id
    elif message.content_type == 'audio':
        file_id = message.audio.file_id
    elif message.content_type == 'voice':
        file_id = message.voice.file_id


    cur.execute('INSERT INTO posts (user_id, user_name, content_type, text, file_id) VALUES (?, ?, ?, ?, ?)',
                (user_id, user_name, content_type, text_content, file_id))
    conn.commit()
    cur.close()
    conn.close()

    admin_message = (
        f"📰 НОВЫЙ ПОСТ ОТ ПАПИЩИКА\n\n"
        f"👤 Пользователь: {user_name}\n"
    )

    if text_content:
        admin_message += f"📝 Текст: {text_content}\n"

    try:

        for admin_id in ADMIN_CHAT_IDS:
            if content_type == 'text':
                bot.send_message(admin_id, admin_message)
            elif content_type == 'photo':
                bot.send_photo(admin_id, file_id, caption=admin_message)
            elif content_type == 'video':
                bot.send_video(admin_id, file_id, caption=admin_message)
            elif content_type == 'document':
                bot.send_document(admin_id, file_id, caption=admin_message)
            elif content_type == 'audio':
                bot.send_audio(admin_id, file_id, caption=admin_message)
            elif content_type == 'voice':
                bot.send_voice(admin_id, file_id, caption=admin_message)

            print(f"✅ {content_type} отправлен админу {admin_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки админу: {e}")

    # ОТЛАДКА
    print("─" * 50)
    print('Дорогие админы, какой-то папищек вам что-то прислал!')
    print("─" * 50)
    print('Его зовут:', user_name)
    print(f"📦 Тип: {content_type}")
    if text_content:
        print(f"📝 Текст: {text_content}")
    print("─" * 50)

    del user_states[user_id]

    bot.send_message(message.chat.id, 'Спасибо! Твой пост сохранен и отправлен на модерацию!')

    show_main_menu(message.chat.id, message.from_user.first_name)

@bot.message_handler(content_types = ['text'])
def defolt_messages(message):
    if user_states.get(message.from_user.id) not in ['waiting_question', 'waiting_post']:
        bot.send_message(message.chat.id,'Я не умею разговаривать, лучше выбери кнопки в меню!')
    show_main_menu(message.chat.id, message.from_user.first_name)

bot.polling(none_stop=True)


# добавить кнопу отмены отправки (назад в меню)
# заблокировать повторное нажатие кнопок если предложить пост или задать вопрос уже нажали