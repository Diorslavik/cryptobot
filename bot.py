# from exchange import Exchange
import asyncio
from coroutines import exchange_coroutine
from exchange import YobitExchange
import settings

if __name__ == "__main__":
    yobit = YobitExchange(settings.YOBIT_API_URL, settings.YOBIT_CURRENCIES)

    loop = asyncio.get_event_loop()

    asyncio.async(exchange_coroutine(yobit, 'trades', sleep_time=1, limit=1))
    asyncio.async(exchange_coroutine(yobit, 'depth', sleep_time=25))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
