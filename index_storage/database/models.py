from datetime import datetime

from sqlalchemy import TIMESTAMP, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    )


class IndexPriceModel(Base):
    __tablename__ = 'index_price'

    ticker: Mapped[str] = mapped_column(String(10))
    price: Mapped[float]

    def __str__(self):
        return f'<{self.__class__.__name__}({self.id}), ticker:{self.ticker \
               }, price:{self.price}>'
