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

    # print(fileData) # for debugging purposes only. this will print out the contents of the file

    return fileData

    # fileData variable contains the contents of the ipolFile which was given
    # by the user. It is set to READ ONLY. <EOF> is added to the end of the file
    # to signify that there are no more lines to interpret.

# ******************************************************** lexer() METHOD ********************************************************
# This method analyzes the tokens and syntax of the file. It is paired with the parser method. 

def lexer(fileContents):

    # lexer method variable definitions
    fileContents = list(fileContents) # turn the fileContents strings into a list
    token = "" # the result of parsed characters
    string = "" # string variable is the one that takes characters and strings inside brackets and treats them as a whole string
    foundBracket = 0 # searches for quotation marks

    for char in fileContents:

        token += char

        if token == " ":
            if foundBracket == 0:
                token = ""
            elif foundBracket == 1:
                token = " "

        # condition satisfied if token parsed evaluates to GIVEYOU!
        elif token == "GIVEYOU!":
            listOfTokens.append("GIVEYOU!")
            # print("GIVEYOU!") # for debugging purposes only. signifies that the word CREATE
            token = ""

        # this looks for [], which signifies that the following will be a string
        # foundBracket = 0, every letter we find is part of a keyword or variable
        # foundBracket = 1, every letter we find is part of a string
        elif token == "[":
            if foundBracket == 0:
                foundBracket = 1
                
        elif token == "]":
            if foundBracket == 1:
                foundBracket = 0     
        
        elif foundBracket == 1:
            string += token     
            token = ""    
            
    # append string to listOfTokens
    listOfTokens.append("STRING:" + string[1:]) 
    string = ""

    # print(token) # for debugging purposes only. prints every parsed character
    # print(listOfTokens) # for debugging purposes only. this shows the contents of the list made by both the parser and lexer
    # return '' # for debugging purposes only. avoids listIndex out of range error when removing return token
    return listOfTokens

# ******************************************************** parser() METHOD ********************************************************
# This method analyzes the tokens and syntax of the file. It is paired with the lexer method. 

def parser(toks):

    i = 0
    while(i < len(toks)):

        # the i+=(NUM) line means how many tokens the parses will get

        if toks[i] + " " + toks[i+1][0:6] == "GIVEYOU! STRING":
            print(toks[i+1][7:])
            i+=2

# ******************************************************** run_file() METHOD ********************************************************

def run_file():

    fileData = open_file(ipolFile)
    toks = lexer(fileData)
    parser(toks)

# fileData = contains the contents of the ipolFile which was given by the user.
# toks =  contains the contents of the fileData that was passed on as a parameter to the lexer
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