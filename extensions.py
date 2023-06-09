import requests
import json
from config import headers, keys


class APIException(Exception):
    pass


class Exchanger:
    @staticmethod
    def exchange(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException("Вы попытались перевести одинаковые валюты")

        try:
            quote_key = keys[quote]
        except KeyError:
            raise APIException("Первая валюта введена неверно")

        try:
            base_key = keys[base]
        except KeyError:
            raise APIException("Вторая валюта введена неверно")

        try:
            amount_check = float(amount)
        except ValueError:
            raise APIException("Вместо числа нечитаемый формат")

        r = requests.request("GET",
                            f"https://api.apilayer.com/exchangerates_data/convert?to={base_key}&from={quote_key}&amount={amount_check}",
                            headers=headers)
        return json.loads(r.content)
