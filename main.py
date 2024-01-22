import datetime

from Database import models, database, crud, schemas

models.Base.metadata.create_all(bind=database.engine)




if __name__ == '__main__':
    # crud.create_user(database.SessionLocal(), schemas.UserCreate(
    #     UID=1,
    #     Name='Jan',
    #     LastName='Kowalski',
    #     Phone='123456789',
    #     Email='email',
    #     Password='password',
    #     Role='USER'
    #
    # ))
    crud.create_borrowed(database.SessionLocal(), schemas.CreateBorrowBook(
        ClientUID = 47364736,
        BookID = 5,
        BorrowDate=datetime.date.today()
    ))