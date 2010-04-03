# Compilers - Project 1
# Reykjavik University, Spring 2010
# Haukur Jonasson, Skuli Arnlaugsson

# This is the lexical analyser file as requested in part 4 of the assignment.
# -*- coding: utf-8 -*-
SYMMAX = 500

class SymbolTableEntry:
    def __init__(self, lexeme):
        self.m_lexeme = lexeme

    def getLexeme(self):
        return self.m_lexeme

class SymbolTable:
    def __init__(self):
        self.SymbolTable = []
        self.lastEntry = 1

    def insert(self, lexeme):
        if len(self.SymbolTable) < SYMMAX:
            entry = SymbolTableEntry(lexeme)
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
        format_width = 10

        print '\n\nAnd for the symboltable :\n'
        print ' Entry'.rjust(format_width) + '\t\t' + ' Lexeme'.rjust(format_width)
        width = 10

        for i,entry in enumerate(self.SymbolTable):
            print '%s\t\t%s'%(str(i).rjust(format_width),entry.getLexeme().rjust(format_width))






