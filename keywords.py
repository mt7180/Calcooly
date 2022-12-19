
import numpy as np
from sympy.parsing.sympy_parser import standard_transformations, convert_xor, implicit_multiplication, convert_equals_signs
import sympy as smp

from scipy.integrate import odeint

from function import Function

keyword_map = {}

def keyword(func):
    """register keyword automatically in keyword_map"""
    keyword_map[func.__name__] = func
    return func

@keyword
def default_function(expr, function_set)-> None:
    try:
        if not expr:
            raise ValueError('no input given')
        input = [inp.strip() for inp in expr.split(';')]
        transformations = (standard_transformations 
                          + (implicit_multiplication,) 
                          + (convert_xor,) 
                          + (convert_equals_signs,))
        for inp in input:
            if not inp: # if current segment of ";"-seperated input is empty
                continue
            elif ("=" or "Eq") in inp:
                sol = smp.simplify(smp.parse_expr(
                    inp, 
                    transformations=transformations, 
                    local_dict = {'e': smp.E})
                ).lhs
            else:
                sol = smp.parse_expr(
                    inp, 
                    transformations=transformations, 
                    local_dict = {'e': smp.E}
                )
            print("sol:", sol, list(sol.free_symbols))
            function_set.functions.append(Function(sol, inp, list(sol.free_symbols)))
            for free_var in sol.free_symbols:
                function_set.free_vars.add(free_var)
    except AttributeError:
        function_set._err += "parsing your function returned an error"
    except Exception as ex:
        function_set._err += str(ex)
    print("errors: ",  function_set._err)

@keyword 
def ode(expr, function_set):
    function_set.plot = "2D_points"
    try:
        transformations = (standard_transformations + (convert_xor,) +(convert_equals_signs,))
        input = [smp.parse_expr(inp.strip(), transformations=transformations, evaluate=True) for inp in expr.split(';')]
        sols_rhs = []
        sols_lhs = []
        deriv_free_symb = []
        S_0 = []
        #for every single input
        for i,inp in enumerate(input):
            try:
                #for every second input (start conditions not to be considered here)
                if i%2 == 0:
                    fd_set=inp.find(smp.Derivative)
                    # find highest derivative:
                    d_max = (0, "")
                    for fd in fd_set:
                        if fd.derivative_count > d_max[0]: dmax = (fd.derivative_count,fd) 
                        # print(dmax)
                    
                    sol=smp.solveset(inp, (dmax[1]))
                    sols_rhs.append(list(sol)[0])  # wandle set in Liste um, auch wenn nicht optimal => takes just the first solution, but should be sufficient here
                    sols_lhs.append(dmax[1])
                    deriv_free_symb.append([s for fd in fd_set for s in fd.free_symbols])
                    #if len(deriv_free_symb) > 0:
                        #self.add_function(list(sol)[0], deriv_free_symb, False,"DiffEq")

                else:
                    S_0.append(inp) #Anfangsbedingungen aus input extrahieren
                    #print(f"S_0: {S_0}")

            except Exception as e:
                #if function_set.err=="": #add just first error
                print(e.with_traceback)
                function_set._err += str(e)
                return       # in case of error while parsing ODE exit and return None
        
        free_sym_d=list({f for free in deriv_free_symb for f in free})[0]  #only derivatives of the same variable are considered
        print(sols_lhs, sols_rhs,"free sym d: ", free_sym_d)
        print(f"S_0: {S_0}")
        #print(input[0].free_symbols) 
        print("#3: ", sol)

        free_sym=[args.func for fd in sols_lhs for args in fd.args if args.is_Function]
        print([*free_sym,free_sym_d])
        inp_f=[smp.lambdify([*free_sym,free_sym_d], sol, 'numpy') for sol in sols_rhs] 
        print("ploop")
        def dSdt(S, t):
            #yy1, yy2 =S
            #return [ans(t,yy1,yy2) for ans in inp_f]
            return [ans(*S,t) for ans in inp_f]    

        if not function_set.limits:
            function_set.limits = [0, float(max(*[S0*20 for S0 in S_0], 1))]  # gibt es bessere Möglichkeiten tmax festzulegen?!
       
        t = np.linspace(float(function_set.limits[0]), float(function_set.limits[1]), 100)  #ToDo automatisch anpassen
        
        #Solve ODE with SciPy
        sol = odeint(dSdt, y0=S_0, t=t)
        for i, y in enumerate(sol.T):
            #ode_list = [sols_lhs[i], sols_rhs[i], [*free_sym,free_sym_d]]
            
            symbolic_function = smp.Eq(sols_lhs[i], sols_rhs[i])
            f=Function(symbolic_function, expr, [*free_sym,free_sym_d], True)
            print("funs: ", f.symbolic_function)
            f.x = t
            f.y = y
            function_set.functions.append(f )
            for free_var in [*free_sym,free_sym_d]:
                function_set.free_vars.add(free_var)
    
    except Exception as e:
        #if function_set.err=="": #add just first error
        print(e.with_traceback)
        function_set._err += str(e)
        return

    @keyword
    def integral(expr, function_set):
        default_function(expr, function_set)
        for f in function_set.functions:
            if len(f.free_variables) > 0:
                f.symbolic_function = smp.integrate(f.symbolic_function)
    
    @keyword
    def derivative(expr, function_set):
        default_function(expr, function_set)
        for f in function_set.functions:
            if len(f.free_variables) > 0:
                f.symbolic_function = smp.Derivative(f.symbolic_function)  