# from exchange import Exchange
import asyncio
from exchange import BitfinexExchange, BitmexExchange, GdaxExchange, KrakenExchange, GemeniExchange
import settings
import sys
import ws


def main(argv):

    """
        Socket exchanges
    """
    bitfinex = BitfinexExchange('Bitfinex',
                                settings.BITFINEX_API_URL,
                                settings.BITFINEX_CURRENCIES,
                                settings.BITFINEX_CHANNELS)

    bitmex = BitmexExchange('BitMEX',
                            settings.BITMEX_API_URL,
                            settings.BITMEX_CURRENCIES,
                            settings.BITMEX_CHANNELS)

    """
        REST API exchanges
    """

    gdax = GdaxExchange("GDAX",
                        settings.GDAX_API_URL,
                        settings.GDAX_CURRENCIES)

    kraken = KrakenExchange("Kraken",
                            settings.KRAKEN_API_URL,
                            settings.KRAKEN_CURRENCIES)

    gemini = exchange.GemeniExchange('Gemini',
                                     settings.GEMINI_API_URL,
                                     settings.GEMINI_CURRENCIES)


    # bitmex = BitmexExchange('BitMEX',
    #                         settings.BITMEX_API_URL,
    #                         settings.BITMEX_CURRENCIES,
    #                         settings.BITFINEX_CHANNELS)

    loop = asyncio.get_event_loop()

    print('Adding bitfinex')
    asyncio.ensure_future(ws.connect(bitfinex))

    print('Adding bitMEX')
    asyncio.ensure_future(ws.connect(bitmex))

    # print('Adding kraken')
    # asyncio.ensure_future(kraken.exchange_coroutine())

    # print('Adding gdax')
    # asyncio.ensure_future(gdax.exchange_coroutine())

    print('Adding gemeni')
    asyncio.ensure_future(ws.connect(gemini))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


if __name__ == "__main__":
    main(sys.argv[1:])
