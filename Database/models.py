from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'Users'

    ID = Column(Integer, primary_key=True, index=True)
    UID = Column(Integer,  nullable=True, unique=True)
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

    ID = Column(Integer,primary_key=True, nullable=False, unique=True)
    ISBN = Column(String, ForeignKey("Titles.ISBN"),nullable=False)

    Title = relationship("Title")


class BorrowBook(Base):
    __tablename__ = 'BorrowedBooks'

    ID = Column(Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    ClientUID = Column(Integer,ForeignKey("Users.UID"),  nullable=False)
    BookID = Column(Integer,ForeignKey("Books.ID"), nullable=False)
    BorrowDate = Column(Date,nullable=False)
    ReturnDate = Column(Date,nullable=True)

    User = relationship("User")
    Book = relationship("Book")
