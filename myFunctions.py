from sympy import *
class Function:
    """Represents a function in a set of functions. 
    Some function-functions are available"""

    #functionSet=[] #Klassenvariable, part of the class definition

    def __init__(self, fun, num, free, tag=""):
        """Initializes a function with fun, which is the already parsed function to be displayed and processed.
        Optional tag is available if extra calculations have to be performed.
        fun: parsed function
        tag: optional tag if function has to be further processed/ calculated
        num: # of function in function set
        free: list of free variables"""
        self.fun = fun
        self.num = num
        self.freeVariables = free
        self.tag = tag
    
    def __str__(self):
        return str(self.fun)

    def integrateFunc(self, variable):
        return integrate(self.fun, variable)

    def differentiateFunc(self, variable):
        return diff(self.fun, variable)