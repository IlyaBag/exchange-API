from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import Result, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.schemas import IndexPrice, IndexPriceSave
from database.db import get_db_session
from database.models import IndexPriceModel


router = APIRouter(prefix='/api/v1', tags=['Index price'])


@router.get('/all-data', response_model=list[IndexPrice])
async def get_all_data(
    ticker: Annotated[str, Query(max_length=10)],
    requested_date: Annotated[
        str | None,
        Query(
            description='String in format YYYY-MM-DD',
            regex=r'^20\d{2}-\d{2}-\d{2}$'
        ),
    ] = None,
    session: AsyncSession = Depends(get_db_session),
):
    """Returns a list of all data for the currency. Allows optional filtering of
    data by date."""
    stmt = (select(IndexPriceModel)
            .filter(IndexPriceModel.ticker == ticker.upper()))
    if requested_date:
        date_obj = datetime.fromisoformat(f'{requested_date}T00:00Z')
        stmt = stmt.filter(
            IndexPriceModel.unix_timestamp.between(
                date_obj.timestamp(),
                (date_obj + timedelta(days=1)).timestamp()
            )
        )
    result: Result = await session.execute(stmt)
    return result.scalars().all()


@router.get('/get-last-price', response_model=IndexPrice)
async def get_last_price(
    ticker: Annotated[str, Query(max_length=10)],
    session: AsyncSession = Depends(get_db_session),
):
    """Returns the last saved price of the adjusted currency."""
    stmt = (select(IndexPriceModel)
            .filter(IndexPriceModel.ticker == ticker.upper())
            .order_by(desc(IndexPriceModel.unix_timestamp))
            .limit(1))
    result: Result = await session.execute(stmt)
    last_price = result.scalar()
    return last_price


@router.post('/save-index-price', status_code=status.HTTP_201_CREATED)
async def save_index_price(
    params: IndexPriceSave,
    session: AsyncSession = Depends(get_db_session),
):
    """Save an index price of a currency."""
    price = IndexPriceModel(**params.model_dump())
    session.add(price)
    await session.commit()
    return {'details': 'Created successfully'}
