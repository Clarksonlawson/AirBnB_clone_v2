#!/usr/bin/python3
"""Defines unittests for models/state.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstance(unittest.TestCase):
    """Testing State Instantiation"""

    def test_zeroArguments(self):
        self.assertEqual(State, type(State()))

    def test_InObjects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_publicID(self):
        self.assertEqual(str, type(State().id))

    def test_publicCreateDate(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_publicUpdateDate(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_publicName(self):
        st = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(st))
        self.assertNotIn("name", st.__dict__)

    def test_twoStatesID(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_DiffCreateDate(self):
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def test_DiffUpdateDate(self):
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    def test_StringRep(self):
        dates = datetime.today()
        dates_repr = repr(dates)
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dates
        stateString = st.__str__()
        self.assertIn("[State] (123456)", stateString)
        self.assertIn("'id': '123456'", stateString)
        self.assertIn("'created_at': " + dates_repr, stateString)
        self.assertIn("'updated_at': " + dates_repr, stateString)

    def test_UnsusedArgs(self):
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def test_withKwargs(self):
        dates = datetime.today()
        dates_iso = dates.isoformat()

        st = State(id="345", created_at=dates_iso, updated_at=dates_iso)
        self.assertEqual(st.id, "345")
        self.assertEqual(st.created_at, dates)
        self.assertEqual(st.updated_at, dates)

    def test_withoutKWARSG(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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

    def test_SaveOne(self):
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        self.assertLess(first_updated_at, st.updated_at)

    def test_saveTwo(self):
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        second_updated_at = st.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        st.save()
        self.assertLess(second_updated_at, st.updated_at)

    def test_withArgs(self):
        st = State()
        with self.assertRaises(TypeError):
            st.save(None)

    def test_UpdatesFiles(self):
        st = State()
        st.save()
        stid = "State." + st.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())

if __name__ == "__main__":
    unittest.main()
