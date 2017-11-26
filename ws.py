import asyncio
import websockets


async def connect(exchange):
    async with websockets.connect(exchange.api_url) as websocket:
        print('Handling: ', exchange)
        consumer_task = asyncio.ensure_future(consumer_handler(exchange, websocket))
        producer_task = asyncio.ensure_future(producer_handler(exchange, websocket))
        await exchange.connect_to_channels(websocket)
        data, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()


async def consumer_handler(exchange, websocket):
    async for message in websocket:
        await exchange.consumer(message)


async def producer_handler(exchange, websocket):
    while True:
        message = await exchange.producer()
        print(message)
        await websocket.send(message)
