# Exchange models here
import asyncio
from orderbook import BitfinexOrder, BitfinexOrderBook
import json


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
