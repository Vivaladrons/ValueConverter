import json
import requests
from config import keys, headers


class APIException(Exception):
    pass


class ValueConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        if amount <= 0:
            raise APIException(f'Не удалось конвертировать отрицательное или нулевое значение {amount}')
        r = requests.get(f"https://api.apilayer.com/fixer/convert?to={base_ticker}&from={quote_ticker}&amount={amount}",
                         headers=headers)
        total_base = json.loads(r.content)['result']
        return total_base
