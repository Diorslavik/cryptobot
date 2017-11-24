# from exchange import Exchange
import asyncio
from exchange import BitfinexExchange, BitmexExchange
import settings
import sys
import ws


def main(argv):

    bitfinex = BitfinexExchange('Bitfinex',
                                settings.BITFINEX_API_URL,
                                settings.BITFINEX_CURRENCIES,
                                settings.BITFINEX_CHANNELS)

    # bitmex = BitmexExchange('BitMEX',
    #                         settings.BITMEX_API_URL,
    #                         settings.BITMEX_CURRENCIES,
    #                         settings.BITFINEX_CHANNELS)

    loop = asyncio.get_event_loop()

    print('Adding bitfinex')
    asyncio.ensure_future(ws.connect(bitfinex))

    # print('Adding bitMEX')
    # asyncio.ensure_future(ws.connect(bitmex))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()

if __name__ == "__main__":
    main(sys.argv[1:])
