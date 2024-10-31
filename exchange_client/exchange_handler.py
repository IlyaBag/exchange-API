from typing import Any

import aiohttp


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
            print('Response status code:', resp.status)  # PRINT_DEL
            data = await resp.json()
            print(f'Price {index_name}: {data['result']['index_price']}')  # PRINT_DEL
    return data

async def get_index_price(index_name: str) -> tuple[str, float]:
    """Get ticker and index price of the specified currency."""
    ticker = get_ticker_from_index_name(index_name)

    data = await fetch_data_from_API(index_name)
    price = data['result']['index_price']

    return ticker, price
