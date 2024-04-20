#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def RegexParser(arg):
    braces = re.search(r"\{(.*?)\}", arg)
    parenthesis = re.search(r"\[(.*?)\]", arg)

    if braces is None:
        if parenthesis is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:parenthesis.span()[0]])
            auth = [i.strip(",") for i in lexer]
            auth.append(parenthesis.group())
            return auth
    else:
        lexer = split(arg[:braces.span()[0]])
        auth = [i.strip(",") for i in lexer]
        auth.append(braces.group())
        return auth


class HBNBCommand(cmd.Cmd):
    """Class Defines the HBNBargsCommand interpreter.

    Attributes:
        prompt (str): The argsCommand prompt.
    """

    prompt = "(hbnb) "
    
    __HBNBClasses = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Class does nothing after receiving promp"""
        pass

    def default(self, arg):
        """Invalid Input triggers this default behaviour"""

        argumentDictionary = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

        regexMatch = re.search(r"\.", arg)

        if regexMatch is not None:
            argument1 = [arg[:regexMatch.span()[0]], arg[regexMatch.span()[1]:]]
            regexMatch = re.search(r"\((.*?)\)", argument1[1])
            if regexMatch is not None:
                argsCommand = [argument1[1][:regexMatch.span()[0]], regexMatch.group()[1:-1]]

                if argsCommand[0] in argumentDictionary.keys():
                    call = "{} {}".format(argument1[0], argsCommand[1])
                    return argumentDictionary[argsCommand[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False
    
    def do_quit(self, arg):
        """Command that exits the program"""

        return True
    
    def do_EOF(self, arg):
        """This command signals the exit command"""
        print("")
        return True
    
    def do_create(self, argument):
        """The Method
        Create a new class instance and print its id.
        """
        argument1 = RegexParser(argument)
        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__HBNBClasses:
            print("** class doesn't exist **")
        else:
            print(eval(argument1[0])().id)
            storage.save()

    
    def do_show(self, argument):
        """This Method
        shows the string representation of an instance of a given id.
        """
        argument1 = RegexParser(argument)
        objectDictionary = storage.all()

        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__HBNBClasses:
            print("** class doesn't exist **")
        elif len(argument1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argument1[0], argument1[1]) not in objectDictionary:
            print("** no instance found **")
        else:
            print(objectDictionary["{}.{}".format(argument1[0], argument1[1])])

    def do_destroy(self, argument):
        """The Method
        Delete a class instance of a given id."""

        argument1 = RegexParser(argument)
        objectDictionary = storage.all()

        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__HBNBClasses:
            print("** class doesn't exist **")
        elif len(argument1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argument1[0], argument1[1]) not in objectDictionary.keys():
            print("** no instance found **")
        else:
            del objectDictionary["{}.{}".format(argument1[0], argument1[1])]
            storage.save()

    def do_all(self, argument):
        """The Method
        Shows string representations of all instances of a given class.
        """
        argument1 = RegexParser(argument)
        if len(argument1) > 0 and argument1[0] not in HBNBCommand.__HBNBClasses:
            print("** class doesn't exist **")
        else:
            objectList = []
            for obj in storage.all().values():
                if len(argument1) > 0 and argument1[0] == obj.__class__.__name__:
                    objectList.append(obj.__str__())
                elif len(argument1) == 0:
                    objectList.append(obj.__str__())
            print(objectList)

    def do_count(self, argument):
        """The Method
        Retrieve the number of instances of a given class."""

        argument1 = RegexParser(argument)
        counter = 0

        for obj in storage.all().values():
            if argument1[0] == obj.__class__.__name__:
                counter += 1
        print(counter)


    def do_update(self, argument):
        """The Method
        Update a class instance of a given id by adding """

        argument1 = RegexParser(argument)
        objectDictionary = storage.all()

        if len(argument1) == 0:
            print("** class name missing **")
            return False
        
        if argument1[0] not in HBNBCommand.__HBNBClasses:
            print("** class doesn't exist **")
            return False
        
        if len(argument1) == 1:
            print("** instance id missing **")
            return False
        
        if "{}.{}".format(argument1[0], argument1[1]) not in objectDictionary.keys():
            print("** no instance found **")
            return False
        
        if len(argument1) == 2:
            print("** attribute name missing **")
            return False
        
        if len(argument1) == 3:
            try:
                type(eval(argument1[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argument1) == 4:
            obj = objectDictionary["{}.{}".format(argument1[0], argument1[1])]

            if argument1[2] in obj.__class__.__dict__.keys():
                typeOfValue = type(obj.__class__.__dict__[argument1[2]])
                obj.__dict__[argument1[2]] = typeOfValue(argument1[3])
            else:
                obj.__dict__[argument1[2]] = argument1[3]
        elif type(eval(argument1[2])) == dict:
            obj = objectDictionary["{}.{}".format(argument1[0], argument1[1])]

            for key, value in eval(argument1[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    typeOfValue = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = typeOfValue(value)
                else:
                    obj.__dict__[key] = value
        storage.save()

if __name__ == "__main__":
    HBNBCommand().cmdloop() 
