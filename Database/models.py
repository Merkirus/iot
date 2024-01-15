from sqlite3 import Timestamp

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'Users'

    UID = Column(Integer, primary_key=True, nullable=False, unique=True)
    Name = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    Phone = Column(String, nullable=False, unique=True)
    Email = Column(String, nullable=False, unique=True)
    Password = Column(String, nullable=False)
    Role = Column(String, nullable=False)


class Title(Base):
    __tablename__ = 'Titles'

    ISBN = Column(String,primary_key=True, nullable=False, unique=True)
    Author = Column(String, nullable=False)
    Title = Column(String, nullable=False,unique=True)


class Book(Base):
    __tablename__ = 'Books'

    ID = Column(Integer,primary_key=True, nullable=False,index=True, unique=True)
    ISBN = Column(String, ForeignKey("Titles.ISBN"),nullable=False)

    Title = relationship("Title")


class BorrowBook(Base):
    __tablename__ = 'BorrowedBooks'

    ID = Column(Integer, primary_key=True, nullable=False, unique=True)
    ClientUID = Column(Integer,  nullable=False, unique=True)
    BookId = Column(Integer, nullable=False, unique=True)
    BorrowDate = Column(Date,nullable=False)
    ReturnDate = Column(Date,nullable=True)

    Client = relationship("Client")
    Book = relationship("Book")