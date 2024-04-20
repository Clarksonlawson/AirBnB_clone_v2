#!/usr/bin/python3
"""Tests for the User Class.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestInstantiation(unittest.TestCase):
    """Testing the instantiation of the User class"""

    def test_NoArgument(self):
        self.assertEqual(User, type(User()))

    def test_InstanceInObject(self):
        self.assertIn(User(), models.storage.all().values())

    def test_IDIsPublic(self):
        self.assertEqual(str, type(User().id))

    def test_CreatedAt(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_UpdatedAt(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_EmailPublic(self):
        self.assertEqual(str, type(User.email))

    def test_PasswordIsPublic(self):
        self.assertEqual(str, type(User.password))

    def test_FirstNameIsPublic(self):
        self.assertEqual(str, type(User.first_name))

    def test_LastNameIsPublic(self):
        self.assertEqual(str, type(User.last_name))

    def test_TwoUSerSameID(self):
        User1 = User()
        User2 = User()
        self.assertNotEqual(User1.id, User2.id)

    def test_DifferentCreateTime(self):
        User1 = User()
        sleep(0.05)
        User2 = User()
        self.assertLess(User1.created_at, User2.created_at)

    def test_DifferentUpdateTime(self):
        User1 = User()
        sleep(0.05)
        User2 = User()
        self.assertLess(User1.updated_at, User2.updated_at)

    def test_StringRep(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "67890"
        user.created_at = user.updated_at = dt
        userString = user.__str__()
        self.assertIn("[User] (67890)", userString)
        self.assertIn("'id': '67890'", userString)
        self.assertIn("'created_at': " + dt_repr, userString)
        self.assertIn("'updated_at': " + dt_repr, userString)

    def test_UnsuedArgument(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiationWithKwargs(self):
        dates = datetime.today()
        dt_iso = dates.isoformat()
        user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dates)
        self.assertEqual(user.updated_at, dates)

    def test_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save method of the  class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_OneSave(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def test_twoSaves(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        second_updated_at = us.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

    def test_withArguments(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def test_UpdateFiles(self):
        user = User()
        user.save()
        usid = "User." + user.id
        with open("file.json", "r") as file:
            self.assertIn(usid, file.read())


# class TestUser_to_dict(unittest.TestCase):
#     """Unittests for testing to_dict method of the User class."""

#     def test_to_dict_type(self):
#         self.assertTrue(dict, type(User().to_dict()))

#     def test_to_dict_contains_correct_keys(self):
#         us = User()
#         self.assertIn("id", us.to_dict())
#         self.assertIn("created_at", us.to_dict())
#         self.assertIn("updated_at", us.to_dict())
#         self.assertIn("__class__", us.to_dict())

#     def test_to_dict_contains_added_attributes(self):
#         us = User()
#         us.middle_name = "Holberton"
#         us.my_number = 98
#         self.assertEqual("Holberton", us.middle_name)
#         self.assertIn("my_number", us.to_dict())

#     def test_to_dict_datetime_attributes_are_strs(self):
#         us = User()
#         us_dict = us.to_dict()
#         self.assertEqual(str, type(us_dict["id"]))
#         self.assertEqual(str, type(us_dict["created_at"]))
#         self.assertEqual(str, type(us_dict["updated_at"]))

#     def test_to_dict_output(self):
#         dt = datetime.today()
#         us = User()
#         us.id = "123456"
#         us.created_at = us.updated_at = dt
#         tdict = {
#             'id': '123456',
#             '__class__': 'User',
#             'created_at': dt.isoformat(),
#             'updated_at': dt.isoformat(),
#         }
#         self.assertDictEqual(us.to_dict(), tdict)

#     def test_contrast_to_dict_dunder_dict(self):
#         us = User()
#         self.assertNotEqual(us.to_dict(), us.__dict__)

#     def test_to_dict_with_arg(self):
#         us = User()
#         with self.assertRaises(TypeError):
#             us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
