from . import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import select, and_


#-------
#USER
#-------


def create_user(db: Session, user_schema: schemas.UserCreate):
    new_user = models.User(**user_schema.dict())
    db.add(new_user)
    db.commit()


def get_user_uid(db:Session, uid: int):
    res = db.query(models.User).filter(models.User.UID==uid).first()

    return res

def get_user_email(db:Session, email: str):
    res = db.query(models.User).filter(models.User.Email==email).first()

    return res

def get_user_phone(db:Session, phone: str):
    res = db.query(models.User).filter(models.User.Phone==phone).first()
    return res


#-------
#TITLE
#-------

def create_title(db:Session, title_schema:schemas.TitleCreate):
    new_title = models.Title(**title_schema.dict())
    db.add(new_title)
    db.commit()


def get_title_by_title(db:Session, title:str):
    res = db.query(models.Title).filter(models.Title.Title==title).first()

    return res

def get_title_by_isbn(db:Session, isbn:str):
    res = db.query(models.Title).filter(models.Title.ISBN==isbn).first()

    return res


#-------
#BOOK
#-------

def create_book(db:Session, book_schema: schemas.BookCreate):
    new_book = models.Book(**book_schema.dict())
    db.add(new_book)
    db.commit()


def get_book_by_id(db:Session, id:int):
    res = db.query(models.Book).filter(models.Book.ID==id).first()

    return res


#-------
#BORROWED BOOK
#-------

def create_borrowed(db:Session, borrow_schema = schemas.CreateBorrowBook):
    new_borrow = models.BorrowBook(**borrow_schema.dict())
    db.add(new_borrow)
    db.commit()



def get_c_borrow_usr_book(db:Session, clientId:int, bookId:int):
    res = db.query(models.BorrowBook).filter(models.BorrowBook.BookID==bookId
                                              , models.BorrowBook.ClientUID==clientId
                                              , models.BorrowBook.ReturnDate == None).first()

    return res


def get_borrowed_by_user(db:Session, clientId:int) :
    _list =db.query(models.BorrowBook).filter(models.BorrowBook.ClientUID == clientId
                                           , models.BorrowBook.ReturnDate == None).all()
    db.commit()

    return list(_list)

def save_borrowed(db:Session, borrowed_item: models.BorrowBook):
    print(borrowed_item.ReturnDate.strftime('%d-%m-%Y'))
    db.query(models.BorrowBook).filter(models.BorrowBook.ID==borrowed_item.ID).update({'ReturnDate':borrowed_item.ReturnDate}, synchronize_session = False)
    db.commit()

    

