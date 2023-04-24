from database import Base
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship


card_color = Table(
    "card_color",
    Base.metadata,
    Column(
        "cards_id",
        Integer,
        ForeignKey("cards.pk"),
        primary_key=True,
    ),
    Column(
        "colors_id",
        Integer,
        ForeignKey("colors.pk"),
        primary_key=True,
    ),
)


class Color(Base):
    __tablename__ = "colors"
    pk = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    id = Column(Integer, nullable=False)
    cards = relationship("Card", secondary=card_color, back_populates="colors")


class Card(Base):
    __tablename__ = "cards"
    pk = Column(Integer, primary_key=True)
    nm_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    brand_id = Column(Integer, nullable=True)
    site_brand_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=True)
    sale = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    sale_price = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=True)
    feedbacks = Column(Integer, nullable=True)
    colors = relationship(
        "Color",
        secondary=card_color,
        back_populates="cards",
    )
