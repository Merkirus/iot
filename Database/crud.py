from . import models, schemas
from sqlalchemy.orm import Session


#-------
#USER
#-------


def create_user(db: Session, user_schema: schemas.UserCreate):
    new_user = models.User(**user_schema.dict())
    db.add(new_user)
    db.commit()

def get_user_uid(db:Session, uid: int):
    return db.query(models.User).filter(models.User.UID==uid).first()

def get_user_email(db:Session, email: str):
    return db.query(models.User).filter(models.User.Email==email).first()

def get_user_phone(db:Session, phone: str):
    return db.query(models.User).filter(models.User.Phone==phone).first()


#-------
#TITLE
#-------

def create_title(db:Session, title_schema:schemas.TitleCreate):
    new_title = models.Title(**title_schema.dict())
    db.add(new_title)
    db.commit()

def get_title_by_title(db:Session, title:str):
    return db.query(models.Title).filter(models.Title.Title==title).first()

def get_title_by_isbn(db:Session, isbn:str):
    return db.query(models.Title).filter(models.Title.ISBN==isbn).first()


#-------
#BOOK
#-------

def create_book(db:Session, book_schema: schemas.BookCreate):
    new_book = models.Book(**book_schema.dict())
    db.add(new_book)
    db.commit()

def get_book_by_id(db:Session, id:int):
    return db.query(models.Book).filter(models.Book.ID==id).first()


#-------
#BORROWED BOOK
#-------

def create_borrowed(db:Session, borrow_schema = schemas.CreateBorrowBook):
    new_borrow = models.BorrowBook(**borrow_schema.dict())
    db.add(new_borrow)
    db.commit()


def get_c_borrow_usr_book(db:Session, clientId:int, bookId:int):
    return db.query(models.BorrowBook).filter(models.BorrowBook.BookId==bookId
                                              and models.BorrowBook.ClientUID==clientId
                                              and models.BorrowBook.ReturnDate==None).first()