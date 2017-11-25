# Exchange models here
import asyncio
from orderbook import BitfinexOrder, BitfinexOrderBook, BitmexOrder, KrakenOrderBook, GdaxOrderBook, GeminiOrderBook
import json
import time
import settings
import requests
import utils


class ExchangeBaseClass:

    def __init__(self, name, api_url, currencies):
        self.name = name
        self.api_url = api_url
        self.currencies = currencies
        self.cache = []

    def __str__(self):
        return self.name


class BitfinexExchange(ExchangeBaseClass):

    def __init__(self, name, api_url, currencies, channels):
        super(BitfinexExchange, self).__init__(name, api_url, currencies)
        self.channels = channels
        self.orderbook = BitfinexOrderBook()

    # Some awful parsing Bitfinex response stuff, see bitfinex api
    async def consumer(self, message):
        message = json.loads(message)
        if isinstance(message, dict):
            pass
        elif isinstance(message[1][0], list):
            orders = message[1]
            for _order in orders:
                order = BitfinexOrder(_order)
                self.orderbook.update(order)
        else:
            _order = message[1]
            try:
                order = BitfinexOrder(_order)
                self.orderbook.update(order)
            except ValueError:
                # Junk data
                pass
        top = self.orderbook.top(self)
        print(top)
        try:
            self.cache.append(top)
            if len(self.cache) > settings.WEBSOCKET_EXCHANGE_CACHE_SIZE:
                utils.export_cache(self.cache)
                self.cache = []
        except AttributeError:
            print(top)

    @staticmethod
    async def producer():
        ping = {
            'event': 'ping',
        }
        await asyncio.sleep(1000)
        return json.dumps(ping)

    async def connect_to_channels(self, websocket):
        # for channel in self.channels: TODO fix for multi-channels to work
        msg = {
            'event': 'subscribe',
            'channel': self.channels[0],
            'symbol': 'tBTCUSD',
            'prec': 'R0'
        }
        await websocket.send(json.dumps(msg))
        return


class BitmexExchange(ExchangeBaseClass):

    def __init__(self, name, api_url, currencies, channels):
        super(BitmexExchange, self).__init__(name, api_url, currencies)
        self.channels = channels
        self.orderbook = BitfinexOrderBook()

    async def consumer(self, message):
        message = json.loads(message)
        if 'data' in message:
            order = BitmexOrder(message['data'][0], self).get_output_data()
            print(order)
            self.cache.append(order)
            if len(self.cache) > settings.WEBSOCKET_EXCHANGE_CACHE_SIZE:
                utils.export_cache(self.cache)
                self.cache = []
                
    @staticmethod
    async def producer():
        ping = {
            'event': 'ping',
        }
        await asyncio.sleep(1000)
        return json.dumps(ping)

    async def connect_to_channels(self, websocket):
        args = [channel + ':XBTUSD' for channel in self.channels]
        msg = {
            'op': 'subscribe',
            'args': args
        }
        await websocket.send(json.dumps(msg))
        return


class KrakenExchange(ExchangeBaseClass):

    def __init__(self, name, api_url, currencies):
        super(KrakenExchange, self).__init__(name, api_url, currencies)
        self.orderbook = KrakenOrderBook()

    @staticmethod
    def make_api_url(url, method, **kwargs):
        url = url + '/' + method

        if kwargs != {}:
            url += '?'

        kws = ['{}={}'.format(name, value) for name, value in kwargs.items()]

        return url + '&'.join(kws)

    def execute_method(self, method='Depth', currency=None, count=200):
        request_url = self.make_api_url(self.api_url,
                                        method,
                                        pair=currency, count=count)
        delay = time.time()
        r = requests.get(request_url)
        delay = time.time() - delay
        r = r.json()

        if r['error']:
            return None

        r = r['result'][currency]
        r['response_time'] = delay
        r['delay'] = delay
        r['timestamp'] = time.time()
        r['exchange'] = currency

        return r

    def connect(self, method='Depth', sleep_time=5, is_infinite=True, count=200):
        if is_infinite:
            while True:
                for currency in self.currencies:
                    data = self.execute_method(method, currency=currency, count=count)
                    if not data:
                        # error handler
                        pass
                    self.orderbook.update(data)
                    top = self.orderbook.top(self)
                    print(str(top))
                    self.cache.append(top)
                    if len(self.cache) > settings.REST_API_EXCHANGE_CACHE_SIZE:
                        utils.export_cache(self.cache)
                        self.cache = []
                time.sleep(sleep_time)
        else:
            for currency in self.currencies:
                data = self.execute_method(method, currency=currency)
                self.orderbook.update(data)
                top = self.orderbook.top(self)
                print(str(top))
                self.cache.append(top)
                if len(self.cache) > settings.REST_API_EXCHANGE_CACHE_SIZE:
                    utils.export_cache(self.cache)
                    self.cache = []
            time.sleep(sleep_time)


