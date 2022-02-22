import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Невозможно сконвертировать одинаковые валюты: {quote}')

        try:
            keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        try:
            keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        #API и логика обраьботки получаемых из него данных были изменены так, чтобы можно было всю необходимую
        #информацию получать, имея бесплатный доступ (на нем доступно только получение курса валют по отношению к евро,
        #т.е. "base" - это всегда евро, другую валюту выбрать в качестве "base" нельзя).

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=30263c7821bcc6630e9bbc336d353054')
        base_c = json.loads(r.content)['rates'][keys[base]]
        quote_c = json.loads(r.content)['rates'][keys[quote]]
        total_quote = quote_c / base_c * amount

        return total_quote