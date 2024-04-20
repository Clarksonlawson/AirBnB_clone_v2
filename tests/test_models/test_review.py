#!/usr/bin/python3
"""Review Unit Tests

"""
from time import sleep
from models.review import Review
import os
import models
import unittest
from datetime import datetime



class TestReviewInstance(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_noArgs(self):
        self.assertEqual(Review, type(Review()))

    def test_toObject(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_publicID(self):
        self.assertEqual(str, type(Review().id))

    def test_publicCreateDate(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_publicUpdateDate(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_publicIDAttribute(self):
        review = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review))
        self.assertNotIn("place_id", review.__dict__)

    def test_publicUserID(self):
        review = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review))
        self.assertNotIn("user_id", review.__dict__)

    def test_publicText(self):
        review = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review))
        self.assertNotIn("text", review.__dict__)

    def test_sameIDs(self):
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.id, rv2.id)

    def test_diffCreateDate(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.created_at, rv2.created_at)

    def test_diffUpdateDate(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.updated_at, rv2.updated_at)

    def test_toString(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        rvstr = review.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + dt_repr, rvstr)
        self.assertIn("'updated_at': " + dt_repr, rvstr)

    def test_unusedArgs(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instanceWithKWARGS(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    def test_noKWARGS(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        self.assertLess(first_updated_at, review.updated_at)

    def test_SaveTwo(self):
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        second_updated_at = review.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        review.save()
        self.assertLess(second_updated_at, review.updated_at)

    def test_saveNoArgs(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_updateFiles(self):
        review = Review()
        review.save()
        rvid = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())

if __name__ == "__main__":
    unittest.main()
