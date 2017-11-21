# from exchange import Exchange
import asyncio
from coroutines import exchange_coroutine
from exchange import ExchangeBaseClass

if __name__ == "__main__":
    exchange1 = ExchangeBaseClass('exchange1', 'lol', 'lsd-coc')
    exchange2 = ExchangeBaseClass('exchange2', 'lal', 'coc-lsd')

    loop = asyncio.get_event_loop()

    asyncio.async(exchange_coroutine(exchange1, 'trades'))
    asyncio.async(exchange_coroutine(exchange2, 'trades'))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
