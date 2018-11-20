# VERONICA THEA MAGNO, MIS
# Assignment 3

# import all necessary imports
from sys import *

# ******************************************************** GLOBAL VARIABLES ********************************************************
listOfTokens = [] # this list contains the parsed characters and represents them as whole strings
listOfNumStack = [] # this list is for determining if the parsed tokens are expressions
listOfLexemesAndTokens = [] # this list is for the table of lexemes and tokens
listOfVariables = [] # this dictionary is for the table of variables, values and types
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
    expr = "" # takes numbers and operators as a whole expresion
    var = "" # will hold the value of the variable being declared

    foundBracket = 0 # indicates whether the current token is a [ or a ]
    stringVarStarted = 0 # indicates whether the variable assignment for strings have started
    exprStarted = 0 # indicates that an expression has started
    isNum = 0
    valueStarted = 0

    for char in fileContents:

        token += char

        # ignore spaces
        if token == " ":

            if foundBracket == 0:
                stringVarStarted = 1
                token = ""

            # gets the variable name after the DSTR and DINT keyword
            if stringVarStarted == 1:

                varDigit = 0

                # this will check if the variable created is a string or a number
                if var.isdigit():
                    varDigit = 1

                if var != "" and exprStarted == 0 and varDigit == 0:

                    listOfTokens.append("VAR:" + var)
                    var = ""
                    stringVarStarted = 0

                elif var != "" and exprStarted == 0 and varDigit == 1:

                    listOfTokens.append("NUM:" + var)
                    var = ""
                    stringVarStarted = 0                    

                elif expr != "" and exprStarted == 1:

                    if expr.isdigit():
                        listOfTokens.append("NUM:" + expr)
                        expr = ""        
                        exprStarted = 0

                    else:
                        # this inserts the token "NUM:0" after an EXPR NUM BLANK
                        if listOfTokens[-1] != listOfTokens[-1][0:3] == "NUM":
                            listOfTokens.append("NUM:0")
                            token = ""

                        listOfTokens.append("EXPR:" + expr)
                        expr = ""        
                        exprStarted = 0                       

            else:
                token = " "

        elif token == "\n" or token == "<EOF>" or token == "\t":
            # print("FOUND NEW LINE") # for debugging purposes only. signifies that a new line was found.
            token = ""

            # this was added so that variables that aren't after the keywords DSTR and DINT are taken as variables
            if var != "" and exprStarted == 0:
                listOfTokens.append("VAR:" + var)
                var = ""
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

        elif token == "GIVEME? ":
            # print("GIVEME? found") # for debugging purposes only. signifies that the word GIVEME?
            listOfTokens.append("GIVEME?")
            token = ""

        # condition satisfied if token parsed evaluates to DSTR
        elif token == "DSTR":
            stringVarStarted = 1
            listOfTokens.append("DSTR")
            token = ""

        # condition satisfied if token parsed evaluates to WITH
        elif token == "WITH ":
            listOfTokens.append("WITH")
            token = ""

        # condition satisfied if token parsed evaluates to DSTR
        elif token == "DINT ":
            # print("FOUND DINT")
            stringVarStarted = 1
            listOfTokens.append("DINT")
            token = ""

        # condition satisfied if token parsed evaluates to PLUS
        elif token == "PLUS":
            # print("PLUS found") # for debugging purposes only. signifies that the word PLUS
            exprStarted = 1
            expr += token
            token = ""    

        # condition satisfied if token parsed evaluates to MINUS
        elif token == "MINUS":
            # print("MINUS found") # for debugging purposes only. signifies that the word MINUS
            exprStarted = 1
            expr += token
            token = ""  

        # condition satisfied if token parsed evaluates to TIMES
        elif token == "TIMES":
            # print("MINUS found") # for debugging purposes only. signifies that the word MINUS
            exprStarted = 1
            expr += token
            token = ""  

        # condition satisfied if token parsed evaluates to DIVBY
        elif token == "DIVBY":
            # print("DIVBY found") # for debugging purposes only. signifies that the word DIVBY
            exprStarted = 1
            expr += token
            token = ""  

        # condition satisfied if token parsed evaluates to MODU
        elif token == "MODU":
            # print("MODU found") # for debugging purposes only. signifies that the word MODU
            exprStarted = 1
            expr += token
            token = ""  

        elif token == "STORE":
            # print("STORE found") # for debugging purposes only. signifies that the word STORE
            listOfTokens.append("STORE")
            token = ""

        elif token == "IN":
            # print("IN found") # for debugging purposes only. signifies that the word IN
            listOfTokens.append("IN")
            token = ""

        elif token == "RUPTURE":
            # print("RUPTURE found") # for debugging purposes only. signifies that the word MODU
            listOfTokens.append("RUPTURE")
            token = ""

        # condition satisfied when stringVarStarted == 1. constructs the variable name.
        elif stringVarStarted == 1:
            var += token
            token = ""

        # this looks for a token and determines if it is a number or not
        if token == "0" or token == "1" or token == "2" or token == "3" or token == "4" or token == "5" or token == "6" or token == "7" or token == "8" or token == "9":
            #print("NUMBER") # for debugging purposes only. signifies that a number was found
            isNum = 1
            listOfTokens.append("NUM:" + token)
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

