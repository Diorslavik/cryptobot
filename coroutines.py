import asyncio


@asyncio.coroutine
def exchange_coroutine(exchange, method='trades', sleep_time=1, limit=None):
    while True:
        yield from asyncio.sleep(sleep_time)
        print(exchange.execute_method(method, limit))
