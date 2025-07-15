# fastapi_app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from .database import Base

class Message(Base):
    __tablename__ = "fct_messages"
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, index=True)
    message_text = Column(String)
    message_date = Column(DateTime)
    has_image = Column(Integer)
    message_length = Column(Integer)

class ImageDetection(Base):
    __tablename__ = "fct_image_detections"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("fct_messages.id"))
    detected_object_class = Column(String)
    confidence_score = Column(Float)

class Channel(Base):
    __tablename__ = "dim_channels"
    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String)