# ******************************************************** eval_expressions() METHOD ********************************************************
# This method evaluates expressions.

def eval_expressions(expr):
    return eval(expr)

# ******************************************************** assign_variable() METHOD ********************************************************
# This method assigns a value to a variable name in the variableDictionary.

def assign_variable(varName, varValue):

    variableDictionary[varName[4:]] = varValue

    #print("VARNAME: ", varName) # for debugging purposes only. this prints the variable name
    #print("VARVALUE: ", varValue) # for debugging purposes only. this prints the variable value

# ******************************************************** get_variable() METHOD ********************************************************
# This method retrieves the variables and their values from the variableDictionary

def get_variable(varName):

    varName = varName[4:]

    #print("VARNAME: ", varName) # for debugging purposes only. this prints the variable name

    if varName in variableDictionary:
        return variableDictionary[varName]
    else:
        return "VARIABLE ERROR: Undefined variable."    

# ******************************************************** parser() METHOD ********************************************************
# This method analyzes the tokens and syntax of the file. It is paired with the lexer method. 

def parser(toks):

    i = 0
    lineNum = 0

    exprString = ""
    finalExpr = ""

    while(i < len(toks)):

        # the i+=(NUM) line means how many tokens the parses will get

        # print("entered the parser") # for debugging purposes only

		# this adds 1 to lineNum everytime the parser finishes a line
		
		# this is for the lexeme CREATE.
        if toks[i] == "CREATE":
		
            lineNum += 1

			# this adds the CREATE lexeme to the listOfLexemesAndTokens
            listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "PROGRAM_CREATE" + "\t\t\t\t" + "CREATE" + "\n")
			
			# this adds the lexeme create to the listOfTokens
    

            i+=1

        if toks[i] == "WITH":
		
			# this adds the CREATE lexeme to the listOfLexemesAndTokens
            listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY" + "\t\t" + "WITH" + "\n")       

			# this adds the lexeme create to the listOfTokens
            i+=1

        # for output
        elif toks[i] + " " + toks[i+1][0:6] == "GIVEYOU! STRING" or toks[i] + " " + toks[i+1][0:3] == "GIVEYOU! VAR":

            lineNum += 1

			# this adds the GIVEYOU! lexeme to the listOfLexemesAndTokens
            if toks[i] == "GIVEYOU!":
			
				# this adds the GIVEYOU! lexeme to the listOfLexemesAndTokens
                listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "OUTPUT" + "\t\t\t\t\t" + "GIVEYOU!" + "\n")            

			# this adds the STRING lexeme to the listOfLexemesAndTokens
            if toks[i+1][0:6] == "STRING":
			
				# this adds the STRING lexeme to the listOfLexemesAndTokens
                listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "STRING" + "\t\t\t" + toks[i+1][7:] + "\n")   

				# this prints out the string given
                print(toks[i+1][7:], end=" ")

			# this adds the VAR lexeme to the listOfLexemesAndTokens
            elif toks[i+1][0:3] == "VAR":
                
				# this adds the VAR lexeme to the listOfLexemesAndTokens
                listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "IDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")           

				# this prints out the var given
                print(get_variable(toks[i+1]), end=" ")
				
			# this adds the lexeme create to the listOfTokens
            i+=2

        # for output
        elif toks[i] + " " + toks[i+1][0:6] == "GIVEYOU!! STRING" or toks[i] + " " + toks[i+1][0:3] == "GIVEYOU!! VAR":

            lineNum += 1

			# this adds the GIVEYOU!! lexeme to the listOfLexemesAndTokens
            if toks[i] == "GIVEYOU!!":
			
				# this adds the GIVEYOU!! lexeme to the listOfLexemesAndTokens
                listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "OUTPUT_WITH_LINE" + "\t\t\t" + "GIVEYOU!!" + "\n")            

			# this adds the STRING lexeme to the listOfLexemesAndTokens
            if toks[i+1][0:6] == "STRING":
 
				# this adds the STRING lexeme to the listOfLexemesAndTokens
                listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "STRING" + "\t\t\t" + toks[i+1][7:] + "\n")         

				# this prints out the string given
                print("\n" + toks[i+1][7:])

			# this adds the VAR lexeme to the listOfLexemesAndTokens
            elif toks[i+1][0:3] == "VAR":
 
				# this adds the VAR lexeme to the listOfLexemesAndTokens
                listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "IDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")          

				# this prints out the var given
                print("\n" + get_variable(toks[i+1]))

            i+=2

        elif toks[i] + " " + toks[i+1][0:3] == "DSTR VAR" or toks[i] + " " + toks[i+1][0:3] == "DINT VAR":

            print("ENTERED")
            
            if toks[i+2] == "":

                lineNum += 1

                if toks[i+1] == "DSTR":
                    assign_variable(toks[i+1], "")
                elif toks[i+1] == "DINT": 
                    assign_variable(toks[i+1], 0)

                i+=2

            elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:6] == "DSTR VAR WITH STRING" or toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] == "DSTR VAR WITH NUM":
                
                lineNum += 1

                    # this is for the LEXEMES AND TOKENS TABLE
                if toks[i] == "DSTR":
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_STRING" + "\t\t\t" + "DSTR" + "\n")
                
                if toks[i+1][0:3] == "VAR":
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "IDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")

                if toks[i+2] == "WITH":
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY" + "\t\t" + "WITH" + "\n")       

                if toks[i+3][0:6] == "STRING":
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "STRING" + "\t\t\t\t\t" + toks[i+3][7:] + "\n")       
                    listOfVariables.append(toks[i+1][4:] + "\t\t" + "STRING" + "\t\t\t" + toks[i+3][7:] + "\n")

                if toks[i+3][0:6] == "STRING":
                    assign_variable(toks[i+1], toks[i+3][7:])

                i+=4

            elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] == "DINT VAR WITH NUM":
                
                lineNum += 1

                    # this is for the LEXEMES AND TOKENS TABLE
                if toks[i] == "DSTR":
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_STRING" + "\t\t\t" + "DINT" + "\n")
                
                if toks[i+1][0:3] == "VAR":
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "IDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")

                if toks[i+2] == "WITH":
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY" + "\t\t" + "WITH" + "\n")       

                if toks[i+3][0:6] == "NUM":
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER" + "\t\t\t\t\t" + toks[i+3][3:] + "\n")       
                    listOfVariables.append(toks[i+1][4:] + "\t\t" + "INTEGER" + "\t\t\t" + toks[i+3][3:] + "\n")

                if toks[i+3][0:3] == "NUM":
                    assign_variable(toks[i+1], toks[i+3][4:])

                i+=4

            elif toks[i+2]:

                if toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][5:]  + " " + toks[i+4][0:3] + " " + toks[i+5][0:3] + " " + toks[i+6][5:] + " " + toks[i+7][0:3] + " " + toks[i+8][0:3] == "DINT VAR WITH PLUS NUM NUM MINUS NUM NUM":

                    lineNum += 1

                    exprString = "(",toks[i+4][4:], "+", toks[i+5][4:], ")+(", toks[i+7][4:], "-", toks[i+8][4:], ")"
                    finalExpr = ''.join(map(str, exprString))

                    assign_variable(toks[i+1][4:], eval_expressions(finalExpr))
                    listOfVariables.append(toks[i+1][4:] + "\t\t\t" + "INTEGER" + "\t\t\t" + str(eval_expressions(finalExpr)) + "\n")

                    if toks[i] == "DINT":
                        listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_STRING" + "\t\t\t" + "DINT" + "\n")
                    if toks[i+1][0:3] == "VAR":
                        listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "IDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    if toks[i+2] == "WITH":
                        listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY" + "\t\t" + "WITH" + "\n")      
                    if toks[i+3][5:] == "PLUS":
                        listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "BASIC_OPERATOR" + "\t\t\t\t" + "PLUS" + "\n")             

                    i+=9

        # DINT VAR WITH PLUS NUM NUM MINUS NUM NUM

