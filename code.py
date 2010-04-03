import sys

class code:
    def __init__(self, filename):
        self.f = open(filename,"w")

    def generate(self, op, arg1, arg2, result):
        self.f.write("\t"+op+"\t"+arg1+"\t"+arg2+"\t"+result+"\n")
        return

    def close(self):
        self.f.close()