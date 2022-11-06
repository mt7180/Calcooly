import base64
from io import BytesIO
import matplotlib.pyplot as plt
import sympy as smp

#import function

class Diagram:
    def __init__(self):
        self.figure = ""
        self._err = ""
        self._plot = None


    def generate_2D_symbolic(self, function_set):
        if not function_set.limit:
            function_set.limit = [-5,5]
        #plot1 = None
        functions = {f.symbolic_function: f.free_variables[0] for f in function_set.functions}
        try:
            plt.switch_backend('Agg')   # no GUI initialized, dont needed
            plt.rcParams['figure.figsize'] = 5, 5
            plt.rcParams['legend.loc']='upper right'
        
            self._plot = smp.plot(*functions.keys(),([*functions.values()][0],-5,5), show = False)
            self._plot.legend=True         
            backend = self._plot.backend(self._plot)
            backend.process_series()
            buffer = BytesIO()
            backend.fig.savefig(buffer, format="png", dpi=100)
            
            # Embed the result in the html output
            self.figure = base64.b64encode(buffer.getbuffer()).decode("ascii")
            
            buffer.close()
        except Exception as e:
            self._err = e
        return self

    def generate_3D_symbolic(self, functions):
        p1 = plotting.plot3d(f.fun, (f.freeVariables[0],tmin, tmax), (f.freeVariables[1],tmin,tmax),surface_color='green', show = false)  # ToDo give possibility to make user input vor plotting range (";[-5,5]")
        

    def generate_2D_points(self,function_set):
        pass

    def generate_diagram(self, function_set):
        max_vars = max([len(f.free_variables) for f in function_set.functions])
        if not max_vars:
            self.generate_2D_points(function_set)
        elif max_vars < 2:
            self.generate_2D_symbolic(function_set)
        elif max_vars < 3:
            self.generate_3D_symbolic(function_set)