# ******************************************************** run_file() METHOD ********************************************************

def run_file():

    fileData = open_file(ipolFile)
    toks = lexer(fileData)
    parser(toks)

# fileData = contains the contents of the ipolFile which was given by the user.
# toks =  contains the contents of the fileData that was passed on as a parameter to the lexer
# the parser method then takes toks as the parameter for the parser method

# ******************************************************** lexemes_tokens() METHOD ********************************************************
# This method displays the lexemes and tokens table

def lexemes_tokens():
    print(*listOfLexemesAndTokens)

# ******************************************************** variables_table() METHOD ********************************************************
# This method displays the stored variables

def variables_table():
    print(*listOfVariables)

# ******************************************************** PROGRAM PROPER ********************************************************
# This is the program proper. Its only objective is to ask the user for the name and extension of
# the file to be interpreted. It will only accept files ending in ".ipol".

while True: 

    print("")
    ipolFile = input("Please enter interpol file to interpret (ex. sample.ipol): ")

    if ipolFile.endswith(".ipol"):
        print("")
        print("=========================== OUTPUT =========================================")
        run_file()
        print("")
        print("========================= LEXEMES AND TOKENS TABLE =========================")
        print("Line #\t\t\tTokens\t\t\t\t\tLexemes ")
        lexemes_tokens()
        print("")
        print("========================= SYMBOL TABLE ======================================")
        print("Variable Name\t\tType\t\t\tValue ")
        variables_table()

        print("")
        break
    else:
        print("Please enter the file to be interpreted. Must be in .ipol extension.")

# ipolFile variable contains the name and extension of the file the user wants to interpret. Once
# the program receives the correct type of file, it will run the run_file() method. Else, the 
# program will keep asking the user to input an .ipol file.