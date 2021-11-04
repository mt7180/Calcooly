import myFunctionSet as fs
from extraFunctions import *
from sympy import *
x,y = symbols('x y')
#f_1, f_2 = symbols('f_1 f_2', cls=Function)

#----------
# Example how to use new classes:
#f_1 = x**2 + 3
#f_2 = 2*x - 1
#funset=fs.FunctionSet()
#funset.add_function(f_1, x)
#funset.add_function(f_2, x)
#-----------
#raw_input="test"
raw_input= "x**2 + 3; 2*x - 1"
#funset=input2functionset(raw_input)
funset=fs.FunctionSet()
funset.input2functionset(raw_input)
print(funset.functionSet)
#for func in funset.functionSet:
    #print (func.freeVariables[0])
    #print(func.fun)

print(functions2diagram(funset)[0])