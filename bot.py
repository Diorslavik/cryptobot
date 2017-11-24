# from exchange import Exchange
import asyncio
from exchange import YobitExchange, BitfinexExchange
import visualization
import settings
import sys
import ws
import getopt


def main(argv):
    opts, args = getopt.getopt(argv, 'pt')

    for opt, arg in opts:
        if opt == '-p':
            yobit = YobitExchange(settings.YOBIT_API_URL, settings.YOBIT_CURRENCIES)

            loop = asyncio.get_event_loop()

            data = loop.run_until_complete(yobit.exchange_coroutine('depth',
                                                                    sleep_time=1,
                                                                    is_infinite=False))

            visualization.pandas_demo(data)
        elif opt == '-t':
            yobit = YobitExchange(settings.YOBIT_API_URL, settings.YOBIT_CURRENCIES)
            bitfinex = BitfinexExchange(settings.BITFINEX_API_URL, settings.BITFINEX_CURRENCIES)

            loop = asyncio.get_event_loop()

            # asyncio.async(yobit.exchange_coroutine('trades', sleep_time=0.5, limit=1))
            # asyncio.async(yobit.exchange_coroutine('depth', sleep_time=5))
            
            print('Adding bitfinex')
            asyncio.ensure_future(ws.connect(bitfinex))

            try:
                loop.run_forever()
            except KeyboardInterrupt:
                loop.close()

if __name__ == "__main__":
    main(sys.argv[1:])
