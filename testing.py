# VERONICA THEA MAGNO, MIS
# Assignment 3

from sys import *

# -------------------------------------------------- GLOBAL VARIABLES --------------------------------------------------
tokens = [] # define tokens list. the tokens list is the variable that contains strings
num_stack = [] # defines number stack list. the number stack contains the numbers defined in an expression
symbolTable = {} # a dictionary that contains the variables and their values

# -------------------------------------------------- OPENFILE METHOD --------------------------------------------------
# this method opens the .ipol file
def openFile(fileData):
    ## "r" means that the file is opened for reading only
    fileData = open(ipolFile, "r").read()

    # the <EOF> variable is added to the end of the file so that the interpreter
    # will be aware that there will be no more lines to be interpreted
    fileData += "<EOF>"

    # print(fileData) # for testing purposes only! this prints out the data from the opened text file. 
    return fileData

# -------------------------------------------------- LEX METHOD --------------------------------------------------
# this is the lex method. the lex function defines and parses tokens of the file
def lex(fileContents):
    # variable definitions

    token = "" # token variable is the one that takes each char as the value
    state = 0 # state variable is the one that searches for quotation marks
    string = "" # string variable is the one that takes characters and strings inside quotation marks and treats them as a whole string
    expr = "" # expr variable is the one that takes numbers and operators as a whole expresion
    isexpr = 0 # isexpr variable is of boolean value and checks whether there are operators in the expression
    num = "" # num variable is the one that takes each number as the value
    varStarted = 0 # varStarted variable is of boolean value and checks whether data is a variable
    var = "" # var is the one that will hold the value of the variable being declared

    fileContents = list(fileContents)

    for char in fileContents:
        token += char

        # defining the tokens
        # token variable needs to be reset after every keyword found so that it will be able to find and hold new tokens
        
        # ignore spaces
        if token == " ":
            if state == 0:
                token = ""
            else:
                token = " "

        # this takes on the next line of the file
        elif token  == "\n" or token == "<EOF>":

            # the token == "<EOF>"" line is added so that expressions will be taken into
            # consideration even when there is no new line after them

            # this condition states that if the expr is not empty and if the
            # given is an expression, meaning with operators, it will be 
            # taken as an expression
            if expr != "" and isexpr == 1:
                # print(expr + "EXPR")
                tokens.append("EXPR:" + expr)
                expr = ""

            # this condition states that if the expr is not empty and if the
            # given is an expression, meaning with no operators, it will be 
            # taken as a numers
            elif expr != "" and isexpr == 0:
                # print(expr + "NUM")
                tokens.append("NUM:" + expr)
                expr = ""

            # this condition is for variable assigning
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0

            token = ""

        # this looks for an equal sign for variable assigning
        elif token == "=" and state == 0:

            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""

            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0      

            if tokens[-1] == "EQUALS":
               # tokens.append("EQEQ")
               tokens[-1] = "EQEQ"
            else:
                tokens.append("EQUALS")

            token = ""
        
        # this looks for the $ sign, which is an indicator that the data is a variable
        elif token == "$" and state == 0:
            varStarted = 1
            var += token
            token = ""

        # this checks if varStarted is true and adds the token to the var variable
        elif varStarted == 1:

            if token == "<" or token == ">":
                if var != "":
                    tokens.append("VAR:" + var)
                    var = ""
                    varStarted = 0

            var += token
            token = ""

        # this looks for the word "PRINT"    
        elif token == "PRINT" or token == "print":
            tokens.append("PRINT")
            token = ""

        # this looks for the word "IF"
        elif token == "IF" or token == "if":
            tokens.append("IF")
            token = ""

        # this looks for the word "ELIF"
        elif token == "ENDIF" or token == "endif":
            tokens.append("ENDIF")
            token = ""

        # this looks for the word "THEN"
        elif token == "THEN" or token == "then":

            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""

            tokens.append("THEN")
            token = ""

        # this looks for the word "INPUT"
        elif token == "INPUT" or token == "input":
            tokens.append("INPUT")
            token = ""

        # this looks for a token and determines if it is a number or not
        elif token == "0" or token == "1" or token == "2" or token == "3" or token == "4" or token == "5" or token == "6" or token == "7" or token == "8" or token == "9":
            # print("NUMBER")
            expr += token
            token = ""
        
        # this looks for the plus sign and sets the isexpr to 1 since it is an expression
        elif token == "+" or token == "-" or token == "/" or token == "*" or token == "%" or token == "**" or token == "//" or token == "++" or token == "--" or token == "(" or token == ")":
            isexpr = 1
            expr += token
            token = ""

        elif token == "\t":
            token = ""

        # this looks for quotation marks
        # state = 0, every letter we find is part of a keyword or variable
        # state = 1, every letter we find is part of a string
        elif token == "\"" or token == " \"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                token = ""

        # this means that we found a double quote and will take every letter inside the quotes as part of a string
        elif state == 1:
            string += token
            token = ""

    print(tokens)  # for debugging purposes only!  
    # print(expr) # for debugging purposes only!  
    return '' # for debugging purposes only!  
    # return tokens

