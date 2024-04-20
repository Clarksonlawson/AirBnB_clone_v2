#!/usr/bin/python3
"""Test file for Amenity
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestInstantiationsAmenity(unittest.TestCase):
    """Test for Insttantiations."""

    def test_noArguments(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_instanceInObject(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_publicID(self):
        self.assertEqual(str, type(Amenity().id))

    def test_publicCreateDate(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_PublicUpdateDate(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_publicNameAttribute(self):
        am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", am.__dict__)

    def test_uniqueIDforTwo(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_differentCreateDate(self):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_differentUpdateDate(self):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_stringRep(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        amstr = am.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_UnusedArgs(self):
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_withKWARGS(self):
        """instantiation with kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "345")
        self.assertEqual(am.created_at, dt)
        self.assertEqual(am.updated_at, dt)

    def test_noKWARGS(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)



if __name__ == "__main__":
    unittest.main()
