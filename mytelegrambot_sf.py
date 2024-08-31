# Задание
# Напишите Telegram-бота, в котором будет реализован следующий функционал:
# Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
# Человек должен отправить сообщение боту в виде <имя валюты, цену которой он хочет узнать> <имя валюты, в которой
# надо узнать цену первой валюты> <количество первой валюты>.

import ChatBot.extensions as extensions
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
    bot.send_message(message.chat.id, 'Бот возвращает цену на определённое количество валюты (список можно посмотреть набрав команду /valutes).\n'
                                      'Напишите какую валюту в какую пересчитать и сумму '
                                      '(например: EUR RUB 10 или евро рубль 10)')

# Обрабатываются все сообщения, содержащие команду '/help'.
@bot.message_handler(commands=['help',])
def handle_help(message):
    bot.send_message(message.chat.id, 'Бот возвращает цену на определённое количество валюты (список можно посмотреть набрав команду /valutes).\n'
                                      'Напишите какую валюту в какую пересчитать и сумму '
                                      '(например: EUR RUB 10 или евро рубль 10)')
    bot.send_message(message.chat.id, 'Команды бота:\n'
                                      '/start - приветствие =)\n'
                                      '/help - помощь\n'
                                      '/convert - запуск конвертера\n'
                                      '/valutes - список доступных валют')

# Обрабатываются все сообщения, содержащие команду '/valutes'.
@bot.message_handler(commands=['valutes', ])
def handle_valutes(message):
    val_dict = []
    for val_k, val_v in cfgtelegrambot.currency_dict.items():
        val_dict.append(val_k + ' - ' + val_v[0])
    bot.send_message(message.chat.id, 'Доступные валюты:\n' + '\n'.join(val_dict))

@bot.message_handler(commands=['convert', ])
def handle_convert(message):
    bot.send_message(message.chat.id, 'Какую валюту Вам нужно сконвертировать ?', reply_markup=conv_markup)
    bot.register_next_step_handler(message, handle_base)

def handle_base(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'В какую валюту нужно сконвертировать ?', reply_markup=conv_markup)
    bot.register_next_step_handler(message, handle_quote, message.text.split()[0])

def handle_quote(message: telebot.types.Message, base):
    bot.send_message(message.chat.id, 'Какую сумму нужно сконвертировать ?')
    bot.register_next_step_handler(message, handle_amount, base, message.text.split()[0])

def handle_amount(message: telebot.types.Message, base, quote):
    try:
        amount = message.text.split()[0].replace(',', '.')
        if float(amount) <= 0:
            raise extensions.AmountIncorrect()
        ex = extensions.Exchange([], base, quote, amount)
        date_rate, rate_value, rp_list = ex.get_currency_rates()  # получение курсов
    except ValueError as err:
        bot.send_message(message.chat.id, err)
    except extensions.AmountIncorrect as err:
        bot.send_message(message.chat.id, err)
    except extensions.CurrentEqual as err:
        bot.send_message(message.chat.id, err)
    except extensions.CurrentNotFound as err:
        bot.send_message(message.chat.id, err)
    except extensions.JsonDecodIncorrect as err:
        bot.send_message(message.chat.id, err)
    else:
        for r_code, r_value in rate_value.items():
            # выводим данные пользователю
            bot.reply_to(message, f'{r_value} {rp_list[1]} за {amount} {rp_list[0]}\nДата обновления курса: {date_rate}')
    finally:
        pass


bot.polling(none_stop=True)

