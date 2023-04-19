from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

# This function takes a user ID and returns the corresponding user object from the database. 
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# This function takes a user's email address and returns the corresponding user object from the database.
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# This function returns a list of user objects from the database, with optional parameters to skip a certain number of records and limit the number of records returned.
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# This function takes a user ID and a user object and updates the corresponding user in the database.
def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    userInstance = db.query(models.User).filter(models.User.id == user_id)

    if not userInstance.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")

    dict_user = dict(user)
    
    userInstance.update(dict_user)
    db.commit()
    return get_user(db=db, user_id=user_id)

# This function takes a user object and creates a new user in the database.
def create_user(db: Session, user: schemas.UserCreate):
    # Create a SQLAlchemy model instance with your data.
    db_user = models.User(email=user.email, name=user.name)
    # add that instance object to your database session.
    db.add(db_user)
    # commit the changes to the database
    db.commit()
    # refresh your instance (so that it contains any new data from the database, like the generated ID).
    db.refresh(db_user)
    return db_user

#  This function takes a user ID and deletes the corresponding user from the database.
def delete_user(db: Session, user_id: int):
    user = get_user(db,user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    
    db.delete(user)
    db.commit()
    return "deleted"


# This function returns a list of book objects from the database, with optional parameters to skip a certain number of records and limit the number of records returned.
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

# This function takes a book ID and returns the corresponding book object from the database.
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

# This function takes a book object and creates a new book in the database.
def add_book(db: Session, book: schemas.BookCreate):
    # Create a SQLAlchemy model instance with your data.
    db_book = models.Book(title = book.title, description = book.description)
    # add that instance object to your database session.
    db.add(db_book)
    # commit the changes to the database
    db.commit()
    # refresh your instance (so that it contains any new data from the database, like the generated ID).
    db.refresh(db_book)
    print(db_book)
    return db_book

# This function assigns a book to a user by updating the owner_id attribute of the book object.
def issue_user_book(db: Session, book_id: int, user_id: int):
    book = get_book(db=db,book_id=book_id)
    user = get_user(user_id=user_id,db=db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {book_id} not found")

    if book.owner_id is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"book id {book_id} is already assigned to an user {user_id}")
    book.owner_id = user_id
    db.commit()
    return f"book id {book_id} is assigned to userid {user_id}"
        
    
# This function takes a book ID and a book object and updates the corresponding book in the database.
def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    bookInstance = db.query(models.Book).filter(models.Book.id == book_id)

    if not bookInstance.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {book_id} not found")

    dict_book = dict(book)
    
    bookInstance.update(dict_book)
    db.commit()
    return get_book(db=db, book_id=book_id)

# This function takes a book ID and deletes the corresponding book from the database.
def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id)

    if not book.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {book_id} not found")

    book.delete()
    db.commit()
    return "deleted"




