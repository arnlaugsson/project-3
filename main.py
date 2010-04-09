# Compilers - Project 2
# Reykjavik University, Spring 2010
# Haukur Jonasson, Skuli Arnlaugsson

# This is the lexical analyser file as requested in part 5 of the assignment.
# -*- coding: utf-8 -*-
import os
import sys
from ply.lex import lex
from parse import compParser

def sep():
    print '--------------------------------------------------------------'


def main(*args):
    usage = """
    Python parser for a small Pascal-like language
    
    Preferred calling method:
        $ python main.py [inputFile] [options] [outputfile]

    Options:
      -  trace   :Show parsing trace
      -  tac     :Show TAC code
      -  table   :Show Symbol table

    OutputFile:
        If you want the TAC saved to file, enter the name
        of the file (not with ".tac").
        Example:
            python main.py pas_code_while output
        Will result in the TAC being saved to "output.tac"

    Example input files:
      -  pas_syntax_ok     
      -  pas_syntax_err
      -  functionCall

Using default input file."""
    # TODO: Add options for the TAC code (print to screen or file)
    # Generate our parser, with the given input

    tree, tac, table, writeToFile = False, False, False, False
    inputFile = 'example'
    outputFile = 'default.tac'


    if len(sys.argv) > 1:
        if sys.argv[1].lower() not in ('tree','tac','table'):
            inputFile = sys.argv[1]
            for param in sys.argv[1:]:
                if param.lower()    == 'trace'     : tree  = True
                elif param.lower()  == 'tac'     : tac   = True
                elif param.lower()  == 'table'   : table = True
                else:
                    outputFile = param + '.tac'
                    writeToFile = True
        """
        if sys.argv[1].lower() not in ('tree','tac','table'):
            inputFile = sys.argv[1]
            for param in sys.argv[2:]:
                if param.lower()    == 'trace'     : tree  = True
                elif param.lower()  == 'tac'     : tac   = True
                elif param.lower()  == 'table'   : table = True
                else:
                    outputFile = param + '.tac'
                    writeToFile = True
        else:
            for param in sys.argv[1:]:
                if param.lower()    == 'trace'     : tree  = True
                elif param.lower()  == 'tac'     : tac   = True
                elif param.lower()  == 'table'   : table = True
                else:
                    outputFile = param + '.tac'
                    writeToFile = True
        """
    else:
        print usage

    filename = 'input'+os.sep+inputFile
    outputFile = 'output'+os.sep+outputFile
    sep()
    print 'Using input "%s"'%filename
    parser = compParser(filename)

    # Start parsing!
    parser.parse(tree)

    fileHandler = open(filename)
    pointer = 0

    if len(parser.errors) > 0:
        sep()

    if not tree:
        while True:
            pointer += 1                                        
            line = fileHandler.readline()
            if not line: break
            lineErrors = []
            for error in parser.errors:
                if error.lineno == pointer:
                    lineErrors.append(error)

            if len(lineErrors) > 0:
                if pointer < 10: print ' %d:\t%s'%(pointer,line),
                else: print '%d:\t%s'%(pointer,line),
                for error in lineErrors:
                    print error.pointPrint()

    if tree: sep()

    if len(parser.errors) == 0:
        print 'No errors were detected.'
        sep()
        if table:   parser.SymbolTable.__repr__()
        if tac:     parser.printCode()
        if writeToFile:
            parser.printTacToFile(outputFile)
    else:
        sep()
        print '%d errors were encountered.'%len(parser.errors)
        sep()

if __name__ == '__main__':
	sys.exit(main(*sys.argv))