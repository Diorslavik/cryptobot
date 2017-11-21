import asyncio


@asyncio.coroutine
def exchange_coroutine(exchange, method='trades'):
    while True:
        yield from asyncio.sleep(1)
        exchange.execute_method(method)
