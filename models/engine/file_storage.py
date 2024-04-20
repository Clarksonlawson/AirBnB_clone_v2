#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class represents an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""

        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with 
        key <obj_class_name>.id"""
      
        FileStorage.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj


    def save(self):
        """method Serialization of __objects to 
        the JSON file __file_path."""

        prevDictionary = FileStorage.__objects

        objectDictionary = {obj: prevDictionary[obj].to_dict() for obj in prevDictionary.keys()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(objectDictionary, file)


    def reload(self):
        """Method Deserialize the JSON file __file_path
          to __objects, if it exists."""
        
        try:
            with open(FileStorage.__file_path) as file:
                objectDictionary = json.load(file)
                for obj in objectDictionary.values():
                    className = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(className)(**obj))
        except FileNotFoundError:
            return
