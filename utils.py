import requests

from cfg import API_URL

class Get():
    @staticmethod
    def get_price(base, quote):
        url = f"{API_URL}{base}"
        list_currencies = requests.get(url)

        if list_currencies.status_code != 200:
            return None

        data = list_currencies.json()

        if 'conversion_rates' in data:
            rates = data['conversion_rates']
            if quote in rates:
                return rates[quote]
        return None