#!/usr/bin/python3
"""Test Class to define the Console.py Tests.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestPrompt(unittest.TestCase):
    """Tests for the Prompts"""

    def test_prompt(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyLine(self):
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", out.getvalue().strip())


class TestHelpCommands(unittest.TestCase):
    """Test for the Help Commands"""

    def test_QuitHelp(self):
        outText = "Quit command to exit the program."

        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(outText, out.getvalue().strip())

    def test_helpCreate(self):
        outText = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(outText, out.getvalue().strip())

    def test_EOFHelp(self):
        outtext = "EOF signal to exit the program."

        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(outtext, out.getvalue().strip())

    def test_showHelp(self):
        outText = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(outText, out.getvalue().strip())

    def test_DestroyHelp(self):
        outText = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(outText, out.getvalue().strip())

    def test_allHelp(self):
        outText = ("Usage: all or all <class> or <class>.all()\n        "
             "Display string representations of all instances of a given class"
             ".\n        If no class is specified, displays all instantiated "
             "objects.")
        
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(outText, out.getvalue().strip())

    def test_CountHelp(self):
        outText = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(outText, out.getvalue().strip())

    def test_UpdateHelp(self):
        outText = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
             "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
             ">) or\n       <class>.update(<id>, <dictionary>)\n        "
             "Update a class instance of a given id by adding or updating\n   "
             "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(outText, out.getvalue().strip())

    def test_Help(self):
        outText = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(outText, out.getvalue().strip())


class TestExitCommand(unittest.TestCase):
    """Testing the Exit command"""

    def test_Quit(self):
        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF(self):
        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestCreateCommand(unittest.TestCase):
    """Test for the create Command"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_CreateMissingClass(self):
        Ans = "** class name missing **"

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(Ans, outputText.getvalue().strip())

    def test_CreateInvalidClass(self):
        Ans = "** class doesn't exist **"

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(Ans, outputText.getvalue().strip())

    def test_CreateInvalidSyntax(self):
        Ans = "*** Unknown syntax: MyModel.create()"

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(Ans, outputText.getvalue().strip())

        Ans = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(Ans, outputText.getvalue().strip())

    def test_CreateObject(self):
        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(outputText.getvalue().strip()))
            testKey = "BaseModel.{}".format(outputText.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(outputText.getvalue().strip()))
            testKey = "User.{}".format(outputText.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(outputText.getvalue().strip()))
            testKey = "State.{}".format(outputText.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(outputText.getvalue().strip()))
            testKey = "City.{}".format(outputText.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(outputText.getvalue().strip()))
            testKey = "Amenity.{}".format(outputText.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(outputText.getvalue().strip()))
            testKey = "Place.{}".format(outputText.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

        with patch("sys.stdout", new=StringIO()) as outputText:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(outputText.getvalue().strip()))
            testKey = "Review.{}".format(outputText.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


if __name__ == "__main__":
    unittest.main()
