from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from dataBase import Base


class Book (Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    genre: Mapped[str] = mapped_column()
