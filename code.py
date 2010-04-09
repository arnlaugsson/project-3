# Compilers - Project 3
# Reykjavik University, Spring 2010
# Haukur Jonasson, Skuli Arnlaugsson

# Global
width = 10

CodeOp = [ 'cd_LABEL', 'cd_UMINUS', 'cd_ASSIGN',
           'cd_ADD', 'cd_SUB', 'cd_MULT', 'cd_DIVIDE',
           'cd_DIV', 'cd_MOD', 'cd_OR', 'cd_AND', 'cd_NOT',
           'cd_LT', 'cd_LE', 'cd_GT', 'cd_GE', 'cd_EQ', 'cd_NE',
		   'cd_GOTO', 'cd_CALL', 'cd_APARAM', 'cd_FPARAM', 'cd_VAR',
           'cd_RETURN', 'cd_NOOP']

def checkIfExists(filename):
    import os
    return os.path.exists(filename)

class Quadruple:
    def __init__(self, op, arg1='', arg2='', result=''):
        self.op     = op          # CodeOp
        self.arg1   = arg1        # Symbol-tableEntry
        self.arg2   = arg2        # Symbol-tableEntry
        self.result = result      # Symbol-tableEntry or Label


class Quint:
    # A class to hold a quintdruple (labels in front)
    def __init__(self,name=' ',op=' ',arg1=' ',arg2=' ',result=' '):
        self.name = name
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        global width
        if self.name == None: name = ''
        else: name = self.name.lower()
        if self.op == None: op = ''
        else: op = self.op[3:]
        if self.arg1 == None:  arg1= ''
        else:  arg1= self.arg1.lower()
        if self.arg2 == None: arg2= ''
        else:  arg2 = self.arg2.lower()
        if self.result == None:  result= ''
        else:  result = self.result.lower()
        return name.rjust(8)+op.rjust(10)+arg1.rjust(15)+arg2.rjust(15)+result.rjust(15)


class Code:
    def __init__(self):
        self.__List = []
        self.__quintList = []
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

    def generateAParams(self,eList):
        for variable in eList:
            qdr = Quadruple('cd_APARAM',None,None,variable)
            self.__List.append(qdr)

    def newLabel(self):
        self.__labels += 1
        labelName = 'lab'+str(self.__labels)
        return labelName

    def newTemp(self):
        self.__tempVariables += 1
        varName = 't'+str(self.__tempVariables)
        return varName

    def readyForPrint(self):
        global width
        label = ''
        for qdr in self.__List:
            if qdr.op == 'cd_LABEL':
                label = '%s:'%qdr.result
            else:
                quint = Quint(label,qdr.op,qdr.arg1,qdr.arg2,qdr.result)
                self.__quintList.append(quint)
                label = ''

    def printTacToFile(self,fileName):
        self.readyForPrint()
        
        if checkIfExists(fileName) == 1:
		    print "- '",fileName,"' already exists in your folder."
		    answer = raw_input("- Do you want to overwrite the file? (Y/N): ")

		    if answer.lower() != "y":
			    print "- Nothing written to file."
			    return False

        fileHandler = open(fileName,'wb')

        for quint in self.__quintList:
            fileHandler.write(quint.__repr__())
            fileHandler.write('\n')

        fileHandler.close()
        print '- TAC written to %s'%fileName
        return True

    def __repr__(self):
        self.readyForPrint()
        global width

        for quint in self.__quintList:
            print quint.__repr__()

