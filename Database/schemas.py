from datetime import datetime, date

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
    id:int
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
    ISBN: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    ID: int
    title: Title
    class Config:
        orm_mode = True


class BorrowBookBase(BaseModel):
    BorrowDate: date
    ClientUID: int
    BookID: int


class CreateBorrowBook(BorrowBookBase):
    ReturnDate: date = None
    pass


class BorrowBook(BorrowBookBase):
    ID:int
    book: Book
    client: User
    class Config:
        orm_mode = True