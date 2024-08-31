# Задание
# Напишите Telegram-бота, в котором будет реализован следующий функционал:
# Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
# Человек должен отправить сообщение боту в виде <имя валюты, цену которой он хочет узнать> <имя валюты, в которой
# надо узнать цену первой валюты> <количество первой валюты>.

import ChatBot.extensions as extensions
import telebot
import ChatBot.config as cfgtelegrambot

bot = telebot.TeleBot(cfgtelegrambot.TOKEN)

command_list = ['/start',     # старт
                '/help',      # помощь
                '/values'     # список доступных валют
                ]

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
                                      '/valutes - список доступных валют')

# Обрабатываются все сообщения, содержащие команду '/valutes'.
@bot.message_handler(commands=['valutes', ])
def handle_valutes(message):
    val_dict = []
    for val_k, val_v in cfgtelegrambot.currency_dict.items():
        val_dict.append(val_k + ' - ' + val_v[0])
    bot.send_message(message.chat.id, 'Доступные валюты:\n' + '\n'.join(val_dict))

@bot.message_handler(content_types=['text',])
def handle_text(message):
    try:
        if message.text not in command_list:
            base = message.text.split()[0]    # валюта которую пересчитываем
            quote = message.text.split()[1]   # валюта в которую пересчитываем
            amount = message.text.split()[2]  # необходимая сумма
    except extensions.AmountIncorrect as err:
        bot.send_message(message.chat.id, err)
    except extensions.CurrentEqual as err:
        bot.send_message(message.chat.id, err)
    except extensions.CurrentNotFound as err:
        bot.send_message(message.chat.id, err)
    except extensions.JsonDecodIncorrect as err:
        bot.send_message(message.chat.id, err)
    else:
        ex = extensions.Exchange([], base, quote, amount)
        date_rate, rate_value, rp_list = ex.get_currency_rates()  # получение курсов
        for r_code, r_value in rate_value.items():
            # выводим данные пользователю
            # bot.send_message(message.chat.id, f'{r_value} {rp_list[1]} за {amount} {rp_list[0]}\nДата обновления курса: {date_rate}')
            bot.reply_to(message,
                         f'{r_value} {rp_list[1]} за {amount} {rp_list[0]}\nДата обновления курса: {date_rate}')
    finally:
        bot.send_message(message.chat.id, 'Спасибо Вам за использование нашего бота!')

# bot.delete_webhook()
bot.polling(none_stop=True)

