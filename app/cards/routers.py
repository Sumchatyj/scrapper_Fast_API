from typing import List

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from scrapper.wilberries import fetch_data
from sqlalchemy.orm import Session

from .models import Card, Color
from .schemas import CardParseSchema, CardSchema, ColorBaseSchema


router = APIRouter(
    prefix="/cards",
    tags=["cards"],
)


@router.put(
    "/{nm_id}", response_model=CardSchema, status_code=status.HTTP_201_CREATED
)
async def put_card(
    nm_id: int, response: Response, db: Session = Depends(get_db)
):
    card_in_db = db.query(Card).filter_by(nm_id=nm_id).first()
    if card_in_db:
        response.status_code = status.HTTP_200_OK
        return card_in_db
    data = fetch_data(nm_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    validated_card = CardParseSchema(**data)
    card = Card(**validated_card.dict())
    db.add(card)
    colors_data = data.get("colors")
    for color_data in colors_data:
        validated_color = ColorBaseSchema(**color_data)
        color = db.query(Color).filter_by(name=validated_color.name).first()
        if not color:
            color = Color(**validated_color.dict())
            db.add(color)
        card.colors.append(color)
    db.commit()
    db.refresh(card)
    return card


@router.get("/{nm_id}", response_model=CardSchema)
async def get_card(nm_id: int, db: Session = Depends(get_db)):
    card_in_db = db.query(Card).filter_by(nm_id=nm_id).first()
    if not card_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return card_in_db


@router.get("/", response_model=List[CardSchema])
async def get_all_cards(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1
):
    skip = (page - 1) * limit
    cards_in_db = db.query(Card).limit(limit).offset(skip).all()
    if not cards_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return cards_in_db


@router.delete("/{nm_id}", status_code=204)
async def dlete_card(nm_id: int, db: Session = Depends(get_db)):
    card_in_db = db.query(Card).filter_by(nm_id=nm_id).first()
    if not card_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    db.delete(card_in_db)
    db.commit()
