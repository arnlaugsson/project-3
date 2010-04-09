# Compilers - Project 3
# Reykjavik University, Spring 2010
# Haukur Jonasson, Skuli Arnlaugsson

import os
import sys
from ply.lex import lex
from parse import compParser

def sep():
    print '--------------------------------------------------------------'

def checkIfExists(filename):
    import os
    return os.path.exists(filename)

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
"""

    tree, tac, table, writeToFile = False, False, False, False
    inputFile = 'pas_code_if'
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
    else:
        print usage
        print 'Using the default input file.'

    filename = 'input'+os.sep+inputFile
    outputFile = 'output'+os.sep+outputFile
    sep()
    print 'Using input "%s"'%filename

    if checkIfExists(filename):
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

    else:
        print 'File: %s was not found.'%filename
        print usage

if __name__ == '__main__':
	sys.exit(main(*sys.argv))