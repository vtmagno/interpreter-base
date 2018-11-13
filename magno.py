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
    expr = "" # takes numbers and operators as a whole expresion
    var = "" # will hold the value of the variable being declared

    foundBracket = 0 # indicates whether the current token is a [ or a ]
    stringVarStarted = 0 # indicates whether the variable assignment for strings have started

    for char in fileContents:

        token += char

        # ignore spaces
        if token == " ":

            if foundBracket == 0:
                stringVarStarted = 1
                token = ""

            # gets the variable name after the DSTR keyword
            if stringVarStarted == 1:

                if var != "":
                    listOfTokens.append("VAR:" + var)
                    var = ""
                    stringVarStarted = 0

            else:
                token = " "

        elif token == "\n" or token == "<EOF>" or token == "\t":
            # print("FOUND NEW LINE") # for debugging purposes only. signifies that a new line was found.
            token = ""

            # this was added so that variables that aren't after the keywords DSTR and DINT are taken as variables
            stringVarStarted = 0

        # condition satisfied if token parsed evaluates to GIVEYOU!
        elif token == "CREATE":
            listOfTokens.append("CREATE")
            # print("CREATE") # for debugging purposes only. signifies that the word CREATE
            token = ""
            
        # condition satisfied if token parsed evaluates to GIVEYOU!
        elif token == "GIVEYOU! ":
            listOfTokens.append("GIVEYOU!")
            # print("GIVEYOU!") # for debugging purposes only. signifies that the word GIVEYOU!
            stringVarStarted = 1
            token = ""

        # condition satisfied if token parsed evaluates to GIVEYOU!!
        elif token == "GIVEYOU!! ":
            listOfTokens.append("GIVEYOU!!")
            # print("GIVEYOU!!") # for debugging purposes only. signifies that the word GIVEYOU!!
            stringVarStarted = 1
            token = ""

        # condition satisfied if token parsed evaluates to DSTR
        elif token == "DSTR":
            stringVarStarted = 1
            listOfTokens.append("DSTR")
            token = ""

        elif token == "WITH ":
            # print("WITH found") # for debugging purposes only. signifies that the word WITH
            listOfTokens.append("WITH")
            token = ""

        elif token == "DINT ":
            # print("DINT found") # for debugging purposes only. signifies that the word DINT
            listOfTokens.append("DINT")
            token = ""

        # condition satisfied when stringVarStarted == 1. constructs the variable name.
        elif stringVarStarted == 1:
            var += token
            token = ""

        # this looks for a token and determines if it is a number or not
        elif token == "0" or token == "1" or token == "2" or token == "3" or token == "4" or token == "5" or token == "6" or token == "7" or token == "8" or token == "9":
            # print("NUMBER") # for debugging purposes only. signifies that a number was found
            expr += token 
            # print(expr) # for debugging purposes only. prints out the created expression
            token = ""

        # condition satisfied if stringVarStarted == 1
        # elif stringVarStarted == 1:

        # this looks for [], which signifies that the following will be a string
        # foundBracket = 0, every letter we find is part of a keyword or variable
        # foundBracket = 1, every letter we find is part of a string
        elif token == "[":
            if foundBracket == 0:
                foundBracket = 1
                
        elif token == "]":
            if foundBracket == 1:
                listOfTokens.append("STRING:" + string[1:]) 
                string = ""
                token = ""
            foundBracket = 0     
        
        elif foundBracket == 1:
            string += token     
            token = ""    

    #print(token) # for debugging purposes only. prints every parsed character
    #print(listOfTokens) # for debugging purposes only. this shows the contents of the list made by both the parser and lexer
    #return '' # for debugging purposes only. avoids listIndex out of range error when removing return token
    return listOfTokens

# ******************************************************** assign_variable() METHOD ********************************************************
# This method assigns a value to a variable name in the variableDictionary.

def assign_variable(varName, varValue):

    variableDictionary[varName[4:]] = varValue

    print("VARNAME: varName") # for debugging purposes only. this prints the variable name
    print("VARVALUE: varValue") # for debugging purposes only. this prints the variable value

# ******************************************************** get_variable() METHOD ********************************************************
# This method retrieves the variables and their values from the variableDictionary

def get_variable(varName):

    varName = varName[4:]

    print("VARNAME: varName") # for debugging purposes only. this prints the variable name

    if varName in variableDictionary:
        return variableDictionary[varName]
    else:
        return "VARIABLE ERROR: Undefined variable."    

# ******************************************************** parser() METHOD ********************************************************
# This method analyzes the tokens and syntax of the file. It is paired with the lexer method. 

def parser(toks):

    i = 0

    while(i < len(toks)):

        # the i+=(NUM) line means how many tokens the parses will get

        # print("entered the parser") # for debugging purposes only

        if toks[i] == "CREATE":
            i+=1

        # for output
        if toks[i] + " " + toks[i+1][0:6] == "GIVEYOU! STRING" or toks[i] + " " + toks[i+1][0:3] == "GIVEYOU! VAR":
             
            print("Entered GIVEYOU! if")

            if toks[i+1][0:6] == "STRING":
                # print("FOUND STRING")
                print(toks[i+1][7:], end=" ")

              
            elif toks[i+1][0:3] == "VAR":
                #print("FOUND VAR")  
                print(get_variable(toks[i+1]))

            i+=2

        # for output
        elif toks[i] + " " + toks[i+1][0:6] == "GIVEYOU!! STRING" or toks[i] + " " + toks[i+1][0:3] == "GIVEYOU!! VAR":
            
            print("Entered GIVEYOU!! if")

            if toks[i+1][0:6] == "STRING":
                # print("FOUND STRING")
                print(toks[i+1][7:])

            elif toks[i+1][0:3] == "VAR":
                # print("FOUND VAR")  
                print(get_variable(toks[i+1]))

            i+=2

        # for assigning variables
        elif toks[i] + " " + toks[i+1][3:] + " " + toks[i+2] + toks[i+3][0:6] == "DSTR VAR WITH STRING": 
            # print(toks[i+2]) # for debugging purposes only!
            print("REACHED")
            if toks[i+3][0:6] == "STRING":
                assign_variable(toks[i+1], toks[i+3][7:])

            i+=4

        print("did not enter")

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