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
    ID: int



class BookCreate(BookBase):
    ISBN: str


class Book(BookBase):
    title: Title
    class Config:
        orm_mode = True


class BorrowBookBase(BaseModel):
    ID:int
    BorrowDate: datetime


class CreateBorrowBook(BorrowBookBase):
    ClientUUID: int
    BookID: int


class BorrowBook(BorrowBookBase):
    book: Book
    client: User
    class Config:
        orm_mode = True