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

conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for val in cfgtelegrambot.currency_dict.values():
    buttons.append(types.KeyboardButton(val[1]))
conv_markup.add(*buttons)

# Обрабатываются все сообщения, содержащие команду '/start'.
@bot.message_handler(commands=['start',])
def handle_start(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, привет')  # message.chat.username -
    bot.send_message(message.chat.id, 'Бот вроде что-то возвращает')

# Обрабатываются все сообщения, содержащие команду '/help'.
@bot.message_handler(commands=['help',])
def handle_help(message):
    bot.send_message(message.chat.id, 'Бот вроде что-то возвращает')
    bot.send_message(message.chat.id, 'Команды бота:\n'
                                      '/start - приветствие =)\n'
                                      '/help - помощь\n'
                                      '/explore - запуск\n'
                                      '/valutes - список ')

# Обрабатываются все сообщения, содержащие команду '/valutes'.
@bot.message_handler(commands=['valutes', ])
def handle_valutes(message):
    val_dict = []
    for val_k, val_v in cfgtelegrambot.currency_dict.items():
        val_dict.append(val_k + ' - ' + val_v[0])
    bot.send_message(message.chat.id, 'Доступные валюты:\n' + '\n'.join(val_dict))

@bot.message_handler(commands=['explore', ])
def handle_convert(message):
    bot.send_message(message.chat.id, 'В какой валюте ценник ?', reply_markup=conv_markup)
    bot.register_next_step_handler(message, handle_base)

def handle_base(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Сколько стоит предложение ?')
    currency = message.text.split()[0]
    bot.register_next_step_handler(message, handle_quote, currency)

def handle_quote(message: telebot.types.Message, currency):
    bot.send_message(message.chat.id, 'Сколько раз закупаем ?')
    amount = message.text.split()[0]
    bot.register_next_step_handler(message, handle_amount, currency, amount)

def handle_amount(message: telebot.types.Message, currency, amount):
    try:
        curr_code = 'RUB'
        if currency == 'доллар':  # Если клиент вводит сумму в долларах, нужно прокинуть код валюты для дальнейших селектов.
            curr_code = 'USD'
        elif currency == 'евро':  # Если клиент вводит сумму в евро, , нужно прокинуть код валюты для дальнейших селектов
            curr_code = 'EUR'
        else:  # Если клиент вводит сумму в рублях, то ничего пересчитывать не надо
            pass
        quantity = int(message.text.split()[0])
        amount = float(amount)
    except ValueError as err:
        bot.send_message(message.chat.id, err)
    except extensions_plr.AmountIncorrect as err:
        bot.send_message(message.chat.id, err)
    else:
        a = extensions_plr.select_data(None, None, amount, None, quantity, curr_code)

        # Селект вернул нам атрибуты предложения
        name_req = a[0][1]  # Здесь мы вытаскиваем наименование предложения из первой строки (строка должна быть единственной, но пока это не факт...)
        amount = a[0][5]    # Это цена, по которой мы предлагаем набор клиенту
        # Получение итоговой стоимости
        total_amount = amount * quantity

        # Выводим данные пользователю
        bot.reply_to(message, '{}. Стоимость в рублях: {:8.2f} ({:2d} X {:8.2f})'.format(name_req, total_amount, quantity, amount))

        # Вывод картинки найденного предложения
        fname = extensions_plr.write_to_file(a[0][6], a[1])
        bot.send_photo(chat_id=message.chat.id, photo=open(fname, 'rb'), caption='Состав набора')
    finally:
        pass

bot.polling(none_stop=True)

