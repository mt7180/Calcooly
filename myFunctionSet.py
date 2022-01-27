from myFunctions import *
import matplotlib.pyplot as plt
import sympy as smp
import numpy as np
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, convert_xor, implicit_multiplication, convert_equals_signs
from scipy.integrate import odeint
from io import BytesIO
import base64

class FunctionSet:
    """Represents the whole set of functions"""
    # class variable; tracks the total number of functions per set
    last_id = 0

    def __init__(self):
        """Initialization"""
        self.functionSet = []
        self.err = ""
        self.tag = ""
        self.limit=""

    def __str__(self):
        """output when printed"""
        output = ""
        for i, func in enumerate(self.functionSet):
            if i < len(self.functionSet) - 1:
                output += str(func) + ", "
            else:
                output += str(func)
        return output

    def add_function(self, fun, free, plot, tag = ""):
        """adds a function to the functionSet"""
        FunctionSet.last_id += 1
        self.functionSet.append(Function(fun, FunctionSet.last_id, free, plot, tag))

    def add_function_withpoints(self, x, y, ode_list, plot, tag):
        """adds a function to the functionSet"""
        FunctionSet.last_id += 1
        func = Eq(ode_list[0], ode_list[1])
        f = Function(func, FunctionSet.last_id, ode_list[2], plot, tag)
        print("funs: ", f.fun)
        f.x = x
        f.y = y
        self.functionSet.append(f)
        #return f

    def functions2diagram(self):
        """draws diagram for set of functions
        returns: (out, fig64, True/False)"""
        fig64 = ""
        if (self.err == "" and len(self.functionSet) > 0 and self.tag != "ODE"):
            x, y, z = smp.symbols('x y z')

            plot1 = None
            out = []
            #also sets digram size of smp.plot:
            plt.rcParams['figure.figsize'] = 5, 5

            try:
                for i, f in enumerate(self.functionSet):
                    if len(f.freeVariables) > 0 and f.plot == True:
                        if self.limit:
                            tmin = self.limit.split(',')[0]
                            tmax = self.limit.split(',')[1]
                        else:
                            tmin = -5
                            tmax = 5
                        #out.append("y"+str(i+1)+"="+smp.latex(f.fun))
                        out.append("f_{"+str(i+1)+"}(")
                        for j, var in enumerate(f.freeVariables):
                            if j < len(f.freeVariables) - 1:
                                out[i] += str(var) + ","
                            else:
                                out[i] += str(var)
                        out[i] += ")=" + smp.latex(f.fun)

                        if len(f.freeVariables) < 2:
                            p1 = smp.plot(f.fun, (var, tmin,tmax), show=False)  # ToDo give possibility to make user input vor plotting range (";[-5,5]")
                            p1[0].label = f.fun
                            if plot1 is not None:
                                plot1.extend(p1)
                            else:
                                plot1 = p1
                        elif len(f.freeVariables) < 3:

                            p1 = plotting.plot3d(f.fun, (f.freeVariables[0],tmin, tmax), (f.freeVariables[1],tmin,tmax),surface_color='green', show = false)  # ToDo give possibility to make user input vor plotting range (";[-5,5]")
                            p1[0].label = f.fun
                            if plot1 is not None:
                                plot1.extend(p1)
                            else:
                                plot1 = p1
                    else:
                        out.append(smp.latex(f.fun))

                if plot1:
                    #Key legend.loc: 'upper_right' is not a valid value for legend.loc; supported values are ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center']
                    plt.rcParams['legend.loc'] = 'upper right'
                    plot1.legend = True

                    backend = plot1.backend(plot1)
                    backend.process_series()
                    buf = BytesIO()
                    backend.fig.savefig(buf, format = "png", dpi = 100)

                    # Embed the result in the html output
                    fig64 = base64.b64encode(buf.getbuffer()).decode("ascii")
                    return (out, fig64, False)
                else:
                    return(out,"",False)
            except TypeError:
                if self.err == "":
                    self.err = "your function can not be plotted -> forgot to give a keyword like 'ODE: ?"
            except Exception as e:
                # add just first error
                if self.err == "":
                    self.err = e
            return (self.err, fig64, True)
        # print ODE to diagram
        elif (self.err == "" and len(self.functionSet) > 0 and self.tag == "ODE"):
            out = []
            fig = plt.figure()
            plt.rcParams['figure.figsize'] = 5, 5
            out.append("ODE: ")
            for i, f in enumerate(self.functionSet):
                if len(f.x) > 0 and len(f.y) >0 and f.plot == True:
                    out.append(smp.latex(f.fun))
                    # y1n=f.y
                    plt.plot(f.x, f.y, label = f.freeVariables[i].name)
            plt.legend(loc = 'upper right')
            plt.xlabel(f.freeVariables[-1].name)
            plt.tight_layout()
            # plt.show()
            buf = BytesIO()
            fig.savefig(buf, format = 'png', dpi=100)
            fig64 = base64.b64encode(buf.getbuffer()).decode("ascii")
            return (out, fig64, False)
        else:
            return (self.err, fig64, True)

    def input2functionset(self, input_raw):
        """parse raw input string and put functions to function set"""
        try:
            if not input_raw:
                raise Exception('something went wrong #1')
            # print(input_raw)
            input = [inp.strip() for inp in input_raw.split(';')]
            transformations = (standard_transformations + (implicit_multiplication,) + (convert_xor,) +(convert_equals_signs,))
            x, y, z = smp.symbols('x y z')

            for i, inp in enumerate(input):
                if not inp: # if current segment of ";"-seperated input is empty
                    continue

                # if equation is given -> simplify
                if ("=" or "Eq") in inp:
                    sol = simplify(parse_expr(inp, transformations=transformations, local_dict={'e': E})).lhs
                else:
                    sol = parse_expr(inp, transformations=transformations, local_dict={'e': E})

                if len(sol.free_symbols) > 0:
                    if self.tag == "Integral":
                        sol = integrate(sol) # only one free symbol should be given
                    elif self.tag == "Derivative":
                        sol = diff(sol)
                    self.add_function(sol, list(sol.free_symbols),True,"")  # ToDo: implement tag (for integration or so) for single Function and replace "" in function call
                # print(self.functionSet)
                else:
                    self.add_function(sol, "",False,"")
        except AttributeError:
            if self.err == "":
                self.err = "parsing your function returned an error"
        except Exception as e:
            #add just first error
            if self.err == "":
                self.err = e

    def extrafunc(self, input_raw):
        """parse input for keywords for extra-function and give tags/ call extra-functions"""
        # if "[" in input_raw:
        input_pre = [inp.strip() for inp in input_raw.split("limit[")]
        if len(input_pre) > 1:
            if "]" in input_pre[1]:  # remember: only one limit must be given!
                self.limit = input_pre[1][:-1]

        if ":" in input_pre[0]:
            print("#2: ", input_pre[0])
            input = [inp.strip() for inp in input_pre[0].split(':')]
            if input[0].upper() == "ODE":
                self.tag = "ODE"
                ## self.ode2functionset(input[1])
                # print("#4", input[1])
                return input[1]
            elif input[0].upper() == "INTEGRAL":
                self.tag = "Integral"
                return input[1]
            elif input[0].upper() == "DERIVATIVE":
                self.tag = "Derivative"
                return input[1]
            else:
                self.err = 'tag: ' + input[0] + ' not known!'
                return input[1]
        else:
            return input_pre[0]

    def ode2functionset(self, input_raw):
        """Parse, calculate and put ode into Function set"""
        try:
            transformations = (standard_transformations + (convert_xor,) +(convert_equals_signs,))
            input = [parse_expr(inp.strip(), transformations=transformations, evaluate=True) for inp in input_raw.split(';')]
            sols_rhs = []
            sols_lhs = []
            deriv_free_symb = []
            S_0 = []
            # for every single input
            for i,inp in enumerate(input):
                try:
                    # for every second input (start conditions not to be considered here)
                    if i%2 == 0:
                        fd_set = inp.find(smp.Derivative)
                        # find highest derivative:
                        d_max = (0, "")
                        for fd in fd_set:
                            if fd.derivative_count > d_max[0]: dmax = (fd.derivative_count,fd)
                           # print(dmax)

                        sol = smp.solveset(inp, (dmax[1]))
                        sols_rhs.append(list(sol)[0])  # wandle set in Liste um, auch wenn nicht optimal => takes just the first solution, but should be sufficient here
                        sols_lhs.append(dmax[1])
                        deriv_free_symb.append([s for fd in fd_set for s in fd.free_symbols])
                        #if len(deriv_free_symb) > 0:
                            #self.add_function(list(sol)[0], deriv_free_symb, False,"DiffEq")
                    # Anfangsbedingungen aus input extrahieren
                    else:
                        S_0.append(inp)
                        #print(f"S_0: {S_0}")
                except Exception as e:
                    if self.err == "": # add just first error
                        self.err = e
                    return       # in case of error while parsing ODE exit and return None

            free_sym_d = list({f for free in deriv_free_symb for f in free})[0]  # only derivatives of the same variable are considered
            # print(sols_lhs, sols_rhs,"free sym d: ", free_sym_d)
            # print(f"S_0: {S_0}")
            # print(input[0].free_symbols)

            free_sym = [args.func for fd in sols_lhs for args in fd.args if args.is_Function]
            # print([*free_sym,free_sym_d])
            inp_f = [smp.lambdify([*free_sym,free_sym_d], sol, 'numpy') for sol in sols_rhs]

            # function for odeint
            def dSdt(S, t):
                # yy1, yy2 =S
                # return [ans(t,yy1,yy2) for ans in inp_f]
                return [ans(*S,t) for ans in inp_f] # *S: unpacked S_vector

            if self.limit:
                tmin = self.limit.split(',')[0]
                tmax = self.limit.split(',')[1]
            else:
                tmin = 0
                tmax = float(max(*[S0*20 for S0 in S_0], 1))  # default

            t = np.linspace(float(tmin), float(tmax), 100)

            # Solve ODE with SciPy
            sol = odeint(dSdt, y0 = S_0, t = t)
            for i, y in enumerate(sol.T):
                ode_list = [sols_lhs[i], sols_rhs[i], [*free_sym,free_sym_d]]
                self.add_function_withpoints(t, y, ode_list, True, "")
        except Exception as e:
            if self.err == "": # add just first error
                self.err = e
            return