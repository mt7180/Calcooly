from myFunctions import *

class FunctionSet:
    """Represents the whole set of functions"""
    #class variable; tracks the total number of functions per set
    last_id=0
    
    def __init__(self):
        """Initialization"""
        self.functionSet=[]
        self.err = ""

    def __str__(self):
        """output when printed"""
        output=""
        for i, func in enumerate(self.functionSet):
            if i < len(self.functionSet)-1:
                output += str(func) +", "
            else:
                output += str(func)
        return output

    def add_function(self, fun, free, tag=""):
        """adds a function to the functionSet"""
        FunctionSet.last_id += 1
        self.functionSet.append(Function(fun, FunctionSet.last_id, free, tag))

