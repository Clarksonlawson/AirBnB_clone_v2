#!/usr/bin/python3
"""
This module defines the FileStorage class.
"""
import json
from models.base_model import BaseModel


class FileStorage:
    """
    This class serializes instances to a JSON file and deserializes
    JSON file to instances.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        with open(self.__file_path, 'w') as f:
            json.dump({key: obj.to_dict() for key, obj in self.__objects.items()}, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                objs = json.load(f)
                self.__objects = {key: BaseModel(**value) for key, value in objs.items()}
        except FileNotFoundError:
            pass

    def close(self):
        """Calls reload method for deserializing the JSON file to objects"""
        self.reload()

