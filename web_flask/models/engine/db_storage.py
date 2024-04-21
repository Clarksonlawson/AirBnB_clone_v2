#!/usr/bin/python3
"""
This module defines the DBStorage class.
"""
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """
    This class manages storage using SQLAlchemy
    """
    __engine = None
    __session = None

    def __init__(self):
        """Constructor for DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                       .format(
                                           environ['HBNB_MYSQL_USER'],
                                           environ['HBNB_MYSQL_PWD'],
                                           environ['HBNB_MYSQL_HOST'],
                                           environ['HBNB_MYSQL_DB']),
                                       pool_pre_ping=True)

        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects"""
        objs = {}
        if cls:
            for obj in self.__session.query(eval(cls)).all():
                objs[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for clazz in [State, City]:
                for obj in self.__session.query(clazz).all():
                    objs[obj.__class__.__name__ + '.' + obj.id] = obj
        return objs

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and initializes a session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Calls remove() method on the private session attribute"""
        self.__session.close()

