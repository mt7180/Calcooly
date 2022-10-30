
import numpy as np
from sympy.parsing.sympy_parser import standard_transformations, convert_xor, implicit_multiplication, convert_equals_signs
import sympy as smp

from function import Function

keyword_map = {}

def keyword(func):
    keyword_map[func.__name__]=func
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
    except AttributeError:
        function_set._err.append("parsing your function returned an error")
    except Exception as e:
         function_set._err.append(e)
    print("errors: ",  function_set._err)
    return

    def ode(expr, err):
        pass

    def integral(func):
        def wrapper(*args, **kwargs):
            return [integrate(f[0]) for f in func(*args, **kwargs) if f[1] > 0]
        return wrapper