class GdaxExchange(ExchangeBaseClass):

    def __init__(self, name, api_url, currencies):
        super(GdaxExchange, self).__init__(name, api_url, currencies)
        self.orderbook = GdaxOrderBook()

    @staticmethod
    def make_api_url(url, method, currencies, **kwargs):
        url = url + '/' + currencies + '/' + method

        if kwargs != {}:
            url += '?'

        kws = ['{}={}'.format(name, value) for name, value in kwargs.items()]

        return url + '&'.join(kws)

    def execute_method(self, method='book', currency=""):
        request_url = self.make_api_url(self.api_url,
                                        method,
                                        currency,
                                        level=3)
        delay = time.time()
        r = requests.get(request_url)
        delay = time.time() - delay

        r = r.json()
        r["response_time"] = delay

        return r

    def connect(self, method='book', sleep_time=5, is_infinite=True):
        if is_infinite:
            while True:
                for currency in self.currencies:
                    data = self.execute_method(method, currency=currency)
                    # error handler
                    self.orderbook.update(data)
                    top = self.orderbook.top(self)
                    print(top)
                    self.cache.append(top)
                    if len(self.cache) > settings.REST_API_EXCHANGE_CACHE_SIZE:
                        utils.export_cache(self.cache)
                        self.cache = []
                time.sleep(sleep_time)
        else:
            for currency in self.currencies:
                data = self.execute_method(method, currency=currency)
                self.orderbook.update(data)
                top = self.orderbook.top(self)
                print(top)
                self.cache.append(top)
                if len(self.cache) > settings.REST_API_EXCHANGE_CACHE_SIZE:
                    utils.export_cache(self.cache)
                    self.cache = []
            time.sleep(sleep_time)


class GeminiExchange(ExchangeBaseClass):
    def __init__(self, name, api_url, currencies):
        api_url += '/' + currencies[0]
        super(GeminiExchange, self).__init__(name, api_url, currencies)
        self.orderbook = BitfinexOrder.GeminiOrderBook()

    async def consumer(self, message):
        message = json.loads(message)
        if len(message) == 4:
            self.orderbook.initvalue(self, message['events'])

        elif len(message) == 6:
            self.orderbook.update(self, message['events'])

    @staticmethod
    async def producer():
        ping = {
            'event': 'ping',
        }
        await asyncio.sleep(1000)
        return json.dumps(ping)

        return result_row


class GeminiExchange(ExchangeBaseClass):
    def __init__(self, name, api_url, currencies):
        api_url += '/' + currencies[0]
        super(GeminiExchange, self).__init__(name, api_url, currencies)
        self.orderbook = BitfinexOrder.GeminiOrderBook()

    async def consumer(self, message):
        message = json.loads(message)
        if len(message) == 4:
            self.orderbook.initvalue(self, message['events'])

        elif len(message) == 6:
            self.orderbook.update(self, message['events'])

    @staticmethod
    async def producer():
        ping = {
            'event': 'ping',
        }
        await asyncio.sleep(1000)
        return json.dumps(ping)
    async def connect_to_channels(self, websocket):
        pass
