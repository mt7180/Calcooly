from myFunctions import *
import matplotlib.pyplot as plt
import sympy as smp
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, convert_xor, implicit_multiplication
from io import BytesIO
import base64
from extraFunctions import extraFunctions

class FunctionSet:
    """Represents the whole set of functions"""
    #class variable; tracks the total number of functions per set
    last_id=0
    
    def __init__(self):
        """Initialization"""
        self.functionSet=[]
        self.err = ""
        self.tag = ""

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

    def functions2diagram(self):
        """draws diagram for set of functions
        returns: (out, fig64, True/False)"""
        fig64=""
        if (self.err == "" and len(self.functionSet)>0):
            x, y, z = smp.symbols('x y z')
            plot1=None
            out=[]
            #also sets digram size of smp.plot:
            plt.rcParams['figure.figsize'] = 3, 3
            
            for i, f in enumerate(self.functionSet):
                if len(f.freeVariables) > 0:
                    #out.append("y"+str(i+1)+"="+smp.latex(f.fun))
                    out.append("f_{"+str(i+1)+"}(")
                    for j, var in enumerate(f.freeVariables):
                        if j < len(f.freeVariables) - 1:
                            out[i] += str(var) + ","
                        else:
                            out[i] += str(var)
                    out[i] += ")=" + smp.latex(f.fun)
                    p1 = smp.plot(f.fun, show=False)
                    p1[0].label=f.fun
                    if plot1 is not None:
                        plot1.extend(p1)
                    else:
                        plot1 = p1
            if plot1:
                #Key legend.loc: 'upper_right' is not a valid value for legend.loc; supported values are ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center']
                plt.rcParams['legend.loc']='upper right'
                plot1.legend=True          
                
                backend = plot1.backend(plot1)
                backend.process_series()
                buf = BytesIO()
                backend.fig.savefig(buf, format="png", dpi=100)
                
                # Embed the result in the html output
                fig64 = base64.b64encode(buf.getbuffer()).decode("ascii")
                return (out, fig64, False)
        else:
            return (self.err, fig64, True)

    def input2functionset(self, input_raw):
        """parse raw input string and put functions to function set"""
        input = [inp.strip() for inp in input_raw.split(';')]
        transformations = (standard_transformations + (implicit_multiplication,) + (convert_xor,))
        x, y, z = smp.symbols('x y z')
        #funset=self.FunctionSet()
        
        for i, inp in enumerate(input):
            tag=""
            extrafun =extraFunctions(inp)
            if extrafun[0]=="ODE":
                self.tag="ODE"
            elif extrafun[0]=="Integral":
                tag="Integral"
            try:
                sol = parse_expr(extrafun[1], transformations=transformations)
                
                if len(sol.free_symbols) > 0:
                    self.add_function(sol, list(sol.free_symbols),tag)
            except AttributeError:
                if self.err == "":
                    self.err = "parsing your function returned an error"
            except Exception as e:
                #add just first error
                if self.err == "":
                    self.err = e
