# fastapi_app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

def get_top_products(db: Session, limit: int = 10):
    return db.query(
        models.Message.message_text.label("product_name"),
        func.count().label("count")
    ).group_by(models.Message.message_text).order_by(func.count().desc()).limit(limit).all()

def get_channel_activity(db: Session, channel_name: str):
    return db.query(
        func.date(models.Message.message_date).label("date"),
        func.count().label("message_count")
    ).join(models.Channel, models.Message.channel_id == models.Channel.id)\
     .filter(models.Channel.channel_name == channel_name)\
     .group_by(func.date(models.Message.message_date))\
     .order_by(func.date(models.Message.message_date)).all()

def search_messages(db: Session, query: str):
    return db.query(models.Message).filter(models.Message.message_text.ilike(f"%{query}%")).all()
