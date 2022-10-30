import sympy as smp

class Function:
    def __init__(self, symbolic, expr, free_vars, plot = True):
        """Initializes a function with fun, which is the already parsed function to be displayed and processed.
        Optional tag is available if extra calculations have to be performed.
        symbolic_function: parsed function
        x: x-points if no function available (ODE output)
        y: y-points if no function available (ODE output)
        tag: optional tag if function has to be further processed/ calculated
        num: # of function in function set
        free: list of free variables
        plot: flag for plotting"""
        self.symbolic_function = symbolic
        self.expr = expr
        self.x = []
        self.y = []
        #self.num = num
        self.free_variables = free_vars
        #self.tag = tag
        self.plot = plot # default plotting mode is True
    
    def __str__(self):
        return self.expr
    
    def __repr__(self):
        return self.expr

    def get_latex_description(self, indx: int) -> str:
        if self.plot:
            vars = ','.join(map(lambda x: str(x), self.free_variables))
            f_latex = ("f_{" + str(indx+1) + "}" 
                +'(' + vars +')'
                + " = " 
                + smp.latex(self.symbolic_function))
        return f_latex
