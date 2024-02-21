#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """creates user object and saves it to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """method that takes in arbitrary keyword arguments
        and returns the first row found in the users table
        as filtered by the method’s input arguments"""
        user = self._session.query(User).filter_by(**kwargs).one()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """method that updates the user’s attributes
        as passed in the method’s arguments
        then commit changes to the database"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self._session.commit()
