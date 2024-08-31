# Задание
# Напишите Telegram-бота, в котором будет реализован следующий функционал:
# Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
# Человек должен отправить сообщение боту в виде <имя валюты, цену которой он хочет узнать> <имя валюты, в которой
# надо узнать цену первой валюты> <количество первой валюты>.

import requests
from datetime import datetime
from rest_framework.exceptions import APIException
from ChatBot.config import API_KEY, currency_dict

class ExchangeBotException(APIException):
    pass

class CurrentNotFound(ExchangeBotException):
    def __init__(self, curr):
        self.curr = curr
        super().__init__(f'Валюта {curr} не найдена\n'
                         f'Список доступных валют можно посмотреть командой /valutes')

class CurrentEqual(ExchangeBotException):
    def __init__(self):
        super().__init__(f'Валюты не должны быть идентичны')

class AmountIncorrect(ExchangeBotException):
    def __init__(self, amount):
        self.amount = amount
        super().__init__(f"Не корректно задана сумма: {amount}")

class JsonDecodIncorrect(ExchangeBotException):
    def __init__(self, err_msg):
        self.err_msg = err_msg
        super().__init__(f"Ошибки в обработке ответа с сайта курсов: {err_msg}")

class Exchange:
    def __init__(self, input_list, base, quote, amount):
        self.input_list = input_list
        self.base = base
        self.quote = quote
        self.amount = amount

    @staticmethod
    def get_price(base, quote, amount=1): #get_currency_rates(base, quote, amount=1):
        url = f"http://data.fixer.io/api/latest?access_key={API_KEY}&symbols={base},{quote}&format=1"
        data = requests.get(url).json()
        if data["success"]:
            rates = data["rates"]

            exchange_rate = 1 / rates[base] * rates[quote]
            price_datetime = datetime.fromtimestamp(data["timestamp"])

            return price_datetime, {quote : round(exchange_rate * amount, 2)}, [currency_dict[base][2], currency_dict[quote][2]]

    # @staticmethod
    def get_currency_rates(self): #, base, quote, amount=1): #get_price(base, quote, amount):
        try:
            amount = round(float(self.amount.replace(',', '.')), 2)
            if amount <= 0:
                raise AmountIncorrect(amount)

            base_code = ''
            quote_code = ''

            # определим буквенный ISO-код валюты (нужен для запроса курса)
            for dict_key, dict_values in currency_dict.items():
                # код валюты, указанную сумму которой, нужно пересчитать
                if dict_key == self.base:
                    base_code = self.base
                else:
                    for i in range(len(dict_values)):
                        if dict_values[i] == self.base.lower():
                            base_code = dict_key
                            break
                # код валюты в которую нужно пересчитать указанную пользователем сумму
                if dict_key == self.quote:
                    quote_code = self.quote
                else:
                    for i in range(len(dict_values)):
                        if dict_values[i] == self.quote.lower():
                            quote_code = dict_key
                            break
            # если какую-либо валюту не определили - вызываем эксепшн
            if base_code == '':
                raise CurrentNotFound(self.base)
            if quote_code == '':
                raise CurrentNotFound(self.quote)
            if base_code == quote_code:
                raise CurrentEqual()

        except CurrentNotFound:  # если с определением валюты возникли проблемы
            raise
        except AmountIncorrect:  # если некорректно введна сумма (меньше или равно нулю)
            raise
        except JsonDecodIncorrect:  # если тег 'td' на найден в полученном ответе
            raise
        else:
            # если ошибок не было - выполняем конвертацию
            price_datetime, exchange_rates, curr_rp_list = Exchange.get_price(base_code, quote_code, amount)

            return price_datetime, exchange_rates, curr_rp_list
        finally:
            print('Спасибо, что выбрали наше решение! =)')

if __name__ == '__main__':
    input_list = ['евро', 'доллары', '10']
    # input_list = ['EUR', 'RUB', '10']
    base = input_list[0]
    quote = input_list[1]
    amount = float(input_list[2])
    ex = Exchange([], base, quote, amount)
    print(ex.get_currency_rates())

