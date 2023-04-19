from pydantic import BaseModel
from typing import List, Optional, Union


# This is the base model for the Book object, which contains the required fields 'title' and 'description'.
class BookBase(BaseModel):
    title: str
    description: Union[str, None] = None


class BookCreate(BookBase):
    pass

# This model extends the BookBase model and adds two additional fields: 'id' and 'owner_id'. The 'id' field is used to uniquely identify a Book object, and 'owner_id' is the id of the User who owns the book. This model also has a nested Config class, which sets the 'orm_mode' flag to True. This tells Pydantic to read data even if it is not in dictionary format, but rather an ORM model or any other arbitrary object with attributes.
class Book(BookBase):
    id: int
    owner_id: Union[int, None] = None 
 
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
    class Config:
        orm_mode = True

# This is the base model for the User object, which contains the required fields 'email' and 'name'.
class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    books: List[Book] = []
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
    class Config:
        orm_mode = True

