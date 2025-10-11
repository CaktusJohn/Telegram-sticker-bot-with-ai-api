'''
This file contains custom Pydantic models to override or supplement aiogram's default models.
'''
from typing import Optional, List
from aiogram.types import TelegramObject, Sticker, PhotoSize


class CustomStickerSet(TelegramObject):
    """
    This class is a lenient version of aiogram.types.StickerSet.
    It makes `is_animated` and `is_video` fields optional to prevent ValidationErrors
    when the Telegram API response for a StickerSet doesn't include them.
    """
    name: str
    title: str
    sticker_type: str
    stickers: List[Sticker]

    # These fields are not always present in the StickerSet object itself.
    is_animated: Optional[bool] = None
    is_video: Optional[bool] = None
    contains_masks: Optional[bool] = None # Making it optional for safety
    thumbnail: Optional[PhotoSize] = None
