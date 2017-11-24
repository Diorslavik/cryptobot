import time


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
            print(bid_volume)
            ask = min([_ask.price for _ask in self.asks])
            ask_volume = abs(sum([_ask.amount for _ask in self.asks if _ask.price == ask]))
            print(ask_volume)

            return OrderBookOutputData(exchange,
                                       bid, bid_volume,
                                       ask, ask_volume,
                                       response_time='')
        else:
            return 'Empty orderbook for ' + exchange.name

    def __repr__(self):
        return 'Bids: ' + str(self.bids) + '\n' + 'Asks: ' + str(self.asks)
