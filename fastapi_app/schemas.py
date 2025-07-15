# fastapi_app/schemas.py
from pydantic import BaseModel
from typing import Optional, List

class TopProduct(BaseModel):
    product_name: str
    count: int

class ChannelActivity(BaseModel):
    date: str
    message_count: int

class MessageSearchResult(BaseModel):
    id: int
    message_text: str
    message_date: str
    channel_id: int
