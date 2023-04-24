import logging

from cards.models import Card, Color
from cards.schemas import CardParseSchema, ColorBaseSchema
from celery import Celery, group
from config import settings
from database import get_db
from scrapper.wilberries import fetch_data


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

url = (
    "amqp://"
    + settings.rabbitmq_default_user
    + ":"
    + settings.rabbitmq_default_pass
    + "@"
    + settings.rabbitmq_host
    + ":"
    + str(settings.rabbitmq_port)
    + "/"
    + settings.rabbitmq_default_vhost
)

celery = Celery("tasks", broker_url=url)


@celery.task
def update_card(nm_id: int):
    logger.info(f"update_card for card {nm_id} called")
    db = next(get_db())
    data = fetch_data(nm_id)
    if not data:
        logger.warning(f"couldn't update card {nm_id}")
        return
    validated_card = CardParseSchema(**data)
    new_card = Card(**validated_card.dict())
    colors_data = data.get("colors")
    for color_data in colors_data:
        validated_color = ColorBaseSchema(**color_data)
        color = db.query(Color).filter_by(name=validated_color.name).first()
        if not color:
            color = Color(**validated_color.dict())
            db.add(color)
        new_card.colors.append(color)
    old_card = db.query(Card).filter(nm_id == nm_id).first()
    for field in Card.__table__.columns:
        field_name = field.name
        if field_name not in ["pk", "nm_id"]:
            new_value = getattr(new_card, field_name)
            old_value = getattr(old_card, field_name)
            if new_value != old_value:
                setattr(old_card, field_name, new_value)
    old_colors = set(old_card.colors)
    new_colors = set(new_card.colors)
    colors_to_remove = old_colors - new_colors
    for color_to_remove in colors_to_remove:
        old_card.colors.remove(color_to_remove)
    colors_to_add = new_colors - old_colors
    for color_to_add in colors_to_add:
        old_card.colors.append(color_to_add)
    try:
        db.commit()
    except Exception as e:
        logger.error(f"couldn't update card {nm_id}, cause of {e}")


@celery.task
def update_all_cards():
    logger.info("update_all_cards called")
    db = next(get_db())
    all_cards = db.query(Card).all()
    task_group = group(update_card.s(card.nm_id) for card in all_cards)
    result = task_group.apply_async()
    while result.parent is not None and not result.parent.ready():
        pass
    update_all_cards.apply_async(countdown=600)


update_all_cards.apply_async()
