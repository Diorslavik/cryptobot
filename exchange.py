# Exchange models here


class ExchangeBaseClass:

    def __init__(self, name, api_url, currencies):
        self.name = name
        self.api_url = api_url
        self.currencies = currencies

    def __str__(self):
        return self.name

    def execute_method(self, method='trades'):
        currencies = '-'.join(self.currencies)
        request_url = self.api_url + '/' + method + '/' + currencies
        print(request_url)
