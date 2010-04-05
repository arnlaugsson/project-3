# Compilers - Project 3
# Reykjavik University, Spring 2010
# Haukur Jonasson, Skuli Arnlaugsson

# This is the lexical analyser file as requested in part 4 of the assignment.
# -*- coding: utf-8 -*-
SYMMAX = 500

class SymbolTableEntry:
    def __init__(self, lexeme, tokenCode):
        self.m_lexeme = lexeme
        self.m_TokenCode = tokenCode

    def getLexeme(self):
        return self.m_lexeme

    def getTC(self):
        return self.m_TokenCode[3:]

class SymbolTable:
    def __init__(self):
        self.SymbolTable = []
        self.lastEntry = 1

    def insert(self, lexeme,tokenCode):
        if len(self.SymbolTable) < SYMMAX:
            entry = SymbolTableEntry(lexeme,tokenCode)
            self.SymbolTable.append(entry)
            self.lastEntry += 1
            return self.lastEntry -1
        else:
            print 'Maximum number of entries in SymbolTable reached. Nothing addedd.'
            return -1

    def lookup(self, lexeme):
        for entry in range(0,len(self.SymbolTable)):
            if self.SymbolTable[entry].getLexeme() == lexeme:
                return entry
        return -1

    def __repr__(self):
        format_num = 5
        format_lex = 10

        print '  -------------------------------'
        print '            SYMBOLTABLE'
        print '  Entry'.rjust(format_num) + '\t'+ 'TC' + '\t' + ' Lexeme'.rjust(format_lex)
        print '  -------------------------------'
        for i,entry in enumerate(self.SymbolTable):
            print '%s\t%s\t%s'%(str(i).rjust(format_num),entry.getTC(),entry.getLexeme().rjust(format_lex))

        print '  -------------------------------'





