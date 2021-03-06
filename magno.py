# VERONICA THEA MAGNO, MIS
# Assignment 3

# import all necessary imports
from sys import *
import math

# ******************************************************** GLOBAL VARIABLES ********************************************************
listOfTokens = [] # this list contains the parsed characters and represents them as whole strings
listOfNumStack = [] # this list is for determining if the parsed tokens are expressions
listOfLexemesAndTokens = [] # this list is for the table of lexemes and tokens

# ******************************************************** addToVarDic() CLASS ********************************************************
# This class defines the variable dictionary

class addToVarDic(object):
    def __init__(self):
        self.variableDictionary = {}

    def addVar(self, variableName, dataType, variableValue):
        self.variableDictionary[variableName] = {'variableName': variableName, 'dataType': dataType, 'variableValue': variableValue}

# ******************************************************** CLASS INSTANCES ********************************************************
addVariable = addToVarDic()

# ******************************************************** variables_table() method ********************************************************
# This method displays the stored variables

def variables_table():

    variablePrintList = []
    finalVarFormat = ""
    varFormat = ""

    for variableDic in addVariable.variableDictionary.values():
            varFormat = variableDic['variableName'], "\t\t\t",  variableDic['dataType'], "\t\t\t",  variableDic['variableValue']
            finalVarFormat = ''.join(map(str, varFormat))
            print(finalVarFormat)

# ******************************************************** open_file() METHOD ********************************************************
# This method opens and readies the file for interpretation.

def open_file(fileData):
    fileData = open(ipolFile, "r").read()
    fileData += "<EOF>"
    #print(fileData) # for debugging purposes only. this will print out the contents of the file

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

                    for character in var:
                        if character == ".":
                            print("Error. No float values are allowed.")
                            exit()

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

        elif token == "<EOF>":
            listOfTokens.append("<EOF>")
            token = ""        
            
        elif token == "\n" or token=="":
            listOfTokens.append(":")
            token = ""

        elif token == "\n" or token == "\t":
            # print("FOUND NEW LINE") # for debugging purposes only. signifies that a new line was found.
            #listOfTokens.append(":")
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
            stringVarStarted = 1
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

        elif token == "ROOT":
            # print("ROOT found") # for debugging purposes only. signifies that the word MODU
            exprStarted = 1
            expr += token
            token = ""  

        elif token == "MEAN":
            # print("ROOT found") # for debugging purposes only. signifies that the word MODU
            exprStarted = 1
            expr += token
            token = ""  

        elif token == "RAISE":
            # print("RAISE found") # for debugging purposes only. signifies that the word MODU
            exprStarted = 1
            expr += token
            token = ""  

        elif token == "DIST":
            # print("RAISE found") # for debugging purposes only. signifies that the word MODU
            exprStarted = 1
            expr += token
            token = ""    

        elif token == "AND":
            # print("RAISE found") # for debugging purposes only. signifies that the word MODU
            listOfTokens.append("AND")
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

    try:
        if listOfTokens[0] != "CREATE":
            print("Error. File must begin with CREATE.")
    except IndexError:
        print("Error. File must begin with CREATE.")
        quit()

        
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

    varType = ""

    if varValue.isdigit() or varValue == 0:
        varType = "\tINTEGER"
    else:
        varType = "STRING"

    addVariable.addVar(varName[4:], varType, varValue)

    #print("VARNAME: ", varName) # for debugging purposes only. this prints the variable name
    #print("VARVALUE: ", varValue) # for debugging purposes only. this prints the variable value

# ******************************************************** get_variable() METHOD ********************************************************
# This method retrieves the variables and their values from the variableDictionary

def get_variable(varName):

    varName = varName[4:]

    if varName in addVariable.variableDictionary[varName]['variableName']:
        return addVariable.variableDictionary[varName]['variableValue']
    else:
        return "VARIABLE ERROR: Undefined variable."    

# ******************************************************** match_syntax() METHOD ********************************************************
# This method checks the syntax for DINT and DSTR

