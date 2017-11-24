# cryptobot
Cryptobot skeleton

## Dependencies
1. python 3.6+
2. aiohttp - async http client-server
3. pandas - data analysis
4. peewee - ORM
6. requests

### Installation
```
pip install aiohttp pandas peewee requests
```

### Executing
```
python bot.py
```

# Adding exchange
## REST API exchange
#### X is an exchange name (Bitfinex, Yobit)
1. Add X_API_URL and X_CURRENCIES to file named settings.py (i.e. YOBIT_API_URL, YOBIT_CURRENCIES)
2. Create class XExchange inherited from ExchangeBaseClass (i.e. YobitExchange(ExchangeBaseClass))
3. Each ExchangeClass should have 3 methods:
make_api_url(url, method, **kwargs);
execute_method(self, method, currency);
exchange_coroutine(self, method, sleep_time, if_infinite)
* We should choose better name for function exchange_coroutine
4. Create object of exchange X in bot.py => X_obj
5. Add 2 lines of code to bot.py:
```
print('Adding X')
asyncio.ensure_future(ws.connect(X_obj))
```
6. Run it!
```
python bot.py
```
## Websocket exchange
#### X is an exchange name (Bitfinex, Yobit)
1. Add X_API_URL, X_CURRENCIES and X_CHANNELS to file named settings.py
2. Similar to REST API exchange
3. Each ExchangeClass should have consumer, producer and connect_to_channels(self, websocket) methods
4. Steps 4-6 are similar to REST API exchange