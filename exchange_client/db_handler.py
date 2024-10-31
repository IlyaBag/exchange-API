import aiohttp


DB_API_HOST = 'http://127.0.0.1:8000'


async def save_price_to_db(ticker: str, price: float):
    async with aiohttp.ClientSession() as session:
        url = f'{DB_API_HOST}/api/v1/save-index-price'
        payload = {'ticker': ticker, 'price': price}
        async with session.post(url=url, json=payload) as resp:
            resp.raise_for_status()
            print('Response status code:', resp.status)  # PRINT_DEL
