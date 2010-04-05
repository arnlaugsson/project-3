

CodeOp = [ 'cd_LABEL', 'cd_UMINUS', 'cd_ASSIGN',
           'cd_ADD', 'cd_SUB', 'cd_MULT', 'cd_DIVIDE',
           'cd_DIV', 'cd_MOD', 'cd_OR', 'cd_AND', 'cd_NOT',
           'cd_LT', 'cd_LE', 'cd_GT', 'cd_GE', 'cd_EQ', 'cd_NE',
		   'cd_GOTO', 'cd_CALL', 'cd_APARAM', 'cd_FPARAM', 'cd_VAR',
           'cd_RETURN', 'cd_NOOP']

class Quadruple:
    def __init__(self):
        self.__m_op     = None      # CodeOp
        self.__m_arg1   = None      # Symbol-tableEntry
        self.__m_arg2   = None      # Symbol-tableEntry
        self.__m_result = None      # Symbol-tableEntry or Label

    def getOp(self):
        return self.__m_op

    def set(self,op,arg1,arg2,result):
        self.__m_op     = op
        self.__m_arg1   = arg1
        self.__m_arg2   = arg2
        self.__m_result = result

    def __repr__(self):
        # TODO: Implement __repr__ for Quadruple class
        pass

class QuadrupleList:
    def __init__(self):
        self.__m_qdr    = None
        self.__m_next   = None

    def __setQuadruple(self,qdr):
        self.__m_qdr = qdr

    def getQuadruple(self):
        return self.__m_qdr

    def getNext(self):
        return self.__m_next

    def setNext(self,qdrList):
        self.__m_next = qdrList

    def add(self,qdr):
        # Adds quadruple to list - at the end of the list??
        # TODO: need to implement add(qdr)
        pass

class Code:
    def __init__(self):
        self.__m_qList = None

    def generate(self,op,arg1,arg2,result):
        qdr = Quadruple(op,arg1,arg2,result)
        self.__m_qList.add(qdr)

    def generateCall(self,entry,eList):
        # TODO: implement generateCall
        pass

    def generateVariables(self,eList):
        # TODO: implement generateVariables
        pass

    def newLabel(self):
        # TODO: implement newLabel
        pass

    def newTemp(self):
        # TODO: implement newTemp
        pass

    def __repr__(self):
        # Pretty print?
        # Called print() in c++ header file
        # TODO: Implement __repr__ for Code class
        pass
