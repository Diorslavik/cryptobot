import time
import settings

class Order:

    def __init__(self, response):
        pass


class OrderBook:

    def __init__(self, orders=list()):
        self.bids = [order for order in orders if order.amount > 0]
        self.asks = [order for order in orders if order.amount < 0]


class OrderBookOutputData:

    def __init__(self, exchange, bid, bid_volume, ask, ask_volume, response_time):
        self.timestamp = time.time()
        self.exchange = exchange.name
        self.bid = bid
        self.bid_volume = bid_volume
        self.ask = ask
        self.ask_volume = ask_volume
        self.response_time = response_time
        self.filename = settings.CSV_FILE_NAME

    def __str__(self):
        return ';'.join([str(self.timestamp), self.exchange,
                         str(self.bid), str(self.bid_volume),
                         str(self.ask), str(self.ask_volume),
                         str(self.response_time)])

    def orderbook_save(self):
        with open(self.filename, 'a') as file:
            file.write(str(self)+"\n")


class BitfinexOrder(Order):

    def __init__(self, response):
        super(BitfinexOrder, self).__init__(response)
        self.id, self.price, self.amount = response
        self.timestamp = time.time()

    def __repr__(self):
        return 'Order: ' + str(self.id) + ', ' + str(self.price) + ', ' + str(self.amount)


class BitfinexOrderBook(OrderBook):

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
                                       response_time='')
        else:
            return 'Empty orderbook for ' + exchange.name

    def __repr__(self):
        return 'Bids: ' + str(self.bids) + '\n' + 'Asks: ' + str(self.asks)


class BitmexOrder(Order):
    def __init__(self, response, exchange):
        super(BitmexOrder, self).__init__(response)

        self.exchange = exchange
        self.bid = response['bidPrice']
        self.bid_volume = response['bidSize'] / response['bidPrice']
        self.ask = response['askPrice']
        self.ask_volume = response['askSize'] / response['askPrice']
        self.timestamp = time.time()

    def __repr__(self):
        return str(OrderBookOutputData(self.exchange,
                                       self.bid, self.bid_volume,
                                       self.ask, self.ask_volume,
                                       response_time=''))


class KrakenOrderBook(OrderBookOutputData):
    def __init__(self, exchange, orders):
        data = self.orderbook_processing(orders)
        super(KrakenOrderBook, self).__init__(exchange, data['bid'], data['bid_volume'], data['ask'],
                                              data['ask_volume'], data['response_time'])

    @staticmethod
    def orderbook_processing(orders):
        result_row = dict()
        result_row['response_time'] = orders['delay']

        orders = orders['result'][list(orders['result'].keys())[0]]
        orders['bids'] = [[float(bid[0]), float(bid[1])] for bid in orders['bids']]
        orders['asks'] = [[float(ask[0]), float(ask[1])] for ask in orders['asks']]

        result_row['bid'] = max([bid[0] for bid in orders['bids']])
        result_row['bid_volume'] = sum([bid[1] for bid in orders['bids'] if bid[0] == result_row['bid']])

        result_row['ask'] = min([ask[0] for ask in orders['asks']])
        result_row['ask_volume'] = sum([ask[1] for ask in orders['asks'] if ask[0] == result_row['ask']])

        return result_row


class GdaxOrderBook(OrderBookOutputData):
    def __init__(self, exchange, orders):
        data = self.orderbook_processing(orders)
        super(GdaxOrderBook, self).__init__(exchange, data['bid'], data['bid_volume'], data['ask'],
                                            data['ask_volume'], data['response_time'])

    @staticmethod
    def orderbook_processing(orders):
        orders['bids'] = [[float(i[0]), float(i[1])] for i in orders['bids']]
        orders['asks'] = [[float(i[0]), float(i[1])] for i in orders['asks']]

        result_row = dict()

        result_row['bid'] = max([bid[0] for bid in orders['bids']])
        result_row['bid_volume'] = sum([bid[1] for bid in orders['bids'] if bid[0] == result_row['bid']])

        result_row['ask'] = min([ask[0] for ask in orders['asks']])
        result_row['ask_volume'] = sum([ask[1] for ask in orders['asks'] if ask[0] == result_row['ask']])

        result_row['response_time'] = orders['delay']

        return result_row

