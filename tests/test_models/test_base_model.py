#!/usr/bin/python3
"""Base Model Tests from base_models
"""
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
import os
import models
import unittest


class TestBaseModelInstance(unittest.TestCase):
    """Instantiation Test for Base Model."""

    def test_noArgs(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_storedInObject(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_StringID(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_publicCreatedAt(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_publicUpdatedDate(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_twoUniqueIDs(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_diffCreateDate(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_DiffUpdateDate(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_toString(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_usedArgs(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_withKWARGS(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_withoutKWARGS(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_withArgsandKWargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

if __name__ == "__main__":
    unittest.main()
