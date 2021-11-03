import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
#from scipy.integrate import odeint
import sympy as smp
#from matplotlib import animation
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, convert_xor, implicit_multiplication
import numpy as np
from io import BytesIO
import base64
import myFunctionSet as fs

def extraFunctions(input):
    listofFunctions=["ODE","Integral"]
    for func in listofFunctions:
        if func in input:
            return (func, input[len(func):])
    return("", input)

    #Parse Input String and prepare plot
def parseInput(input_raw):
    fig64=""
    input = [inp.strip() for inp in input_raw.split(';')]
    #input=input_raw.replace("^","**")
    transformations = (standard_transformations + (implicit_multiplication,) + (convert_xor,))
    x, y, z = smp.symbols('x y z')
    plot1=None
    out=[]
    #also sets digram size of smp.plot:
    plt.rcParams['figure.figsize'] = 3, 3
   
    try: 
        for i, inp in enumerate(input):

            func1 =extraFunctions(inp)
            #if func1[0]=="ODE":
                #todo
            sol = parse_expr(func1[1], transformations=transformations)
            print(sol)
            if len(sol.free_symbols) > 0:
                if len(sol.free_symbols)==1:
                    if func1[0]=="Integral":
                        sol=smp.integrate(sol,x)
                        
                    out.append("y"+str(i+1)+"="+smp.latex(sol))
                    #p1 = smp.plot(sol, label=inp, legend=True, show=False)
                    p1 = smp.plot(sol, show=False)
                    p1[0].label=sol
                    if plot1 is not None:
                        plot1.extend(p1)
                    else:
                        plot1 = p1
                elif len(sol.free_symbols)==2:
                    p1 = smp.plotting.plot3d(sol, show=False)
                    out.append("y"+str(i+1)+"="+smp.latex(sol))
                    #p1 = smp.plot(sol, label=inp, legend=True, show=False)
                    p1 = smp.plotting.plot3d(sol, show=False)
                    p1[0].label=sol
                    if plot1 is not None:
                        plot1.extend(p1)
                    else:
                        plot1 = p1
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
    except Exception as e:
        return (e, fig64, True)

