# Compilers - Project 3
# Reykjavik University, Spring 2010
# Haukur Jonasson, Skuli Arnlaugsson

# -*- coding: utf-8 -*-
import sys
from scanner import Scanner
from token import *
from symbolTable import *
import token
from synchronizingSets import syncsets
import code

import symbolTable
depth = 0
def trackDepth(func):
    def wrapper(classInstance,input=None):
        global depth
        if classInstance.printTree: print depth,'\t','    '*depth,'Opening:', func.__name__
        depth += 1
        value = func(classInstance,input)
        depth -= 1
        if classInstance.printTree: print depth,'\t','    '*depth,'Closing:',  func.__name__
        return value
    return wrapper

class Error:
    """ An instance of the Error class is a parser error encountered during parsing.
        It has three attributes:
            lineno, charnum and the error message.
    """
    def __init__(self, lineno, columnno, message):
        self.lineno = lineno
        self.columnno = columnno
        self.message = message
    def __repr__(self):
        return 'Line %d:%d: \t%s'%(self.lineno,self.columnno,self.message)
    def pointPrint(self):
        return "\t"+" "*(self.columnno-2) + "^ " + self.message

class Parser:
    # TODO: Add code generation to the following parsing functions:
    #   Expression, SimpleExpression, Term, Termrest, Factor, FactorRest
    # TODO: create functions: opToCode, getSymbolTable, getCode
    global depth
    def __init__(self,input):
        self.__scanner = Scanner(input)
        self.__code = code.Code()
        self.__currentToken = None
        self.__foundError = False
        self.__errorInFunction = ''
        self.__errorDepth = None
        self.printTree = False
        self.errors = []
        self.__tempList = []

        self.SymbolTable = symbolTable.SymbolTable()
        self.__initializeSymbolTable()

    def __initializeSymbolTable(self):
        self.SymbolTable.insert('0','tc_CONST')
        self.SymbolTable.insert('1','tc_CONST')

    def __newTemp(self):
        # Create a new temp variable, insert into SymbolTable and return
        varName = self.__code.newTemp()
        stPointer = self.SymbolTable.insert(varName,'tc_VAR')
        self.__code.generate('cd_VAR',None,None,self.SymbolTable.SymbolTable[stPointer].m_lexeme)
        return stPointer

    def __newLabel(self):
        labelName = self.__code.newLabel()
        stPointer = self.SymbolTable.insert(labelName,'tc_LABEL')
        self.__code.generate('cd_LABEL',None,None,self.SymbolTable.SymbolTable[stPointer].m_lexeme)

    def printCode(self):
        self.__code.__repr__()
        
    def parse(self,bool=False):
        if bool: self.printTree = True
        self.__getToken()
        self.__Program()

    def __getTokenCode(self):
        return self.__currentToken.TokenCode


    def __getToken(self):
        self.__currentToken = self.__scanner.nextToken()
        if self.__currentToken == None: return False

        if self.__getTokenCode() == 'tc_ID':
            entry = self.SymbolTable.lookup(self.__currentToken.DataValue[0].upper())

            if entry == -1 :  # -1 means not found in table
                # Entry does not exist -> add it!
                num = self.SymbolTable.insert(self.__currentToken.DataValue[0].upper(),self.__getTokenCode())

                # Associate the token with the entry
                self.__currentToken.setSymTabEntry(num)
            else:
                # Token exists:
                # Associate the token with the entry
                self.__currentToken.setSymTabEntry(entry)


        elif self.__getTokenCode() == 'tc_NUMBER':
            # Same as for entry ..
            entry = self.SymbolTable.lookup(self.__currentToken.DataValue[0].upper())
            if entry == -1:
                num = self.SymbolTable.insert(self.__currentToken.DataValue[0].upper(),self.__getTokenCode())
                self.__currentToken.setSymTabEntry(num)
            else:
                self.__currentToken.setSymTabEntry(entry)

        return True

    def __callersname(self):
        return sys._getframe(2).f_code.co_name



    def __addError(self,token,message):
        self.errors.append(Error(token.lineno,token.columnno,message))


    def __recover(self):
        global depth
        if self.printTree: print '\t','    '*depth,'->Trying to recover.'
        if len(syncsets[self.__errorInFunction]) == 0: return
        while True:
            if not self.__getTokenCode() in syncsets[self.__errorInFunction]:

                if self.printTree: print '\t','    '*depth, '-->Discarded %s'%self.__currentToken.DataValue[0]
                result = self.__getToken()
                if not result:
                    if self.printTree: print '\t','  '*(depth),'->Reached end of input, could not recover.'
                    break
            else:
                if self.printTree: print '\t','    '*depth, '-->Match: %s with %s'%(self.__getTokenCode(),self.__getTokenCode())
                self.__foundError = False
                self.__errorInFunction = ''
                self.__errorDepth = None
                if self.printTree: print '\t','    '*depth,'->Recovered!'
                #self.__getToken()
                break


    def __match(self,expectedIn):

        # To track error depth - we do not want to recover from sibling or
        # parent's functions.
        global depth

        # If we encounter an illegal symbol, skip passed it and report.
        if self.__getTokenCode() == 'tc_ERROR':
            message = 'Illegal character'
            while self.__getTokenCode() == 'tc_ERROR':
                self.__addError(self.__currentToken,message)
                self.__getToken()

        # If we know there is an error, check depth and exit if depth is the same
        # or greater. Recover if error depth is smaller.
        if self.__foundError:
            if self.__errorDepth < depth:
                if self.__getTokenCode() in syncsets[self.__errorInFunction]:
                    if self.printTree: print '\t','    '*depth,'--->Skipping', self.__getTokenCode(), 'because of the Error flag.'
                    return
            else:
                #if self.printTree: print '\t','    '*depth,self.__errorInFunction, syncsets[self.__errorInFunction]
                self.__recover()
                self.__getToken()
                return

        if self.printTree: print '\t','    '*depth,'-->Match:', expectedIn, 'with', self.__getTokenCode()

        # Wrong token to what we expected. Report error.
        if self.__getTokenCode() != expectedIn:
            if self.__getTokenCode() == 'tc_ID2LONG' and expectedIn == 'tc_ID':
                message = 'Identifier too long (max 32 characters)'
                self.__addError(self.__currentToken,message)
                self.__getToken()
                return
            callFunc = self.__callersname()
            if self.__getTokenCode() == 'tc_ID':
                recTC = 'an identifier'
            elif self.__getTokenCode() == 'tc_NUMBER':
                recTC = 'a number'
            else:
                recTC = '"'+self.__currentToken.DataValue[0]+'"'
            message = 'Expected %s (%s)'%(token.tc2Name[expectedIn],callFunc)
            if self.printTree: print '\t','    '*depth,'Error: Could not match at depth %d'%depth
            self.__addError(self.__currentToken,message)
            self.__foundError = True
            self.__errorInFunction = callFunc
            self.__errorDepth = depth

            if self.__getTokenCode() in syncsets[callFunc]: return
            if self.printTree: print '\t','    '*depth,'Discarding unexpected token "%s"'%self.__currentToken.DataValue[0]
            self.__getToken()

        else: self.__getToken()

    def __missingSingle(self,expTC):
        try:
            name = token.tc2Name[expTC]
        except:
            name = expTC
        message = 'Expected %s'%name
        self.__addError(self.__currentToken,message)

    @trackDepth
    def __Program(self,input=None):
        # ProgramDefinition returns the program name (string)
        programName = self.__ProgramDefinition()

        # Reset tempList in between - since we do not want to
        # add the ProgramDefinition identifier-list to our TAC anyway.
        self.__tempList = []
        
        if self.__getTokenCode() == 'tc_SEMICOL':
            self.__match('tc_SEMICOL')
        else:
            self.__missingSingle('tc_SEMICOL')
        
        self.__Declarations()
        # Now generate TAC for the program variables
        self.__code.generateVariables(self.__tempList)
        # And flush list.
        self.__tempList = []

        if self.__foundError:
            self.__recover()
            self.__getToken()

        self.__code.generate('cd_GOTO',None,None,programName)

        self.__SubprogramDeclarations()


        self.__code.generate('cd_LABEL',None,None,programName)
        self.__CompoundStatement()
        self.__match('tc_DOT')
        self.__code.generate('cd_RETURN',None,None,None)        

    @trackDepth
    def __ProgramDefinition(self,input=None):
        self.__match('tc_PROGRAM')
        pointer = self.__currentToken.getSymTabEntry()
        name = self.SymbolTable.SymbolTable[pointer].m_lexeme
        self.__match('tc_ID')
        self.__match('tc_LPAREN')
        self.__IdentifierList()
        self.__match('tc_RPAREN')
        return name

    @trackDepth
    def __IdentifierList(self,input=None):
        lexeme = self.SymbolTable.SymbolTable[self.__currentToken.getSymTabEntry()].m_lexeme
        self.__tempList.append(lexeme)
        self.__match('tc_ID')
        
        if self.__currentToken.TokenCode == 'tc_COMMA': self.__IdentifierListRest()

    @trackDepth
    def __IdentifierListRest(self,input=None):
        self.__match('tc_COMMA')
        self.__IdentifierList()

    @trackDepth
    def __IdentifierListAndType(self,input=None):
        self.__IdentifierList()
        self.__match('tc_COLON')
        self.__Type()

    @trackDepth
    def __Declarations(self,input=None):
        if self.__currentToken.TokenCode == 'tc_VAR':
            self.__match('tc_VAR')
            self.__IdentifierListAndType()
            self.__match('tc_SEMICOL')
            self.__Declarations()

    @trackDepth
    def __Type(self,input=None):
        if self.__currentToken.TokenCode == 'tc_ARRAY':self.__TypeArray()
        self.__StandardType()


    @trackDepth
    def __TypeArray(self,input=None):
        self.__match('tc_ARRAY')
        self.__match('tc_LBRACKET')
        self.__match('tc_NUMBER')
        self.__match('tc_DOTDOT')
        self.__match('tc_NUMBER')
        self.__match('tc_RBRACKET')
        self.__match('tc_OF')


    @trackDepth
    def __StandardType(self,input=None):
        if self.__currentToken.TokenCode == 'tc_INTEGER':
            self.__match('tc_INTEGER')
        elif self.__currentToken.TokenCode == 'tc_REAL':
            self.__match('tc_REAL')
        else:
            if not self.__currentToken.TokenCode == 'tc_SEMICOL':
                self.__match('tc_INTEGER')

    @trackDepth
    def __SubprogramDeclarations(self,input=None):
        if self.__currentToken.TokenCode in ('tc_FUNCTION','tc_PROCEDURE'):
            self.__SubprogramDeclaration()
            self.__match('tc_SEMICOL')
            self.__code.generate('cd_RETURN',None,None,None)
            self.__SubprogramDeclarations()

    @trackDepth
    def __SubprogramDeclaration(self,input=None):
        self.__SubprogramHead()
        self.__match('tc_SEMICOL')

        self.__Declarations()
        self.__code.generateVariables(self.__tempList)
        self.__tempList = []

        self.__CompoundStatement()

    @trackDepth
    def __SubprogramHead(self,input=None):
        if self.__currentToken.TokenCode == 'tc_FUNCTION':
            self.__Function()

        elif self.__currentToken.TokenCode == 'tc_PROCEDURE':
            self.__Procedure()

    @trackDepth
    def __Function(self,input=None):
        self.__match('tc_FUNCTION')
        pointer = self.__currentToken.getSymTabEntry()
        self.__code.generate('cd_LABEL',None,None,self.SymbolTable.SymbolTable[pointer].m_lexeme)        


        self.__match('tc_ID')
        self.__Arguments()
        self.__match('tc_COLON')
        self.__StandardType()

    @trackDepth
    def __Procedure(self,input=None):
        self.__match('tc_PROCEDURE')
        pointer = self.__currentToken.getSymTabEntry()
        self.__code.generate('cd_LABEL',None,None,self.SymbolTable.SymbolTable[pointer].m_lexeme)        

        self.__match('tc_ID')
        self.__Arguments()

    @trackDepth
    def __Arguments(self,input=None):
        if self.__currentToken.TokenCode == 'tc_LPAREN':
            self.__match('tc_LPAREN')

            self.__ParameterList()
            self.__code.generateFParams(self.__tempList)
            self.__tempList = []

            self.__match('tc_RPAREN')

    @trackDepth
    def __ParameterList(self,input=None):
        self.__IdentifierListAndType()
        self.__ParameterListRest()

    @trackDepth
    def __ParameterListRest(self,input=None):
        if self.__currentToken.TokenCode == 'tc_SEMICOL':
            self.__match('tc_SEMICOL')
            self.__IdentifierListAndType()
            self.__ParameterListRest()

    @trackDepth
    def __CompoundStatement(self,input=None):
        self.__match('tc_BEGIN')
        self.__OptionalStatements()
        self.__match('tc_END')

    @trackDepth
    def __OptionalStatements(self,input=None):
        self.__StatementList()

    @trackDepth
    def __StatementList(self,input=None):
        self.__Statement()
        self.__StatementListRest()

    @trackDepth
    def __StatementListRest(self,input=None):
        if self.__currentToken.TokenCode == 'tc_SEMICOL':
            self.__match('tc_SEMICOL')
            self.__Statement()
            self.__StatementListRest()

    @trackDepth
    def __Statement(self,input=None):
        if self.__currentToken.TokenCode == 'tc_BEGIN':
            self.__CompoundStatement()

        elif self.__currentToken.TokenCode == 'tc_IF':
            self.__IfStatement()

        elif self.__currentToken.TokenCode == 'tc_WHILE':
            self.__WhileStatement()
        elif self.__currentToken.TokenCode == 'tc_ID':
            pointer = self.__currentToken.getSymTabEntry()
            self.__match('tc_ID')
            self.__IdOrProcedureStatement(pointer)
        else:
            self.__match('tc_STATEMENT')



    @trackDepth
    def __ArrayReference(self,input=None):
        self.__match('tc_LBRACKET')
        self.__Expression()
        self.__match('tc_RBRACKET')


    @trackDepth
    def __IdOrProcedureStatement(self, prevEntryPointer):
        if self.__currentToken.TokenCode == 'tc_ASSIGNOP':
            self.__match('tc_ASSIGNOP')
            outcomePointer = self.__Expression()
            self.__code.generate('cd_ASSIGN',self.SymbolTable.SymbolTable[outcomePointer].m_lexeme,None,self.SymbolTable.SymbolTable[prevEntryPointer].m_lexeme)

        elif self.__currentToken.TokenCode == 'tc_LBRACKET':
            self.__ArrayReference()
            self.__match('tc_ASSIGNOP')
            self.__Expression()


        elif self.__currentToken.TokenCode == 'tc_LPAREN':
            self.__match('tc_LPAREN')
            self.__tempList = []            
            self.__ExpressionList()
            self.__code.generateAParams(self.__tempList)
            self.__tempList = []
            self.__code.generate('cd_CALL',self.SymbolTable.SymbolTable[prevEntryPointer].m_lexeme,None,None)
            self.__match('tc_RPAREN')

    @trackDepth
    def __IfStatement(self,input=None):
        self.__match('tc_IF')

        end     = self.__code.newLabel()
        ifFalse = self.__code.newLabel()
        temp    = self.__code.newTemp()


        ifTrue = self.__Expression()

        compare = self.__code.newLabel()

        self.__code.generate('cd_ASSIGN',self.SymbolTable.SymbolTable[self.SymbolTable.lookup('0')].m_lexeme,None,temp)
        self.__code.generate('cd_GOTO',None,None,compare)

        self.__code.generate('cd_LABEL',None,None,ifTrue)
        self.__code.generate('cd_ASSIGN',self.SymbolTable.SymbolTable[self.SymbolTable.lookup('1')].m_lexeme,None,temp)

        self.__code.generate('cd_LABEL',None,None,compare)
        self.__code.generate('cd_EQ',temp,self.SymbolTable.SymbolTable[self.SymbolTable.lookup('0')].m_lexeme,ifFalse)


        if self.__currentToken.TokenCode == 'tc_THEN':
            self.__match('tc_THEN')
        else:
            self.__missingSingle('tc_THEN')

        self.__Statement()

        self.__code.generate('cd_GOTO',None,None,end)

        self.__match('tc_ELSE')

        self.__code.generate('tc_LABEL',None,None,ifFalse)
        self.__Statement()
        self.__code.generate('tc_LABEL',None,None,end)

    @trackDepth
    def __WhileStatement(self,input=None):
        self.__match('tc_WHILE')
        self.__Expression()
        if self.__currentToken.TokenCode == 'tc_DO':
            self.__match('tc_DO')
        else:
            self.__missingSingle('tc_DO')
        self.__Statement()


    @trackDepth
    def __ExpressionList(self,input=None):
        expr = self.__Expression()
        self.__tempList.append(self.SymbolTable.SymbolTable[expr].m_lexeme)
        self.__ExpressionListRest()


    @trackDepth
    def __ExpressionListRest(self,input=None):
        if self.__currentToken.TokenCode == 'tc_COMMA':
            self.__match('tc_COMMA')
            expr = self.__Expression()
            self.__tempList.append(self.SymbolTable.SymbolTable[expr].m_lexeme)
            self.__ExpressionListRest()

    @trackDepth
    def __Expression(self,input=None):
        entry = self.__SimpleExpression()
        entry = self.__SimpleExpressionRelop(entry)
        return entry

    @trackDepth
    def __SimpleExpressionRelop(self,prevEntryPointer=None):
        if self.__currentToken.TokenCode == 'tc_RELOP':
            op = self.__currentToken.DataValue[1]
            self.__match('tc_RELOP')
            label = self.__code.newLabel()
            entry = self.__SimpleExpression()
            self.__code.generate(op,self.SymbolTable.SymbolTable[prevEntryPointer].m_lexeme,self.SymbolTable.SymbolTable[entry].m_lexeme,label)
            return label            
        else:
            return prevEntryPointer

    @trackDepth
    def __SimpleExpression(self,input=None):
        uminus = False
        if self.__currentToken.TokenCode == 'tc_ADDOP':
            op = self.__currentToken.DataValue[1]
            if op == 'op_MINUS':
                uminus = True
            self.__match('tc_ADDOP')

        entry = self.__Term()

            
        entry = self.__SimpleExpressionAddop(entry)
        if uminus:
            temp = self.__newTemp()
            self.__code.generate('cd_UMINUS',self.SymbolTable.SymbolTable[entry].m_lexeme,None,self.SymbolTable.SymbolTable[temp].m_lexeme)
            entry = temp

        return entry
        


    @trackDepth
    def __SimpleExpressionAddop(self,prevEntryPointer):
        if self.__currentToken.TokenCode == 'tc_ADDOP':
            op = self.__currentToken.DataValue[1]
            self.__match('tc_ADDOP')
            entry = self.__Term()
            entry = self.__SimpleExpressionAddop(entry)
            pointer = self.__newTemp()
            self.__code.generate(op,self.SymbolTable.SymbolTable[prevEntryPointer].m_lexeme,self.SymbolTable.SymbolTable[entry].m_lexeme,self.SymbolTable.SymbolTable[pointer].m_lexeme)
            return pointer
        else:
            return prevEntryPointer

    @trackDepth
    def __Term(self,input=None):
        entry = self.__Factor()
        entry = self.__TermRest(entry)
        return entry

    @trackDepth
    def __TermRest(self,prevEntryPointer=None):
        if self.__currentToken.TokenCode == 'tc_MULOP':
            op = self.__currentToken.DataValue[1]
            self.__match('tc_MULOP')
            entry = self.__Term()
            temp = self.__newTemp()
            self.__code.generate(op,self.SymbolTable.SymbolTable[prevEntryPointer].m_lexeme,self.SymbolTable.SymbolTable[entry].m_lexeme,self.SymbolTable.SymbolTable[temp].m_lexeme)
            return temp
        else:
            return prevEntryPointer

    @trackDepth
    def __Factor(self,input=None):
        if self.__currentToken.TokenCode == 'tc_LPAREN':
            self.__match('tc_LPAREN')
            entry = self.__Expression()
            self.__match('tc_RPAREN')
        elif self.__currentToken.TokenCode == 'tc_NOT':
            self.__match('tc_NOT')
            entry =self.__Factor()
        elif self.__currentToken.TokenCode == 'tc_NUMBER':
            entry = self.__currentToken.getSymTabEntry()
            self.__match('tc_NUMBER')
        elif self.__currentToken.TokenCode == 'tc_ID':
            entry = self.__currentToken.getSymTabEntry()
            self.__match('tc_ID')
            entry = self.__FactorRest(entry)
        else:
            self.__missingSingle('an identifier')
            entry =  0
        return entry

    @trackDepth
    def __FactorRest(self,prevEntry):
        if self.__currentToken.TokenCode == 'tc_LPAREN':
            self.__match('tc_LPAREN')
            self.__tempList = []            
            self.__ExpressionList()
            self.__code.generateAParams(self.__tempList)
            self.__tempList = []
            self.__code.generate('cd_CALL',self.SymbolTable.SymbolTable[prevEntry].m_lexeme,None,None)
            self.__match('tc_RPAREN')

        elif self.__currentToken.TokenCode == 'tc_LBRACKET':
            self.__ArrayReference()

        return prevEntry


