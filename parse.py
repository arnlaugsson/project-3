# Compilers - Project 2
# Reykjavik University, Spring 2010
# Haukur Jonasson, Skuli Arnlaugsson

#
# -*- coding: utf-8 -*-
import sys
from scanner import Scanner
from token import *
import token
import code
from synchronizingSets import syncsets

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
        print "\t"+" "*(self.columnno-2) + "^--- " + self.message

class Parser:
    def __init__(self,input,output):
        self.__scanner = Scanner(input)
        self.__code = code(output)
        self.__currentToken = None
        self.__foundError = False
        self.__errorInFunction = ''
        self.errors = []
        self.skipped = []

    def parse(self):
        self.__getToken()
        self.__Program()

    def close(self):
        self.__code.close()

    def __getToken(self):
        self.__currentToken = self.__scanner.nextToken()

    def __callersname(self):
        return sys._getframe(2).f_code.co_name

    def __addError(self,token,message):
        self.errors.append(Error(token.lineno,token.columnno,message))


    def __recover(self):
        skip = True
        for tc in syncsets[self.__errorInFunction]:
            if self.__currentToken.TokenCode != tc:
                self.__getToken()
            else:
                # Token found in sync set
                skip = False
                break
        if skip:
            self.__getToken()

        else:
            self.__foundError = False
            self.__errorInFunction = ''


    def __match(self,expectedIn):
        if self.__currentToken.TokenCode == 'tc_ERROR':
            message = 'Illegal symbol'
            while self.__currentToken.TokenCode == 'tc_ERROR':
                self.__addError(self.__currentToken,message)
                self.__getToken()

        if self.__currentToken.TokenCode != expectedIn:
            callFunc = self.__callersname()
            if self.__currentToken.TokenCode == 'tc_ID':
                recTC = 'an identifier'
            elif self.__currentToken.TokenCode == 'tc_NUMBER':
                recTC = 'a number'
            else:
                recTC = '"'+self.__currentToken.DataValue[0]+'"'
            message = 'Expected %s not %s. (%s)'%(expectedIn[3:],recTC,callFunc[2:])
            self.__addError(self.__currentToken,message)
            self.__foundError = True
            self.__errorInFunction = callFunc

            if recTC in syncsets[callFunc]:
                # If the current token is in the follow set of the calling function
                # We do not want to throw it out.
                return
        else:
            self.__foundError = False
            self.__errorInFunction = ''
        self.__getToken()


    def __Program(self):
        # tc_EOF
        self.__ProgramDefinition()
        if self.__foundError: self.__recover()

        self.__match('tc_SEMICOL')

        self.__Declarations()
        if self.__foundError: self.__recover()


        self.__SubprogramDeclarations()
        if self.__foundError: self.__recover()


        self.__CompoundStatement()
        if self.__foundError: self.__recover()

        self.__match('tc_DOT')

    def __ProgramDefinition(self):
        self.__match('tc_PROGRAM')
        self.__match('tc_ID')
        self.__match('tc_LPAREN')

        self.__IdentifierList()
        if self.__foundError: self.__recover()

        self.__match('tc_RPAREN')

    def __IdentifierList(self):
        self.__match('tc_ID')
        self.__IdentifierListRest()

    def __IdentifierListRest(self):
        if self.__currentToken.TokenCode == 'tc_COMMA':
            self.__match('tc_COMMA')
            self.__IdentifierList()

    def __IdentifierListAndType(self):
        self.__IdentifierList()
        self.__match('tc_COLON')
        self.__Type()

    def __Declarations(self):
        if self.__currentToken.TokenCode == 'tc_VAR':
            self.__match('tc_VAR')
            self.__IdentifierListAndType()
            if self.__foundError: self.__recover()
            self.__match('tc_SEMICOL')
            self.__Declarations()

    def __Type(self):
        self.__TypeArray()
        self.__StandardType()


    def __TypeArray(self):
        if self.__currentToken.TokenCode == 'tc_ARRAY':
            self.__match('tc_ARRAY')
            if not self.__foundError: self.__match('tc_LBRACKET')
            if not self.__foundError: self.__match('tc_NUMBER')
            if not self.__foundError: self.__match('tc_DOTDOT')
            if not self.__foundError: self.__match('tc_NUMBER')
            if not self.__foundError: self.__match('tc_RBRACKET')
            if not self.__foundError: self.__match('tc_OF')


    def __StandardType(self):
        if self.__currentToken.TokenCode == 'tc_INTEGER':
            self.__match('tc_INTEGER')
        elif self.__currentToken.TokenCode == 'tc_REAL':
            self.__match('tc_REAL')

    def __SubprogramDeclarations(self):
        if self.__currentToken.TokenCode in ('tc_FUNCTION','tc_PROCEDURE'):
            self.__SubprogramDeclaration()
            if self.__foundError: self.__recover()
            self.__match('tc_SEMICOL')
            self.__SubprogramDeclarations()

    def __SubprogramDeclaration(self):
        self.__SubprogramHead()
        if self.__foundError: self.__recover()
        self.__match('tc_SEMICOL')
        self.__Declarations()
        if self.__foundError: self.__recover()
        self.__CompoundStatement()

    def __SubprogramHead(self):
        if self.__currentToken.TokenCode == 'tc_FUNCTION':
            self.__Function()
        elif self.__currentToken.TokenCode == 'tc_PROCEDURE':
            self.__Procedure()

    def __Function(self):
        self.__match('tc_FUNCTION')
        if not self.__foundError: self.__match('tc_ID')
        self.__Arguments()
        if self.__foundError: self.__recover()
        self.__match('tc_COLON')
        self.__StandardType()

    def __Procedure(self):
        self.__match('tc_PROCEDURE')
        if not self.__foundError: self.__match('tc_ID')
        self.__Arguments()

    def __Arguments(self):
        if self.__currentToken.TokenCode == 'tc_LPAREN':
            self.__match('tc_LPAREN')
            self.__ParameterList()
            if self.__foundError: self.__recover()
            self.__match('tc_RPAREN')

    def __ParameterList(self):
        self.__IdentifierListAndType()
        if self.__foundError: self.__recover()
        self.__ParameterListRest()

    def __ParameterListRest(self):
        if self.__currentToken.TokenCode == 'tc_SEMICOL':
            self.__match('tc_SEMICOL')
            self.__IdentifierListAndType()
            if self.__foundError: self.__recover()
            self.__ParameterListRest()

    def __CompoundStatement(self):
        self.__match('tc_BEGIN')
        self.__OptionalStatements()
        if self.__foundError: self.__recover()
        self.__match('tc_END')

    def __OptionalStatements(self):
        self.__StatementList()
        if self.__foundError: self.__recover()

    def __StatementList(self):
        self.__Statement()
        if self.__foundError: self.__recover()
        self.__StatementListRest()

    def __StatementListRest(self):
        if self.__currentToken.TokenCode == 'tc_SEMICOL':
            self.__match('tc_SEMICOL')
            self.__StatementList()

    def __Statement(self):
        if self.__currentToken.TokenCode == 'tc_ID':
            self.__match('tc_ID')
            self.__IdOrProcedureStatement()
        elif self.__currentToken.TokenCode == 'tc_BEGIN':
            self.__CompoundStatement()
        elif self.__currentToken.TokenCode == 'tc_IF':
            self.__IfStatement()
        elif self.__currentToken.TokenCode == 'tc_WHILE':
            self.__WhileStatement()

    def __ArrayReference(self):
        self.__match('tc_LBRACKET')
        self.__Expression()
        self.__match('tc_RBRACKET')


    def __IdOrProcedureStatement(self):
        if self.__currentToken.TokenCode == 'tc_ASSIGNOP':
            self.__match('tc_ASSIGNOP')
            self.__Expression()
        elif self.__currentToken.TokenCode == 'tc_LBRACKET':
            self.__ArrayReference()
            if self.__foundError: self.__recover()
            self.__match('tc_ASSIGNOP')
            self.__Expression()
        elif self.__currentToken.TokenCode == 'tc_LPAREN':
            self.__match('tc_LPAREN')
            self.__ExpressionList()
            if self.__foundError: self.__recover()
            self.__match('tc_RPAREN')

    def __IfStatement(self):
        self.__match('tc_IF')
        self.__Expression()
        self.__match('tc_THEN')
        self.__Statement()
        self.__match('tc_ELSE')
        self.__Statement()

    def __WhileStatement(self):
        self.__match('tc_WHILE')
        self.__Expression()
        if self.__foundError: self.__recover()
        self.__match('tc_DO')
        self.__Statement()


    def __ExpressionList(self):
        self.__Expression()
        if self.__foundError: self.__recover()
        self.__ExpressionListRest()

    def __ExpressionListRest(self):
        if self.__currentToken.TokenCode == 'tc_COMMA':
            self.__match('tc_COMMA')
            self.__ExpressionList()

    def __Expression(self):
        self.__SimpleExpression()
        if self.__foundError: self.__recover()
        self.__ExpressionRest()

    def __ExpressionRest(self):
        if self.__currentToken.TokenCode == 'tc_RELOP':
            self.__match('tc_RELOP')
            self.__SimpleExpression()

    def __SimpleExpression(self):
        if self.__currentToken.TokenCode == 'tc_ADDOP':
            self.__match('tc_ADDOP')
        self.__Term()
        if self.__foundError: self.__recover()
        self.__SimpleExpressionRest()

    def __SimpleExpressionRest(self):
        if self.__currentToken.TokenCode == 'tc_ADDOP':
            self.__match('tc_ADDOP')
            self.__Term()
            if self.__foundError: self.__recover()
            self.__SimpleExpressionRest()

    def __Term(self):
        self.__Factor()
        if self.__foundError: self.__recover()
        self.__TermRest()

    def __TermRest(self):
        if self.__currentToken.TokenCode == 'tc_MULOP':
            self.__match('tc_MULOP')
            self.__Factor()
            if self.__foundError: self.__recover()
            self.__TermRest()

    def __Factor(self):
        if self.__currentToken.TokenCode == 'tc_LPAREN':
            self.__match('tc_LPAREN')
            self.__Expression()
            if self.__foundError: self.__recover()
            self.__match('tc_RPAREN')
        elif self.__currentToken.TokenCode == 'tc_NOT':
            self.__match('tc_NOT')
            self.__Factor()
        elif self.__currentToken.TokenCode == 'tc_NUMBER':
            self.__match('tc_NUMBER')
        elif self.__currentToken.TokenCode == 'tc_ID':
            self.__match('tc_ID')
            self.__FactorRest()

    def __FactorRest(self):
        if self.__currentToken.TokenCode == 'tc_LPAREN':
            self.__match('tc_LPAREN')
            self.__ExpressionList()
            if self.__foundError: self.__recover()
            self.__match('tc_RPAREN')
        elif self.__currentToken.TokenCode == 'tc_LBRACKET':
            self.__ArrayReference()