from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Date

class UserBase(BaseModel):
    UID: int
    Name: str
    LastName: str
    Phone: str
    Email: str
    Password: str
    Role: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    class Config:
        orm_mode = True

class TitleBase(BaseModel):
    ISBN: str
    Author:str
    Title:str


class TitleCreate(TitleBase):
    pass


class Title(TitleBase):
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    pass


class BookCreate(BookBase):
    ISBN: str


class Book(BookBase):
    ID: int
    title: Title
    class Config:
        orm_mode = True


class BorrowBookBase(BaseModel):
    BorrowDate: datetime


class CreateBorrowBook(BorrowBookBase):
    ClientUID: int
    BookId: int


class BorrowBook(BorrowBookBase):
    ID:int
    BookId: int
    ClientUID: int
    class Config:
        orm_mode = True