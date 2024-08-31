TOKEN = '5957782602:AAEq8reL8N957GbRfGsqYgv-Kk6p5Ys1UC0'
API_KEY = 'your_apikey_here'
list_proposal = []

# value[2] используется для чат бота - валюта в родительном падеже
currency_dict = {'RUB': ['Российский рубль', 'рубль', 'рублей', 'Russian Ruble'],
                 'USD': ['Доллары сша', 'доллар', 'долларов', 'доллары', 'баксы', 'баксов', 'us dollar', 'US Dollar'],
                 'EUR': ['Евро', 'евро', 'евро', 'Euro'],
                 }
rate_dict = {'RUB-USD': 100, 'RUB-EUR': 200}