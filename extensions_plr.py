# Чат-бот для Телеграм. Покупка донат-предложений

import sqlite3, qrcode
import requests
from datetime import datetime
from rest_framework.exceptions import APIException
from ChatBot.config import API_KEY, currency_dict
import tensorflow as tf

def tensor_flow():
    pass
    # print('list_physical_devices ::: ', tf.config.list_physical_devices('GPU'))
    # mnist = tf.keras.datasets.mnist
    #
    # (x_train, y_train),(x_test, y_test) = mnist.load_data()
    # x_train, x_test = x_train / 255.0, x_test / 255.0
    #
    # model = tf.keras.models.Sequential([
    #   tf.keras.layers.Flatten(input_shape=(28, 28)),
    #   tf.keras.layers.Dense(128, activation='relu'),
    #   tf.keras.layers.Dropout(0.2),
    #   tf.keras.layers.Dense(10, activation='softmax')
    # ])
    #
    # model.compile(optimizer='adam',
    #   loss='sparse_categorical_crossentropy',
    #   metrics=['accuracy'])
    #
    # model.fit(x_train, y_train, epochs=5)
    # model.evaluate(x_test, y_test)
    pass

def qr_code(data, filename):
    img = qrcode.make(data)  # генерируем qr-код
    img.save(filename)       # сохраняем img в файл
    print('filename ::: ', filename)
    return filename

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

# class SalesPlr:
#     def __init__(self, amount, quantity):
#         self.amount = float(amount)
#         self.quantity = int(quantity)
#
#     # @staticmethod
#     def get_price(self):
#         return self.amount * self.quantity
#
#     def get_currency_rates(self):
#         print('Спасибо, что выбрали наше решение! =)')

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    print("Файл из blob сохранен в: ", filename, "\n")

    return filename

def create_table():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    # Создаем таблицу
    cursor.execute('CREATE TABLE IF NOT EXISTS bot_sales_plar (id INTEGER PRIMARY KEY, bl_Image BLOB,'
                   ' num_BaseSumRUB NUMERIC, num_BaseSumUSD NUMERIC, num_BaseSumEUR NUMERIC, num_SaleSum NUMERIC,'
                   ' int_quantity INTEGER, str_name TEXT NOT NULL)')
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

def insert_data(id, photo, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, str_name, int_quantity):
    bl_Image = convert_to_binary_data(photo)  # подготовим изображение для вставки в blob-поле

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    #Делаем вставку данных
    cursor.execute('INSERT INTO bot_sales_plar (id, bl_Image, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, str_name, int_quantity) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                   (id, bl_Image, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, str_name, int_quantity))

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

def select_data(id, str_name, num_BaseSum, bl_Image, int_quantity, curr_code):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    select_text = 'SELECT id, str_name, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, bl_Image, int_quantity FROM bot_sales_plar'
    if (id is not None) or\
       (str_name is not None) or\
       (num_BaseSum is not None) or\
       (bl_Image is not None) or\
       (int_quantity is not None):
        select_text = select_text + ' WHERE '
        flg = 0
        if id is not None:
            flg = 1
            select_text = select_text + f'id = {id}'
        if str_name is not None:
            if flg == 1:
                select_text = select_text + ' AND '
            flg = 1
            select_text = select_text + f'str_name = {str_name}'
        if num_BaseSum is not None:
            if flg == 1:
                select_text = select_text + ' AND '
            flg = 1
            if curr_code == 'RUB':
                select_text = select_text + f'num_BaseSumRUB = {num_BaseSum}'
            elif curr_code == 'USD':
                select_text = select_text + f'num_BaseSumUSD = {num_BaseSum}'
            elif curr_code == 'EUR':
                select_text = select_text + f'num_BaseSumUSD = {num_BaseSum}'
        if bl_Image is not None:
            if flg == 1:
                select_text = select_text + ' AND '
            flg = 1
            select_text = select_text + f'bl_Image = {bl_Image}'
        if int_quantity is not None:
            if flg == 1:
                select_text = select_text + ' AND '
            select_text = select_text + f'int_quantity >= {int_quantity}'

    cursor.execute(select_text)  # выполним запрос

    # Сохраняем изменения и закрываем соединение
    results = cursor.fetchall()
    # print('results: ', results)

    name = results[0][5]
    photo_path = 'E:\Games\RSL\VVV\\' + str(name) + ".jpg"
                 #  os.path.join("db_data", name + ".jpg")
    results.append(photo_path)
    # write_to_file(results[0][6], photo_path)

    # print('results: ', results[0][1])
    # for row in results:
    #     print(row)
    cursor.close()
    connection.close()

    return results

def select_all_data(list_proposal):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    select_text = 'SELECT id, str_name, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, bl_Image, int_quantity FROM bot_sales_plar'
    cursor.execute(select_text)  # выполним запрос

    # Сохраняем изменения и закрываем соединение
    results = cursor.fetchall()

    # print('results: ', results[0][1])
    # list_proposal = []
    for row in results:
        list_proposal.append([row[1], row[5], row[6]])
        # print(row[1], ' - ', row[5], ' - ', row[6])

    cursor.close()
    connection.close()

    return list_proposal

class SqLite3_Connection:
    # Создаем подключение к базе данных (файл my_database.db будет создан)
    # def __init__(self, connection, cursor):
    #     self.connection = connection
    #     self.cursor = cursor

    def insert_data(self, connection, cursor):
        pass

    def select_data(self, connection, cursor):
        pass

    def create_table(self): #, connection, cursor):
        pass

if __name__ == '__main__':
    tensor_flow()

    # create_table()

    # insert_data(0, 'E:\Games\RSL\photo_4999.jpg', 4999.0, 49.99, 59.99, 5000.00, "Суперцепочка древних осколков", 1)
    # insert_data(1, 'E:\Games\RSL\photo_5999.jpg', 5999.0, 59.99, 69.99, 6000.00, "Элитный сакральный набор", 2)
    # insert_data(2, 'E:\Games\RSL\photo_7999.jpg', 7999.0, 79.99, 89.99, 8000.00, "Молниеносное предложение камней душ", 1)
    # insert_data(3, 'E:\Games\RSL\photo_9999.jpg', 9999.0, 99.99, 109.99, 10000.00, "Набор-конструктор (мифические шарды)", 3)

    # select_all_data([])
    # qr_code()

    # select_data(None, None, None, None, None)
    # select_data(None, None, 7999.0, None, 5)
    # select_data(None, None, 7999, None, 1, 'RUB')
    pass

# cursor.execute('INSERT INTO bot_sales_plar (id, bl_Image, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, str_name, int_quantity)
# VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (0, bl_Image, 4999.0, 49.99, 59.99, 5000.00, "Набор рубинов", 1))
# cursor.execute('INSERT INTO bot_sales_plar (id, bl_Image, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, str_name, int_quantity)
# VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (1, bl_Image, 5999.0, 59.99, 69.99, 6000.00, "Набор энергии", 2))
# cursor.execute('INSERT INTO bot_sales_plar (id, bl_Image, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, str_name, int_quantity)
# VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (2, bl_Image, 6999.0, 69.99, 79.99, 7000.00, "Набор войдовых шардов", 3))
# cursor.execute('INSERT INTO bot_sales_plar (id, bl_Image, num_BaseSumRUB, num_BaseSumUSD, num_BaseSumEUR, num_SaleSum, str_name, int_quantity)
# VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (3, bl_Image, 7999.0, 79.99, 89.99, 8000.00, "Набор мифических шардов", 5))
