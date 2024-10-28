import asyncio
import aiohttp


INDEX_NAMES = ('btc_usd', 'eth_usd')


async def get_index_price(index_name):
    """
    Fetch the index price of the specified currency.

    Estimated JSON response:
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
        url = 'https://test.deribit.com/api/v2/public/get_index_price'
        params = {'index_name': index_name}
        async with session.get(url=url, params=params) as resp:
            print('Response status code:', resp.status)
            text = await resp.json()
            print(f'Price {index_name}: {text['result']['index_price']}')

async def main():
    for name in INDEX_NAMES:
        await get_index_price(name)


if __name__ == '__main__':
    asyncio.run(main())
