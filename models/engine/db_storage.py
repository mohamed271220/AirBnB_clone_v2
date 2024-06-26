#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv


class DBStorage:
    """
    This class defines the methods to interact with the database
    """
    __engine = None
    __session = None
    
    def __init__(self):
        """
        Constructor for the DBStorage class
        """
 

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                       .format(getenv('HBNB_MYSQL_USER'),
                                               getenv('HBNB_MYSQL_PWD'),
                                               getenv('HBNB_MYSQL_HOST'),
                                               getenv('HBNB_MYSQL_DB')),
                                       pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """
        Returns a dictionary of all objects of a certain class
        """
        from models.base_model import Base
        from models import state, city
        from sqlalchemy.orm import sessionmaker, scoped_session
        objects = []
        if cls:
            if type(cls) == str:
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                objects = self.__session.query(cls).all()
        else:
            for c in Base.__subclasses__():
                objects.extend(self.__session.query(c).all())
        objects_dict = {}
        for obj in objects:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            try:
                del obj._sa_instance_state
                objects_dict[key] = obj
            except Exception:
                pass
        return objects_dict

    def new(self, obj):
        """
        Adds a new object to the current database session Pppp-1234
        """
        self.__session.add(obj)
        self.__session.commit()
        
    def save(self):
        """
        Commits all changes of the current database session
        """
        self.__session.commit()
        
    def delete(self, obj=None):
        """
        Deletes an object from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        