# Compilers - Project 1
# Reykjavik University, Spring 2010
# Haukur Jonasson, Skuli Arnlaugsson
# -*- coding: utf-8 -*-

import ply.lex as lex
from token import tokens
from token import reserved
from token import op_Type

# *** Global *********************************************************
#
# For error tracking we need to keep know how many letters have been
# read in previous lines.

previousLexPosLineCount = 0

# *** Simple Regular expressions *************************************
# Simple regular expressions for tokens that have no dataType and no
# opType. These can be defined directly by saying t_NAME = r'...' <=
# but this prevents us from adding special notes such as dt or opType.

t_tc_SEMICOL   = r';'
t_tc_COLON     = r':'
t_tc_COMMA     = r','
t_tc_DOTDOT    = r'\.\.'
t_tc_DOT       = r'\.'
t_tc_LPAREN    = r'\('
t_tc_LBRACKET  = r'\['
t_tc_RPAREN    = r'\)'
t_tc_RBRACKET  = r'\]'

# *** Regular Expression definitions *********************************
#
# Regular expressions for complex items, such as identifiers and
# operators that have more than one type.

letter              = r'[a-zA-Z]'
digit               = r'[0-9]'
digits              = digit + r'(' + digit + r')*'
int_num             = digits
optional_fraction   = r'\.'+int_num
optional_exponent   = r'e|E' + int_num
real_num            = int_num + r'(' + optional_fraction + r')?([Ee][+-]?'+int_num+')?'
identifier          = letter + r'(' + letter + r'|' + digit + r')*'

relop               = r'(\=)|(<\=)|(<)|(<>)|(>=)|(>)'
addop               = r'(\+)|(-)|(or)'
mulop               = r'(\*)|(/)|(div)|(mod)|(and)'
assignop            = r':\='

# For more complicated items, such as ID, Keywords, Number and Ops we
# need rules like the following:
@lex.TOKEN(relop)
def t_tc_RELOP(t):
    t.OpType = op_Type.get(t.value)
    t.DataType = 'dt_OP'
    return t

@lex.TOKEN(addop)
def t_tc_ADDOP(t):
    t.OpType = op_Type.get(t.value)
    t.DataType = 'dt_OP'
    return t

@lex.TOKEN(mulop)
def t_tc_MULOP(t):
    t.OpType = op_Type.get(t.value)
    t.DataType = 'dt_OP'
    return t

@lex.TOKEN(assignop)
def t_tc_ASSIGNOP(t):
    t.OpType = op_Type.get(t.value)
    t.DataType = 'dt_OP'
    return t


@lex.TOKEN(real_num)
def t_tc_REAL_NUM(t):
    # We are not allowed to return a tc_REAL or tc_INT, so we change
    # it to tc_NUMBER
    t.type = 'tc_NUMBER'
    t.DataType = 'dt_REAL'
    return t

@lex.TOKEN(int_num)
def t_tc_INT_NUM(t):
    # Same as above.
    t.type = 'tc_NUMBER'
    t.DataType = 'dt_INTEGER'
    t.OpType = 'op_NONE'
    return t    

@lex.TOKEN(identifier)
def t_tc_ID(t):
    global maxLenghtOfIdentifier
    # Check if lexeme is a reserved keyword:
    if t.value.lower() in reserved:
        # lexeme found in reserved, update type.
        t.type = reserved.get(t.value.lower())
        t.DataType = 'dt_KEYWORD'
    else:
        # Plain old ID, add the data-type flag.
        t.DataType = 'dt_ID'
    return t

    
def t_newline(t):
    r'\n+'
    # Update the read lexpos counter and lineno count.
    global previousLexPosLineCount
    previousLexPosLineCount = t.lexpos - 1
    t.lexer.lineno += len(t.value)


# Ignore white-spaces.
t_ignore  = ' \t'
  
def t_COMMENT(t):
    # Ignore comments starting with '{' and ending with '}'.
    r'\{.*\}'
    pass

def t_error(t):
    # Skip o
    t.type = 'tc_ERROR'
    t.DataType = 'dt_NONE'
    global previousLexPosLineCount
    t.columnno = t.lexpos - previousLexPosLineCount
    t.lexer.skip(1)
    return t