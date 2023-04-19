from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from application import crud, schemas, models
from  application.database import SessionLocal, engine

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# define API endpoints

# read root
@app.get("/")
def read_root():
    return {"Hello": "World"}

# create user endpoint

@app.post("/users/", response_model=schemas.User, tags=['Users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# read users endpoint
@app.get("/users/", response_model=List[schemas.User], tags=['Users'])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

# read user endpoint
@app.get("/users/{user_id}", response_model=schemas.User, tags=['Users'])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# update user endpoint
@app.put("/users/{user_id}", response_model=schemas.User, tags=['Users'])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db, user=user, user_id=user_id)


# delete user endpoint
@app.delete("/users/{user_id}", tags=['Users'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)

# issue book for user endpoint
@app.post("/users/{user_id}/books/{book_id}", response_model = str, tags=['Users'])
def issue_book_for_user(
    user_id: int, book_id: int, db: Session = Depends(get_db)
):
    return crud.issue_user_book(db=db, user_id=user_id, book_id = book_id)


# read books endpoint
@app.get("/books/", response_model=List[schemas.Book], tags=['Books'])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

# read book endpoint
@app.get("/books/{book_id}", response_model=schemas.Book, tags=['Books'])
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# create book endpoint
@app.post("/books/", response_model=schemas.Book, tags=['Books'])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.add_book(db=db, book=book)


# update book endpoint
@app.put("/books/{book_id}", response_model=schemas.Book, tags=['Books'])
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.update_book(db, book=book, book_id=book_id)


# delete book endpoint
@app.delete("/books/{book_id}", tags=['Books'])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id=book_id)