def match_syntax(var1, var2):

    err = 0

    if var1 != var2:

        err = 1

        return err

    else:

        return err

# ******************************************************** parser() METHOD ********************************************************
# This method analyzes the tokens and syntax of the file. It is paired with the lexer method. 

def parser(toks):

    i = 0
    lineNum = 0
    err = 0

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

        if toks[i] == ":":
            i+=1

        elif toks[i] == "RUPTURE":
		
            lineNum += 1

			# this adds the CREATE lexeme to the listOfLexemesAndTokens
            listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "PROGRAM_RUPTURE" + "\t\t\t\t" + "RUPTURE" + "\n")
			
			# this adds the lexeme create to the listOfTokens

            i+=2

        elif toks[i] == "<EOF>":
		
            lineNum += 1

			# this adds the CREATE lexeme to the listOfLexemesAndTokens
            listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "EOF" + "\t\t\t\t\t" + "<EOF>" + "\n")
			
			# this adds the lexeme create to the listOfTokens

            i+=1

        elif toks[i] == "WITH":
		
			# this adds the CREATE lexeme to the listOfLexemesAndTokens
            listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY" + "\t\t" + "WITH" + "\n")       

			# this adds the lexeme create to the listOfTokens
            i+=1

        elif toks[i] + " " + toks[i+1][0:3] == "GIVEME? VAR":

            lineNum += 1

            variable_Input = input("What is your name? ")

            #GIVEME?
            listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INPUT" + "\t\t\t\t\t" + "GIVEME?" + "\n")  
            #VAR
            listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "IDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")       

            assign_variable(toks[i+1], variable_Input)  

            i+=3

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
                print("\n" + toks[i+1][7:], sep='')

			# this adds the VAR lexeme to the listOfLexemesAndTokens
            elif toks[i+1][0:3] == "VAR":
                
				# this adds the VAR lexeme to the listOfLexemesAndTokens
                listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "IDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")           

				# this prints out the var given
                print("\n" + get_variable(toks[i+1]), sep='')
				
			# this adds the lexeme create to the listOfTokens
            i+=3

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
                print("\n" + str(get_variable(toks[i+1])))

            i+=3

        elif toks[i] == "DINT":

            operator = ""
            operator2 = ""

            openParenthesis = "("         
            closeParenthesis = ")"      

            err = 0

            # -------------------------------------------- for DINT VAR only
            if err == 0:
            
                err = match_syntax(toks[i+1][0:3], "VAR")
                err = match_syntax(toks[i+2], ":")

                if err == 0:

                    lineNum +=1 

                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARE_INTEGER" + "\t\t\t\t" + "DINT" + "\n")

                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    
                    assign_variable(toks[i+1], "0")
                    i += 3
                    
            # -------------------------------------------- for DINT VAR WITH NUM only	
            
            if err == 1:

                err = match_syntax(toks[i+3][0:3], "NUM")
                err = match_syntax(toks[i+4], ":")

                if err == 0:

                    lineNum += 1

                    #DINT
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARE_INTEGER" + "\t\t\t\t" + "DINT" + "\n")
                    #VAR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    #WITH
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY " + "\t\t" + "WITH" + "\n")    
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+3][4:] + "\n")                    
                  
                    assign_variable(toks[i+1], toks[i+3][4:])
                    i+=5

            # -------------------------------------------- for DINT VAR WITH EXPR NUM NUM only	
            if err == 1:

                err = match_syntax(toks[i+3][0:4], "EXPR")
                err = match_syntax(toks[i+4][0:3], "NUM")
                err = match_syntax(toks[i+5][0:3], "NUM")
                err = match_syntax(toks[i+6], ":")

                if err == 0:

                    lineNum +=1

                    #DINT
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARE_INTEGER" + "\t\t\t\t" + "DINT" + "\n")
                    #VAR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    #WITH
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY " + "\t\t" + "WITH" + "\n")    
                    #EXPR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "BASIC_OPERATOR" + "\t\t\t\t" + toks[i+3][5:] + "\n")    
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+4][4:] + "\n")
                    # IF SECOND NUM IS NOT EQUAL TO 0
                    if toks[i+5][0:4] != "0":
                        listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+5][4:] + "\n")

                    #err = match_syntax(toks[i+4][0:3], "NUM")
                    #err = match_syntax(toks[i+5][0:3], "NUM")

                    if toks[i+3][5:] == "PLUS":
                        operator = "+"
                    elif toks[i+3][5:] == "MINUS":
                        operator = "-"
                    elif toks[i+3][5:] == "DIVBY":
                        operator = "/"
                    elif toks[i+3][5:] == "TIMES":
                        operator = "*"
                    elif toks[i+3][5:] == "MODU":
                        operator = "%"
                    elif toks[i+3][5:] == "RAISE":
                        operator = "**"

                    if toks[i+3][5:] == "ROOT":
                        exprString = toks[i+4][4:], operator, (toks[i+5][4:])
                        finalExpr = ''.join(map(str, exprString))

                    else:
                        exprString = toks[i+4][4:], operator, toks[i+5][4:]
                        finalExpr = ''.join(map(str, exprString))

                    assign_variable(toks[i+1], str(eval_expressions(finalExpr)))

                    i+=7

            # -------------------------------------------- for DINT VAR WITH EXPR NUM NUM EXPR NUM NUM only	
            if err == 1:                

                # DINT VAR WITH EXPR NUM NUM EXPR NUM NUM
                err = match_syntax(toks[i+2][0:4], "EXPR")
                err = match_syntax(toks[i+3][0:3], "NUM")
                err = match_syntax(toks[i+4][0:3], "NUM")
                err = match_syntax(toks[i+5][0:4], "EXPR")
                err = match_syntax(toks[i+6][0:3], "NUM")
                err = match_syntax(toks[i+7][0:3], "NUM")
                err = match_syntax(toks[i+8], ":")
                
                if err == 0:

                    lineNum +=1

                    #DINT
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARE_INTEGER" + "\t\t\t\t" + "DINT" + "\n")
                    #VAR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    #WITH
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY " + "\t\t" + "WITH" + "\n")    
                    #EXPR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "BASIC_OPERATOR" + "\t\t\t\t" + toks[i+3][5:] + "\n")    
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+4][4:] + "\n")
                    #NUM
                    if toks[i+5][4:] != "0":
                        listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+5][4:] + "\n")
                    #EXPR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "BASIC_OPERATOR" + "\t\t\t\t" + toks[i+6][5:] + "\n")   
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+7][4:] + "\n")
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+8][4:] + "\n")                                         

                    if toks[i+2][5:] == "PLUS":
                        operator = "+"
                    elif toks[i+2][5:] == "MINUS":
                        operator = "-"
                    elif toks[i+2][5:] == "DIVBY":
                        operator = "/"
                    elif toks[i+2][5:] == "TIMES":
                        operator = "*"
                    elif toks[i+2][5:] == "MODU":
                        operator = "%"
                    elif toks[i+2][5:] == "RAISE":
                        operator = "**"
                    elif toks[i+2][5:] == "ROOT":
                        exprString = toks[i+4][4:], operator, (toks[i+5][4:])
                        finalExpr = ''.join(map(str, exprString))

                    if toks[i+5][5:] == "PLUS":
                        operator2 = "+"
                    elif toks[i+5][5:] == "MINUS":
                        operator2 = "-"
                    elif toks[i+5][5:] == "DIVBY":
                        operator2 = "/"
                    elif toks[i+5][5:] == "TIMES":
                        operator2 = "*"
                    elif toks[i+5][5:] == "MODU":
                        operator2 = "%"         
                    elif toks[i+5][5:] == "RAISE":
                        operator2 = "**"    
                    elif toks[i+5][5:] == "ROOT":
                        exprString = toks[i+7][4:], operator, (toks[i+8][4:])
                        finalExpr = ''.join(map(str, exprString))

                    exprString = openParenthesis, toks[i+3][4:], operator, toks[i+4][4:], closeParenthesis, operator, openParenthesis, toks[i+6][4:], operator2, toks[i+7][4:], closeParenthesis
                    
                    print(exprString)
                    finalExpr = ''.join(map(str, exprString))

                    assign_variable(toks[i+1], str(eval_expressions(finalExpr)))
                    i+=11            

            # -------------------------------------------- for DINT VAR WITH EXPR NUM NUM EXPR NUM NUM : only	
            if err == 1:                

                # DINT VAR WITH EXPR NUM NUM EXPR NUM NUM
                err = match_syntax(toks[i+3][0:4], "EXPR")
                err = match_syntax(toks[i+4][0:3], "NUM")
                err = match_syntax(toks[i+5][0:3], "NUM")
                err = match_syntax(toks[i+6][0:4], "EXPR")
                err = match_syntax(toks[i+7][0:3], "NUM")
                err = match_syntax(toks[i+8][0:3], "NUM")
                err = match_syntax(toks[i+9], ":")

                if err == 0:

                    lineNum +=1

                    #DINT
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARE_INTEGER" + "\t\t\t\t" + "DINT" + "\n")
                    #VAR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    #WITH
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY " + "\t\t" + "WITH" + "\n")    
                    #EXPR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "BASIC_OPERATOR" + "\t\t\t\t" + toks[i+3][5:] + "\n")    
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+4][4:] + "\n")
                    #NUM
                    if toks[i+5][4:] != "0":
                        listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+5][4:] + "\n")
                    #EXPR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "BASIC_OPERATOR" + "\t\t\t\t" + toks[i+6][5:] + "\n")   
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+7][4:] + "\n")
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+8][4:] + "\n")                                         

                    if toks[i+3][5:] == "PLUS":
                        operator = "+"
                    elif toks[i+3][5:] == "MINUS":
                        operator = "-"
                    elif toks[i+3][5:] == "DIVBY":
                        operator = "/"
                    elif toks[i+3][5:] == "TIMES":
                        operator = "*"
                    elif toks[i+3][5:] == "MODU":
                        operator = "%"
                    elif toks[i+3][5:] == "RAISE":
                        operator = "**"
                    elif toks[i+3][5:] == "ROOT":
                        exprString = toks[i+4][4:], operator, (toks[i+5][4:])
                        finalExpr = ''.join(map(str, exprString))

                    if toks[i+6][5:] == "PLUS":
                        operator2 = "+"
                    elif toks[i+6][5:] == "MINUS":
                        operator2 = "-"
                    elif toks[i+6][5:] == "DIVBY":
                        operator2 = "/"
                    elif toks[i+6][5:] == "TIMES":
                        operator2 = "*"
                    elif toks[i+6][5:] == "MODU":
                        operator2 = "%"         
                    elif toks[i+6][5:] == "RAISE":
                        operator2 = "**"    
                    elif toks[i+6][5:] == "ROOT":
                        exprString = toks[i+7][4:], operator, (toks[i+8][4:])
                        finalExpr = ''.join(map(str, exprString))

                    exprString = openParenthesis, toks[i+4][4:], operator, toks[i+5][4:], closeParenthesis, operator, openParenthesis, toks[i+7][4:], operator2, toks[i+8][4:], closeParenthesis
                    finalExpr = ''.join(map(str, exprString))

                    assign_variable(toks[i+1], str(eval_expressions(finalExpr)))
                    i+=10               
			
			# -------------------------------------------- for DINT VAR WITH DIST NUM NUM AND NUM NUM only	
            if err == 1:

                # DINT VAR WITH DIST NUM NUM AND NUM NUM

                err = match_syntax(toks[i+2][0:4], "EXPR")
                err = match_syntax(toks[i+3][0:3], "NUM")
                err = match_syntax(toks[i+4][0:3], "NUM")
                err = match_syntax(toks[i+5][4:], "AND")
                err = match_syntax(toks[i+6][0:3], "NUM")
                err = match_syntax(toks[i+7][0:3], "VAR")	
                
                dist = 0

                if err == 0:

                    lineNum +=1

                    #DINT
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARE_INTEGER" + "\t\t\t\t" + "DINT" + "\n")
                    #VAR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    #WITH
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY " + "\t\t" + "WITH" + "\n")    
                    #DIST
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "BASIC_OPERATOR" + "\t\t\t\t" + "DIST" + "\n")    
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+3][4:] + "\n")
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+4][4:] + "\n")
                    #AND
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DISTANCE_AND " + "\t\t\t\t" + "AND" + "\n")					
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+6][4:] + "\n")	
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER " + "\t\t\t\t" + toks[i+7][4:] + "\n")		

                    num_x2 = int(toks[i+6][4:])
                    num_x1 = int(toks[i+3][4:])
                    
                    num_y2 = int(toks[i+7][4:])
                    num_y1 = int(toks[i+4][4:])

                    dist = math.sqrt((num_x2 - num_x1)**2 + (num_y2 - num_y1)**num_y1)  
                    
                    assign_variable(toks[i+1], str(dist))
                    
                    i+=11

        # -------------------------------------------- for DSTR
        elif toks[i] == "DSTR":

            err = 0

            # -------------------------------------------- for DSTR VAR only
            if err == 0:
            
                err = match_syntax(toks[i+1][0:3], "VAR")
                err = match_syntax(toks[i+2], ":")

                

                if err == 0:

                    lineNum +=1 

                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARE_INTEGER" + "\t\t\t\t" + "DSTR" + "\n")

                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    
                    assign_variable(toks[i+1], "")
                    i += 3

            # -------------------------------------------- for DSTR VAR WITH STRING only	
            
            if err == 1:

                err = match_syntax(toks[i+3][0:6], "STRING")
                err = match_syntax(toks[i+4], ":")

                if err == 0:

                    lineNum += 1

                    #DSTR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARE_INTEGER" + "\t\t\t\t" + "DINT" + "\n")
                    #VAR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+1][4:] + "\n")
                    #WITH
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "DECLARATION_ASSIGN_WITH_KEY " + "\t\t" + "WITH" + "\n")    
                    #STRING
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "STRING " + "\t\t\t\t\t" + toks[i+3][7:] + "\n")                    
                  
                    assign_variable(toks[i+1], toks[i+3][7:])
                    i+=5

        elif toks[i] == "STORE":

            err = 0

            # -------------------------------------------- for STORE NUM IN VAR only
            if err == 0:
            
                err = match_syntax(toks[i+1][0:3], "NUM")
                err = match_syntax(toks[i+2], "IN")
                err = match_syntax(toks[i+3][0:3], "VAR")

                if err == 0:

                    lineNum +=1 

                    #STORE
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "ASSIGN_KEY" + "\t\t\t\t" + "STORE" + "\n")
                    #NUM
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INTEGER" + "\t\t\t\t\t" + toks[i+1][4:] + "\n")
                    #IN
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "ASSIGN_VAR_KEY" + "\t\t\t\t" + "IN" + "\n")
                    #VAR
                    listOfLexemesAndTokens.append("[" + str(lineNum) + "]" + "\t\t\t" + "INDENTIFIER" + "\t\t\t\t" + toks[i+3][4:] + "\n")

                    assign_variable(toks[i+3], toks[i+1][4:])
                    i += 5

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
        print("Variable Name\t\t\tType\t\t\tValue ")
        variables_table()

        print("")
        break
    else:
        print("Please enter the file to be interpreted. Must be in .ipol extension.")

# ipolFile variable contains the name and extension of the file the user wants to interpret. Once
# the program receives the correct type of file, it will run the run_file() method. Else, the 
# program will keep asking the user to input an .ipol file.