from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class IndexPriceModel(Base):
    __tablename__ = 'index_price'

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10))
    price: Mapped[float]
    unix_timestamp: Mapped[float] = mapped_column(
        server_default=text("extract(epoch from now())"),
    )

    def __str__(self):
        return f'<{self.__class__.__name__}({self.id}), ticker:{self.ticker \
               }, price:{self.price}>'
