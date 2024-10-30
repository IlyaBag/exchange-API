import aiohttp
import asyncio
import time
from typing import Any


INDEX_NAMES = ('btc_usd', 'eth_usd')
POLLING_INTERVAL = 60


def get_ticker_from_index_name(index_name: str) -> str:
    return index_name.split('_')[0].upper()

async def fetch_data_from_API(index_name: str) -> dict[str, Any]:
    """
    Fetch the data with the index price of the specified currency from
    exchange API.

    Expected JSON response:
    {
        "jsonrpc":"2.0",
        "result":{
            "index_price":69417.94,
            "estimated_delivery_price":69417.94
        },
        "usIn":1730142372194405,
        "usOut":1730142372194508,
        "usDiff":103,
        "testnet":true
    }
    """
    async with aiohttp.ClientSession() as session:
        url = 'https://deribit.com/api/v2/public/get_index_price'
        params = {'index_name': index_name}
        async with session.get(url=url, params=params) as resp:
            resp.raise_for_status()
            data = await resp.json()
    return data

async def get_index_price(index_name: str) -> tuple[str, float]:
    """Get ticker and index price of the specified currency."""
    ticker = get_ticker_from_index_name(index_name)

    data = await fetch_data_from_API(index_name)
    price = data['result']['index_price']

    return ticker, price

async def save_price_to_db(ticker: str, price: float):
    async with aiohttp.ClientSession() as session:
        url = 'http://127.0.0.1:8000/api/v1/save-index-price'
        payload = {'ticker': ticker, 'price': price}
        async with session.post(url=url, json=payload) as resp:
            resp.raise_for_status()

async def main() -> None:
    """Receive data from the exchange API in a delayed loop and save it into
    a database."""
    while True:
        start_time = time.time()
        for name in INDEX_NAMES:
            ticker, price = await get_index_price(name)
            await save_price_to_db(ticker, price)
        await asyncio.sleep(POLLING_INTERVAL - (time.time() - start_time))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nClient stopped')
