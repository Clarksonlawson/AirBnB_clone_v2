#!/usr/bin/python3

"""Helper function for the parsing of the program """
import re
from shlex import split

def regParser(arg):
    """Parses the program and break it down to
    tokens of arguments"""

    braces = re.search(r"\{(.*?)\}", arg)
    parentesis = re.search(r"\[(.*?)\]", arg)

    if braces is None:
        if parentesis is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:parentesis.span()[0]])
            ax = [i.strip(",") for i in lexer]
            ax.append(parentesis.group())
            return ax
    else:
        lexer = split(arg[:braces.span()[0]])
        ax = [i.strip(",") for i in lexer]
        ax.append(braces.group())
        return ax
