# VERONICA THEA MAGNO, MIS
# Assignment 3

# import all necessary imports
from sys import *

# ******************************************************** GLOBAL VARIABLES ********************************************************
listOfTokens = [] # this list contains the parsed characters and represents them as whole strings
listOfNumStack = [] # this list is for determining if the parsed tokens are expressions
variableDictionary = {} # this dictionary will contain variables and their values

# ******************************************************** open_file() METHOD ********************************************************
# This method opens and readies the file for interpretation.

def open_file(fileData):
    fileData = open(ipolFile, "r").read()
    fileData += "<EOF>"
    return fileData

    # fileData variable contains the contents of the ipolFile which was given
    # by the user. It is set to READ ONLY. <EOF> is added to the end of the file
    # to signify that there are no more lines to interpret.


# ******************************************************** run_file() METHOD ********************************************************
# This method 

def run_file():

    fileData = open_file(ipolFile)
    toks = lexer_method(fileData)
    parser_method(toks)

# fileData = contains the contents of the ipolFile which was given by the user.
# toks =  contains the contents of the fileData that was passed on as a parameter to the lexer_method
# the parser method then takes toks as the parameter for the parser method

# ******************************************************** PROGRAM PROPER ********************************************************
# This is the program proper. Its only objective is to ask the user for the name and extension of
# the file to be interpreted. It will only accept files ending in ".ipol".

while True: 

    ipolFile = input("Please enter the file to be interpreted: ")

    if ipolFile.endswith(".ipol"):
        run_file()
        break
    else:
        print("Please enter the file to be interpreted. Must be in .ipol extension.")

# ipolFile variable contains the name and extension of the file the user wants to interpret. Once
# the program receives the correct type of file, it will run the run_file() method. Else, the 
# program will keep asking the user to input an .ipol file.