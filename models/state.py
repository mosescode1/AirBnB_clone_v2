#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from os import getenv


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"
    name = Column("name", String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Intilizes states"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
        # id = Column(String(60), primary_key=True, nullable=False)
    else:
        def cities(self):
            from models.city import City
            import models
            temp = {}
            for k, v in models.storage.all(City).items():
                if v.to_dict()["State.id"] == self.id:
                    temp.update({k, v})
            return temp
            # if value.to_dict()["state_id"] == self.id:
