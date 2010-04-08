width = 15

CodeOp = [ 'cd_LABEL', 'cd_UMINUS', 'cd_ASSIGN',
           'cd_ADD', 'cd_SUB', 'cd_MULT', 'cd_DIVIDE',
           'cd_DIV', 'cd_MOD', 'cd_OR', 'cd_AND', 'cd_NOT',
           'cd_LT', 'cd_LE', 'cd_GT', 'cd_GE', 'cd_EQ', 'cd_NE',
		   'cd_GOTO', 'cd_CALL', 'cd_APARAM', 'cd_FPARAM', 'cd_VAR',
           'cd_RETURN', 'cd_NOOP']

class Quadruple:
    def __init__(self, op, arg1, arg2, result):
        self.__op     = op      # CodeOp
        self.__arg1   = arg1      # Symbol-tableEntry
        self.__arg2   = arg2      # Symbol-tableEntry
        self.__result = result      # Symbol-tableEntry or Label

    def getOp(self):
        return self.__op

    def set(self,op,arg1,arg2,result):
        self.__op     = op
        self.__arg1   = arg1
        self.__arg2   = arg2
        self.__result = result

    def __repr__(self):
        global width
        op = self.__op[3:].rjust(width)
        if self.__arg1: arg1 = self.__arg1.rjust(width)
        else: arg1 = ''.rjust(width)
        if self.__arg2: arg2 = self.__arg2.rjust(width)
        else: arg2 = ''.rjust(width)
        if self.__result: result = str(self.__result).rjust(width)
        else: result = ''.rjust(width)
        return op+arg1+arg2+result


class Code:
    # TODO: Create a pretty print function to represent TAC
    # TODO: Create a function to change:
    #
    #       op      arg1    arg2    result
    #       LABEL   _       _       test
    #       Assign  1       _       t1
    #
    # TO:
    #
    #       Label:  op      arg1    arg2    result
    #       test:   Assign  1       _       t1
    pass

    def __init__(self):
        self.__List = []
        self.__tempVariables = 0
        self.__labels = 0

    def generate(self,op,arg1,arg2,result):
        # Result is a int (index in symbol-table)
        qdr = Quadruple(op,arg1,arg2,result)
        self.__List.append(qdr)

    def generateCall(self,entry,eList):
        # GenerateCall takes a list of variables as a parameters
        # and creates a line in the list for each variable in the list.
        # Finally it creates the call line where.

        for variable in eList:
            qdr = Quadruple('cd_APARAM',None,None,variable)
            self.__List.append(qdr)

        qdr = Quadruple('cd_CALL',entry,None,None)
        self.__List.append(qdr)

    def generateVariables(self,eList):
        for variable in eList:
            qdr = Quadruple('cd_VAR',None,None,variable)
            self.__List.append(qdr)

    def generateFParams(self,eList):
        for variable in eList:
            qdr = Quadruple('cd_FPARAM',None,None,variable)
            self.__List.append(qdr)


    def newLabel(self):
        self.__labels += 1
        labelName = 'lab'+str(self.__labels)
        return labelName

    def newTemp(self):
        self.__tempVariables += 1
        varName = 't'+str(self.__tempVariables)
        return varName

    def __repr__(self):
        global width
        # Pretty print?
        # Called print() in c++ header file
        print 'Op'.rjust(width) + 'Arg1'.rjust(width) + 'Arg2'.rjust(width) + 'Result'.rjust(width)
        print '----------'.rjust(width) + '----------'.rjust(width) + '----------'.rjust(width) + '----------'.rjust(width)
        for qdr in self.__List:
            print qdr.__repr__()
        pass
