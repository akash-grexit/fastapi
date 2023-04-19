from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# Create SQLAlchemy models from the Base class
# defined as a subclass of the Base class.
class User(Base):
    __tablename__ = "users" # This line specifies the name of the database table that will be created for this model.

    # Create model attributes/columns
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)

    # This line specifies the relationship between the User and Book models. It indicates that a User object can have multiple Book objects associated with it.
    books = relationship("Book", back_populates="owner")


class Book(Base):
    __tablename__ = "books"
    
    # Create model attributes/columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String,index=True)
    
    # This line specifies that the Book table will have an integer column owner_id which is a foreign key referencing the id column of the User table. This column can be nullable and the SET NULL option is used to set the owner_id to NULL when the associated User object is deleted.
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='SET NULL'), nullable=True)

    # This line specifies the relationship between the Book and User models. It indicates that a Book object can be associated with a User object, and if the associated User object is deleted, the owner_id column of the Book table will be set to NULL (this is achieved using the passive_deletes=True parameter).

    owner = relationship("User", back_populates="books", passive_deletes=True)
