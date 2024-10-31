import asyncio
import time

from db_handler import save_price_to_db
from exchange_handler import get_index_price


INDEX_NAMES = ('btc_usd', 'eth_usd')
POLLING_INTERVAL = 60


async def main() -> None:
    """Receive data from the exchange API in a delayed loop and save it into
    a database."""
    while True:
        start_time = time.time()
        print(f'\n{start_time}')  # PRINT_DEL
        for name in INDEX_NAMES:
            ticker, price = await get_index_price(name)
            await save_price_to_db(ticker, price)
        await asyncio.sleep(POLLING_INTERVAL - (time.time() - start_time))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nClient stopped')
