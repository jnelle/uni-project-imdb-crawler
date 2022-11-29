from pydantic import BaseModel


class Review(BaseModel):
    review_title: str
    rating: int
    review: str
    url: str
    date: str
    helpfulness: str
    author: str
    id: str
    name: str
    year: int
