import time
import settings


class Order:

    def __init__(self, response):
        pass


class OrderBook:

    def __init__(self, orders=list()):
        pass


class OrderBookOutputData:

    def __init__(self, exchange, bid, bid_volume, ask, ask_volume, response_time):
        self.timestamp = time.time()
        self.exchange = exchange.name
        self.bid = bid
        self.bid_volume = bid_volume
        self.ask = ask
        self.ask_volume = ask_volume
        self.response_time = response_time

    def __str__(self):
        return ';'.join([str(self.timestamp), self.exchange,
                         str(self.bid), str(self.bid_volume),
                         str(self.ask), str(self.ask_volume),
                         str(self.response_time)])
        

class BitfinexOrder(Order):

    def __init__(self, response):
        super(BitfinexOrder, self).__init__(response)
        self.id, self.price, self.amount = response
        self.timestamp = time.time()

    def __repr__(self):
        return 'Order: ' + str(self.id) + ', ' + str(self.price) + ', ' + str(self.amount)


class BitfinexOrderBook(OrderBook):
    def __init__(self, orders=list()):
        super(BitfinexOrderBook, self).__init__(self)
        self.bids = [order for order in orders if order.amount > 0]
        self.asks = [order for order in orders if order.amount < 0]

    def __init__(self, orders=list()):
        super(BitfinexOrderBook, self).__init__(self)
        self.bids = [order for order in orders if order.amount > 0]
        self.asks = [order for order in orders if order.amount < 0]

    def update(self, order):
        if order.price == 0:
            if order.amount > 0:
                order_to_remove = [bid for bid in self.bids if bid.id == order.id]
                self.bids.remove(order_to_remove)
            if order.amount < 0:
                order_to_remove = [ask for ask in self.asks if ask.id == order.id]
                self.asks.remove(order_to_remove)
        elif order.amount > 0:
            self.bids.append(order)
        elif order.amount < 0:
            self.asks.append(order)

    def top(self, exchange):
        if self.bids and self.asks:
            bid = max([_bid.price for _bid in self.bids])
            bid_volume = abs(sum([_bid.amount for _bid in self.bids if _bid.price == bid]))
            ask = min([_ask.price for _ask in self.asks])
            ask_volume = abs(sum([_ask.amount for _ask in self.asks if _ask.price == ask]))

            return OrderBookOutputData(exchange,
                                       bid, bid_volume,
                                       ask, ask_volume,
                                       response_time=-1)
        else:
            return 'Empty orderbook for ' + exchange.name

    def __repr__(self):
        return 'Bids: ' + str(self.bids) + '\n' + 'Asks: ' + str(self.asks)


class GeminiOrderBook:

    asks = dict()
    bids = dict()
    ask = float()
    bid = float()
    ask_volume = float()
    bid_volume = float()
    timestamp = int()

    def initvalue(self, exchange, orders=list()):
        for order in orders:
            if order['side'] == 'bid':
                self.bids[float(order['price'])] = float(order['remaining'])
            elif order['side'] == 'ask':
                self.asks[float(order['price'])] = float(order['remaining'])
        print(self.top(exchange))

    def update(self, exchange, order):
        order = order[0]
        if 'side' in order:
            if order['side'] == 'bid':
                if order['price'] in self.bids:
                    self.bids[order['price']] += float(order['delta'])
                    if float(order['price']) > self.bid:
                        print(self.top(exchange))

            elif order['side'] == 'ask':
                if order['price'] in self.asks:
                    self.asks[order['price']] += float(order['delta'])
                    if float(order['price']) < self.ask:
                        print(self.top(exchange))

            if self.ask_volume == 0 or self.bid_volume == 0:
                print(self.top(exchange))

    def top(self, exchange):
        self.bid = max(self.bids.keys())
        self.ask = min(self.asks.keys())
        self.ask_volume = self.asks[self.ask]
        self.bid_volume = self.bids[self.bid]

        return OrderBookOutputData(exchange,
                                   self.bid, self.bid_volume,
                                   self.ask, self.ask_volume,
                                   response_time='')


class BitmexOrder(Order):
    def __init__(self, response, exchange):
        super(BitmexOrder, self).__init__(response)

        self.exchange = exchange
        self.bid = response['bidPrice']
        self.bid_volume = response['bidSize'] / response['bidPrice']
        self.ask = response['askPrice']
        self.ask_volume = response['askSize'] / response['askPrice']
        self.timestamp = time.time()

    def get_output_data(self):
        return OrderBookOutputData(self.exchange,
                                   self.bid, self.bid_volume,
                                   self.ask, self.ask_volume,
                                   response_time=-1)


class KrakenOrderBook(OrderBook):
    def __init__(self):
        super(KrakenOrderBook, self).__init__()
        self.bids = []
        self.asks = []
        self.response_time = -1

    def top(self, exchange):
        bid = max([bid[0] for bid in self.bids])
        bid_volume = sum([_bid[1] for _bid in self.bids if _bid[0] == bid])

        ask = min([ask[0] for ask in self.asks])
        ask_volume = sum([_ask[1] for _ask in self.asks if _ask[0] == ask])

        return OrderBookOutputData(exchange, bid, bid_volume, ask, ask_volume, self.response_time)

    def update(self, orders):
        self.bids = [[float(bid[0]), float(bid[1])] for bid in orders['bids']]
        self.asks = [[float(ask[0]), float(ask[1])] for ask in orders['asks']]
        self.response_time = orders['response_time']


class GdaxOrderBook(OrderBook):
    def __init__(self):
        super(GdaxOrderBook, self).__init__()
        self.bids = []
        self.asks = []
        self.response_time = -1

    def top(self, exchange):
        bid = max([bid[0] for bid in self.bids])
        bid_volume = sum([_bid[1] for _bid in self.bids if _bid[0] == bid])

        ask = min([ask[0] for ask in self.asks])
        ask_volume = sum([_ask[1] for _ask in self.asks if _ask[0] == ask])

        return OrderBookOutputData(exchange, bid, bid_volume, ask, ask_volume, self.response_time)

    def update(self, orders):
        self.bids = [[float(bid[0]), float(bid[1])] for bid in orders['bids']]
        self.asks = [[float(ask[0]), float(ask[1])] for ask in orders['asks']]
        self.response_time = orders['response_time']



"""
EXAMPLE CLASS
"""


# Данный класс представляет отдельный order биржи, для более удобного использования внутри программы
# У данного класса есть те же поля, что у ордера на данной бирже
class ExchangeOrder(Order):

    def __init__(self, response, exchange):
        super(ExchangeOrder, self).__init__(response)

        self.name = exchange.name

        # response parsing #
        # как пример #
        self.bid = response['bidPrice']
        self.bid_volume = response['bidSize'] / response['bidPrice']
        self.ask = response['askPrice']
        self.ask_volume = response['askSize'] / response['askPrice']
        self.timestamp = time.time()

    def __repr__(self):
        pass


# Данный класс представляет ордер бук биржи, то есть набор bids и asks
# bids, asks - списки ExchangeOrder'ов
# Пока он не обязателен, нужен только для того, чтобы хранить целый orderbook
class ExchangeOrderBook(OrderBook):

    def update(self, order):
        # Здесь проходит добавление объекта ExchangeOrder в bids или в asks
        pass

    def top(self, exchange):
        # Метод для получение верхушки ордербука
        # return OutputOrderBookData obj
        pass

    def __repr__(self):
        pass
