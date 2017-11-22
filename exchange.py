# Exchange models here
import requests


class ExchangeBaseClass:

    def __init__(self, api_url, currencies):
        self.api_url = api_url
        self.currencies = currencies

    def __str__(self):
        return self.api_url

    def execute_method(self, method='trades'):
        request_url = self.make_api_url(self.api_url,
                                        method,
                                        currencies=self.currencies)

        r = requests.get(request_url)
        return r.json()

    @staticmethod
    def make_api_url(url, method, currencies, **kwargs):
        pass


class YobitExchange(ExchangeBaseClass):

    def execute_method(self, method='trades', limit=None):
        request_url = self.make_api_url(self.api_url,
                                        method,
                                        currencies=self.currencies,
                                        limit=limit)

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
