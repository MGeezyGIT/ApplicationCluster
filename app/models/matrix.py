from pydantic import BaseModel
from typing import List

class Keyword(BaseModel):
    keyword: str

class Chapter(BaseModel):
    title: str
    keywords: List[Keyword]

class Matrix(BaseModel):
    chapters: List[Chapter]
