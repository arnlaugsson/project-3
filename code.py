

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
        return str(self.__op) + '\t' + str(self.__arg1) + '\t\t' + str(self.__arg2) + '\t\t' + str(self.__result)


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

    def newLabel(self):
        self.__labels += 1
        labelName = 'lab'+str(self.__labels)
        return labelName

    def newTemp(self):
        self.__tempVariables += 1
        varName = 't'+str(self.__tempVariables)
        return varName

    def __repr__(self):
        # Pretty print?
        # Called print() in c++ header file
        print
        print 'TAC preview..'
        print 'Op' + '\t\t' + 'Arg1' + '\t\t' + 'Arg2' + '\t\t' + 'Result'
        for qdr in self.__List:
            print qdr.__repr__()
        pass