# -------------------------------------------------- EVALUATEEXPRESSION METHOD --------------------------------------------------
# this method evaluates the expresions formed in the lex method. it takes expr from the lex method as a parameter
def evaluateExpression(expr):
    return eval(expr)

# -------------------------------------------------- ASSIGNVARIABLE METHOD --------------------------------------------------
# this method stores the variables and their values. it takes varName and varValue as the parameters 
def assignVariable(varName, varValue):
    
    # 4: means that it will remove "VAR:" from the stored value FOR NUM DATA TYPE
    symbolTable[varName] = varValue 

    # print("ASSIGNVARIABLE METHOD, VARNAME: ", varName) # for debugging purposes only!
    # print("ASSIGNVARIABLE METHOD, VARVALUE: ", varValue) # for debugging purposes only!

# -------------------------------------------------- GETVARIABLE METHOD --------------------------------------------------    
# this method retrieves the variables and their values from the symbolTable dictionary
def getVariable(varName):

    # print("GETVARIABLE METHOD, VARNAME: ", varName) # for debugging purposes only!
    varName = varName[4:]

    if varName in symbolTable:
        return symbolTable[varName] # for debugging purposes only!
    else:
        return "VARIABLE ERROR: Undefined variable."
        exit()

# -------------------------------------------------- GETINPUT METHOD --------------------------------------------------
# this method retrieves and processes the input from the user
def getInput(string, varName):
    i = input(string[1:-1] + " ")

    symbolTable[varName] = i

# -------------------------------------------------- PARSE METHOD --------------------------------------------------
# this method takes toks as the parameter, which is the fileData variable passed on to the lex method.
def parse(toks):
    
    i = 0
    while(i < len(toks)):

        # this takes the tokens and deciphers the keywords so that it will
        # know what operation to do
        if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
            
            # this condition checks if the first word in the line of the file
            # is equal to string. If yes, it will take out the STRING word and
            # print out the corresponding value
            if toks[i+1][0:6] == "STRING":
                print(toks[i+1][8:-1])
            
            # this condition checks if the first word in the line of the file
            # is equal to num. If yes, it will take out the NUM word and
            # print out the corresponding value           
            elif toks[i+1][0:3] == "NUM":
                print(toks[i+1][4:])
            
            # this condition checks if the first word in the line of the file
            # is equal to expr. If yes, it will take out the EXPR word and
            # print out the corresponding value                 
            elif toks[i+1][0:4] == "EXPR":

                # this line uses evaluatedExp as the holder of the value from
                # the evaluateExpression method. the evaluateExpression method
                # takes the parsed value from EXPR as the parameter
                evaluatedExp = evaluateExpression(toks[i+1][5:])
                print(evaluatedExp)    

            # this condition checks if the first word in the line of the file
            # is equal to var. If yes, it will take out the VAR word and
            # print out the corresponding value                 
            elif toks[i+1][0:3] == "VAR":        
                print(getVariable(toks[i+1]))

            i += 2
                
        # this condition is what outputs the stored variables
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            # print(toks[i+2]) # for debugging purposes only!

            # assignVariable(toks[i], toks[i+2]) # for debugging purposes only!

            # we take 'i+2' since toks is a list, and if we take a look at VAR EQUALS STRING, STRING is in position 2 which means that we have to use 2 since we are evaluating the type
            if toks[i+2][0:6] == "STRING":
                assignVariable(toks[i], toks[i+2][8:-1])

            elif toks[i+2][0:3] == "NUM":
                assignVariable(toks[i], toks[i+2][4:])

            elif toks[i+2][0:4] == "EXPR":
                assignVariable(toks[i], evaluateExpression(toks[i+2][5:]))

            elif toks[i+2][0:3] == "VAR":
                assignVariable(toks[i], getVariable(toks[i+2]))

            i += 3

        # this condition is for input variables
        elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
            getInput(toks[i+1][7:],toks[i+2][4:])

            i+=3

    # print(symbolTable) # for debugging purposes only!

# -------------------------------------------------- RUNFILE METHOD --------------------------------------------------
# this method runs the chosen file
def runFile():

    # fileData is the variable that holds the contents of the nominated file
    # from open_file method, which takes ipolFile as the parameter -- taken from the user
    fileData = openFile(ipolFile)

    # toks is the variable that holds the data passed from the lex method , which takes fileData as the parameter
    toks = lex(fileData)

    # parse is the method that takes toks as the parameter. the parse method is
    # the method where the tokens are readied for outputing
    parse(toks)

# -------------------------------------------------- PROGRAM PROPER --------------------------------------------------
while True: 

    ipolFile = input("Please enter the file to be interpreted: ")

    if ipolFile.endswith(".ipol"):
        runFile()
        break
    else:
        print("Please enter the file to be interpreted. Must be in .ipol extension.")