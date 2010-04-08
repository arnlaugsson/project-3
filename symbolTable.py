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

class EntryList:
    """
    Not needed in our impl. - we use a list, not a linked list.
    """
    pass

class SymbolTable:
    def __init__(self):
        self.SymbolTable = []
        self.lastEntry = 0

    def insert(self,lexeme,tokenCode):
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
        width = 20

        print 'Entry'.rjust(width) + ' Lexeme'.rjust(width)
        print '----------'.rjust(width) + '----------'.rjust(width)

        for i,entry in enumerate(self.SymbolTable):
            print str(i).rjust(width) + entry.getLexeme().rjust(width)

        print '--------------------------------------------------------------'





