#!/usr/bin/python3
"""Test file for File_storage
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestInstantiations(unittest.TestCase):
    """Testing the Instantiation Class"""

    def test_InstanceNoArgument(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_InstanceWithArgument(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_PrivateFilePath(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_PrivateObjectDict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_InitializeStorage(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Testing the Filestorage Methods"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_AllWithArgs(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        bm = BaseModel()
        user = User()
        st = State()
        pl = Place()
        city = City()
        am = Amenity()
        review = Review()
        models.storage.new(bm)
        models.storage.new(user)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(city)
        models.storage.new(am)
        models.storage.new(review)
        self.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn("User." + user.id, models.storage.all().keys())
        self.assertIn(user, models.storage.all().values())
        self.assertIn("State." + st.id, models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn("Place." + pl.id, models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn("City." + city.id, models.storage.all().keys())
        self.assertIn(city, models.storage.all().values())
        self.assertIn("Amenity." + am.id, models.storage.all().keys())
        self.assertIn(am, models.storage.all().values())
        self.assertIn("Review." + review.id, models.storage.all().keys())
        self.assertIn(review, models.storage.all().values())

    def test_newWithArgs(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        city = City()
        am = Amenity()
        review = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(city)
        models.storage.new(am)
        models.storage.new(review)
        models.storage.save()
        save_text = ""

        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("User." + us.id, save_text)
            self.assertIn("State." + st.id, save_text)
            self.assertIn("Place." + pl.id, save_text)
            self.assertIn("City." + city.id, save_text)
            self.assertIn("Amenity." + am.id, save_text)
            self.assertIn("Review." + review.id, save_text)

    def test_saveWthArgs(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        city = City()
        am = Amenity()
        review = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(city)
        models.storage.new(am)
        models.storage.new(review)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)
        self.assertIn("User." + us.id, objs)
        self.assertIn("State." + st.id, objs)
        self.assertIn("Place." + pl.id, objs)
        self.assertIn("City." + city.id, objs)
        self.assertIn("Amenity." + am.id, objs)
        self.assertIn("Review." + review.id, objs)

    def test_reloadWithArgs(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
