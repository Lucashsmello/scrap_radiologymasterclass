# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import Optional


@dataclass
class CaseItem:
    image_urls: list[str]
    images = None
    fig_caption: str
    fig_description: list[str]
    gallery_name1: str
    case_id: str
    gallery_name2: Optional[str] = None
    file_path: Optional[str] = None
