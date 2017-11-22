# Exchange models here
import requests
import asyncio
from models import YobitTrading


class ExchangeBaseClass:

    def __init__(self, api_url, currencies):
        self.api_url = api_url
        self.currencies = currencies

    def __str__(self):
        return self.api_url


class YobitExchange(ExchangeBaseClass):

    def execute_method(self, method='trades', limit=None):
        request_url = self.make_api_url(self.api_url,
                                        method,
                                        currencies=self.currencies, limit=limit)
        r = requests.get(request_url)
        return r.json()

    @staticmethod
    def make_api_url(url, method, currencies, **kwargs):
        if kwargs['limit'] is None:
            kwargs.pop('limit')

        uri = url + '/' + method + '/' + '-'.join(currencies)

        if kwargs != {}:
            uri += '?'

        kws = ['{}={}'.format(name, value) for name, value in kwargs.items()]  # args formatting

        return uri + '&'.join(kws)

    async def exchange_coroutine(self, method='trades', sleep_time=1, is_infinite=True, limit=None):
        if is_infinite:
            while True:
                await asyncio.sleep(sleep_time)
                data = self.execute_method(method, limit)
                print(data)

                model = YobitTrading.select()[0]

                history = model.get_history()
                history.append(data)
                model.set_history(history)

                model.save()
        else:
            await asyncio.sleep(sleep_time)
            data = self.execute_method(method, limit)
            return data
