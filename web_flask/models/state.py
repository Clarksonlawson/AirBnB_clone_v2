#!/usr/bin/python3
"""
This module defines the State class.
"""
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """
    This class defines a State object.
    """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    if environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """
            Getter method to return the list of City objects
            from storage linked to the current State
            """
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

