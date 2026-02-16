# This is the class that defines and builds the table in the DB

from unittest.mock import Base

from sqlalchemy import Column, Integer, String


class UserDBModel(Base):
    __tablename__ = "users" # name of the table in the DB

    id = Column(Integer, primary_key=True, index=True) # primary key is a unique identifier for each record in the table. Indexing it allows for faster lookups.
    username = Column(String, index=True, unique = True, nullable=False) # username of the user, indexed for faster search
    email = Column(String, unique=True, index=True, nullable=False) # email of the user, must be unique and indexed for faster search
    password = Column(String, nullable=False) # password of the user, stored as a string (in a real application, this should be hashed for security)