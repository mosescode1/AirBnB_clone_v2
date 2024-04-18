#!/usr/bin/python3
"""Module for the db storage """
import os
from sqlalchemy import MetaData, create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {
    "User": User,
    "Place": Place,
    "City": City,
    "Amenity": Amenity,
    "Review": Review,
    "State": State
}


class DBStorage:
    __engine = None
    __session = None

    def __init__(self) -> None:
        """initiliaztion of enviroment variables"""
        user = os.getenv("HBNB_MYSQL_USER")

        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        testing = os.getenv("HBNB_ENV")

        conn_str = f"mysql+mysqldb://{user}:{password}@{host}/{db}"

        self.__engine = create_engine(conn_str, pool_pre_ping=True)

        if testing == "test":
            metadata = MetaData(bind=DBStorage.__engine)
            all_table = metadata.sorted_tables

            for table in all_table:
                table.drop(self.__engine)

    def all(self, cls=None):
        if cls is None:
            # returns a list so i can concat them together
            # gives Error if i dont do it that way
            object = self.__session.query(
                City).all() + self.__session.query(State).all()
            # .union(
            #     self.__session.query(Place)
            # ).union(
            #     self.__session.query(City)
            # ).union(
            #     self.__session.query(Review)
            # ).union(
            #     self.__session.query(Amenity)
            # ).all()
            return {f"{obj.__class__.__name__}": obj for obj in object}
        else:
            className = classes[cls]
            object = self.__session.query(className).all()
            return {f"{obj.__class__.__name__}": obj for obj in object}

    def new(self, obj):
        """saves the new instance created to database"""
        self.__session.add(obj)

    def save(self):
        """Saves the instance"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete an object if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(bind=self.__engine)

        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    # def close(self):
    #     self.__session.close(self)
