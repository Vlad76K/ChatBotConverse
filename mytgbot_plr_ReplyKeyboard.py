# Задание
# Напишите Telegram-бота, в котором будет реализован следующий функционал:
# Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
# Человек должен отправить сообщение боту в виде <имя валюты, цену которой он хочет узнать> <имя валюты, в которой
# надо узнать цену первой валюты> <количество первой валюты>.

import ChatBot.extensions_plr as extensions_plr
import telebot
import ChatBot.config as cfgtelegrambot
from telebot import types

bot = telebot.TeleBot(cfgtelegrambot.TOKEN)

command_list = ['/start',     # старт
                '/help',      # помощь
                '/convert',   # запуск конвертера валют
                '/values'     # список доступных валют
                ]

# conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
# buttons = []
# for val in cfgtelegrambot.currency_dict.values():
#     buttons.append(types.KeyboardButton(val[1]))
# conv_markup.add(*buttons)

def handle_start(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, привет')  # message.chat.username -
    bot.send_message(message.chat.id, 'Бот вроде что-то возвращает )))')

@bot.message_handler(func=lambda message: message.text == 'Написать в поддержку')
def write_to_support(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введите своё имя')
    bot.register_next_step_handler(message, handle_start)

@bot.callback_query_handler(func=lambda call: call.data == 'save_data')
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Данные сохранены!')

@bot.callback_query_handler(func=lambda call: call.data == 'change_data')
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Изменение данных!')
    write_to_support(message)

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    # list_proposal = extensions_plr.select_all_data([])
    # i = 0
    # if len(list_proposal) > 0:
    #     keyboard.add(button_save, button_change)
    #     for el in list_proposal:
    #         # button_sale = telebot.types.InlineKeyboardButton(text=list_proposal[i], callback_data='change_data')
    #         # keyboard.add(button_sale)
    #         fname = extensions_plr.write_to_file(list_proposal[i][2], f'E:\Games\RSL\VVV\\{list_proposal[i][1]}.jpg')
    #         bot.send_photo(chat_id=message.chat.id, photo=open(fname, 'rb'), caption=f'Цена: {list_proposal[i][1]}', reply_markup=keyboard)
    #         i = i + 1
    #
    # extensions_plr.qr_code(data, filename)

    button_support = telebot.types.KeyboardButton(text="Написать в поддержку")
    button1 = telebot.types.KeyboardButton(text="Кнопка 1")
    button2 = telebot.types.KeyboardButton(text="Кнопка 2")
    button3 = telebot.types.KeyboardButton(text="Кнопка 3")
    keyboard.add(button_support, button1)
    keyboard.add(button2, button3)
    # Вывод картинки найденного предложения
    bot.send_message(chat_id, 'Добро пожаловать в бота покупки наборов', reply_markup=keyboard)

@bot.message_handler(commands=['remove_keyboard'])
def remove_keyboard(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id,
                     'Удаляю клавиатуру',
                     reply_markup=keyboard)

bot.polling(none_stop=True)

