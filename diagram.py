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
       
        functions = {f.symbolic_function: f.free_variables[0] for f in function_set.functions}
        
        self._plot = smp.plot(
            *functions.keys(),
            ([*functions.values()][0], function_set.limits[0], function_set.limits[1]),
            show = False
        )

    def generate_3D_symbolic(self, function_set):
        #x, y, z = smp.symbols('x y z')
        functions = {f.symbolic_function: f.free_variables for f in function_set.functions}
        free_vars = [*functions.values()][0] # only for the first function, todo: check if same vars for other functions

        self._plot = smp.plotting.plot3d(
            *functions.keys(), 
            (free_vars[0], function_set.limits[0], function_set.limits[1]), 
            (free_vars[1], function_set.limits[0], function_set.limits[1]),
            surface_color='green', show = False
        )
        

    def generate_2D_points(self,function_set):
        pass

    def generate_diagram(self, function_set):
        if not function_set.limits:
            function_set.limits = [-5,5]
        try:
            plt.switch_backend('Agg')   # without GUI initialization, not needed
            plt.rcParams['figure.figsize'] = 5, 5
            plt.rcParams['legend.loc']='upper right'
            max_vars = max([len(f.free_variables) for f in function_set.functions])
            if not max_vars:
                self.generate_2D_points(function_set)
            elif max_vars < 2:
                self.generate_2D_symbolic(function_set)
            elif max_vars < 3:
                self.generate_3D_symbolic(function_set)
            self._plot.legend=True         
            backend = self._plot.backend(self._plot)
            backend.process_series()
            buffer = BytesIO()
            backend.fig.savefig(buffer, format="png", dpi=100)
            
            # Embed the result in the html output
            self.figure = base64.b64encode(buffer.getbuffer()).decode("ascii")
        except Exception as ex:
            self._err += str(ex)
        buffer.close()

