#!/usr/bin/python3
"""Class Defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent an city amenity.

    Attributes:
        name (str): The name of the amenity.
    """

    name = ""
