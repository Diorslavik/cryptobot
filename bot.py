# from exchange import Exchange
import asyncio
from exchange import YobitExchange
import visualization
import settings
import sys, getopt

def main(argv):
    opts, args = getopt.getopt(argv, 'p')

    for opt, arg in opts:
        if opt == '-p':
            yobit = YobitExchange(settings.YOBIT_API_URL, settings.YOBIT_CURRENCIES)

            loop = asyncio.get_event_loop()

            data = loop.run_until_complete(yobit.exchange_coroutine('depth',
                                                                   sleep_time=1,
                                                                   is_infinite=False))

            visualization.pandas_demo(data)
        else:
            yobit = YobitExchange(settings.YOBIT_API_URL, settings.YOBIT_CURRENCIES)

            loop = asyncio.get_event_loop()

            asyncio.async(yobit.exchange_coroutine('trades', sleep_time=0.5, limit=1))
            asyncio.async(yobit.exchange_coroutine('depth', sleep_time=5))

            try:
                loop.run_forever()
            except KeyboardInterrupt:
                loop.close()

if __name__ == "__main__":
    main(sys.argv[1:])
