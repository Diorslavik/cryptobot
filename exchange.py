# Exchange models here
import asyncio
from orderbook import BitfinexOrder, BitfinexOrderBook
import json
import time
import requests

class ExchangeBaseClass:

    def __init__(self, name, api_url, currencies):
        self.name = name
        self.api_url = api_url
        self.currencies = currencies

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
            print('Message is a set!')
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
                print('Junk data')
        print(self.orderbook.top(self))

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

    @staticmethod
    async def consumer(message):
        print(message)
        return json.loads(message)

    @staticmethod
    async def producer():
        pass

    async def connect_to_channels(self, websocket):
        args = [channel + ':XBTUSD' for channel in self.channels]
        msg = {
            'op': 'subscribe',
            'args': args
        }
        print('Connecting to channels: ' + str(args))
        await websocket.send(json.dumps(msg))

class KrakenExchange(ExchangeBaseClass):

    def __init__(self, name, api_url, currencies):
        super(KrakenExchange, self).__init__(name, api_url, currencies)

    @staticmethod
    def make_api_url(url, method, **kwargs):
        url = url + '/' + method

        if kwargs != {}:
            url += '?'

        kws = ['{}={}'.format(name, value) for name, value in kwargs.items()]

        return url + '&'.join(kws)

    def execute_method(self, method='Depth', currency=None):
        request_url = self.make_api_url(self.api_url,
                                        method,
                                        pair=currency, count=200)
        delay = time.time()
        r = requests.get(request_url)
        delay = time.time() - delay

        r = r.json()
        r["delay"] = delay
        r['timestamp']=time.time()
        r['exchange'] = currency

        return self.json_processing(r)

    async def exchange_coroutine(self, method='Depth', sleep_time=5, is_infinite=True):
        if is_infinite:
            while True:
                for currency in self.currencies:
                    data = self.execute_method(method, currency=currency)
                    print(data)
                await asyncio.sleep(sleep_time)

        else:
            for currency in self.currencies:
                data = self.execute_method(method, currency=currency)

            await asyncio.sleep(sleep_time)
            print(data)

    @staticmethod
    def json_processing(jsn):

        result_row = {}
        result_row['timestamp'] = jsn['timestamp']
        result_row['response_time'] = jsn['delay']
        result_row['exchange'] = jsn['exchange']

        jsn = jsn['result'][list(jsn['result'].keys())[0]]
        jsn['bids'] = [[float(bid[0]), float(bid[1])] for bid in jsn['bids']]
        jsn['asks'] = [[float(ask[0]), float(ask[1])] for ask in jsn['asks']]

        result_row['bid'] = max([bid[0] for bid in jsn['bids']])
        result_row['bid_volume'] = sum([bid[1] for bid in jsn['bids'] if bid[0] == result_row['bid']])

        result_row['ask'] = min([ask[0] for ask in jsn['asks']])
        result_row['ask_volume'] = sum([ask[1] for ask in jsn['asks'] if ask[0] == result_row['ask']])

        return result_row

class GdaxExchange(ExchangeBaseClass):

    def __init__(self, name, api_url, currencies):
        super(GdaxExchange, self).__init__(name, api_url, currencies)
        # self.orderbook = BitfinexOrderBook()

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
                                        level = 3)
        delay = time.time()
        r = requests.get(request_url)
        delay = time.time() - delay

        r = r.json()
        r["delay"]=delay
        r['timestamp']=time.time()
        r['exchange']=currency
        return self.json_processing(r)

    async def exchange_coroutine(self, method='book', sleep_time=5, is_infinite=True):
        if is_infinite:
            while True:
                for currency in self.currencies:
                    data = self.execute_method(method, currency=currency)
                    print(data)
                await asyncio.sleep(sleep_time)

        else:
            for currency in self.currencies:
                data = self.execute_method(method, currency=currency)

            await asyncio.sleep(sleep_time)
            print(data)

    @staticmethod
    def json_processing(jsn):

        jsn['bids'] = [[float(i[0]), float(i[1])] for i in jsn['bids']]
        jsn['asks'] = [[float(i[0]), float(i[1])] for i in jsn['asks']]

        result_row = {}

        result_row['timestamp'] = jsn['timestamp']
        result_row['exchange'] = jsn['exchange']

        result_row['bid'] = max([bid[0] for bid in jsn['bids']])
        result_row['bid_volume'] = sum([bid[1] for bid in jsn['bids'] if bid[0]==result_row['bid']])

        result_row['ask'] = min([ask[0] for ask in jsn['asks']])
        result_row['ask_volume'] = sum([ask[1] for ask in jsn['asks'] if ask[0]==result_row['ask'] ])

        result_row['response_time'] = jsn['delay']

        return result_row