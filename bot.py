# from exchange import Exchange
import asyncio
from exchange import BitfinexExchange, BitmexExchange, GdaxExchange, KrakenExchange, GeminiExchange
from concurrent.futures import ThreadPoolExecutor
import settings
import signal
import sys
import ws
import time

p = ThreadPoolExecutor(settings.THREAD_COUNT)

def main(argv):
    loop = asyncio.get_event_loop()

    bitfinex = BitfinexExchange('Bitfinex',
                                settings.BITFINEX_API_URL,
                                settings.BITFINEX_CURRENCIES,
                                settings.BITFINEX_CHANNELS)

    bitmex = BitmexExchange('BitMEX',
                            settings.BITMEX_API_URL,
                            settings.BITMEX_CURRENCIES,
                            settings.BITMEX_CHANNELS)

    kraken = KrakenExchange('Kraken',
                            settings.KRAKEN_API_URL,
                            settings.KRAKEN_CURRENCIES)

    gdax = GdaxExchange("GDAX",
                        settings.GDAX_API_URL,
                        settings.GDAX_CURRENCIES)

    print('Adding gdax')
    loop.run_in_executor(p, gdax.connect)
    time.sleep(0.5)

    print('Adding kraken')
    loop.run_in_executor(p, kraken.connect)
    time.sleep(0.5)

    print('Adding bitfinex')
    asyncio.ensure_future(ws.connect(bitfinex))
    time.sleep(0.5)

    print('Adding bitMEX')
    asyncio.ensure_future(ws.connect(bitmex))
    time.sleep(0.5)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()

    # REST API exchanges
    # gdax = GdaxExchange("GDAX",
    #                     settings.GDAX_API_URL,
    #                     settings.GDAX_CURRENCIES)
    # gemini = GeminiExchange('Gemini',
    #                         settings.GEMINI_API_URL,
    #                         settings.GEMINI_CURRENCIES)

    # print('Adding gdax')
    # asyncio.ensure_future(gdax.exchange_coroutine())

    # print('Adding gemini')
    # asyncio.ensure_future(ws.connect(gemini))


if __name__ == "__main__":
    main(sys.argv[1:])
