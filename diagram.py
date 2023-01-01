import base64
from io import BytesIO
import matplotlib.pyplot as plt
import sympy as smp
import traceback  # error handling

class Diagram:

    def __init__(self):
        self.figure = ""
        self._err = ""
        self._plot = None

    def move_sympyplot_to_axes(self, p, ax): # ax has to be a tuple
        backend = p.backend(p)
        backend.ax = ax
        backend.process_series()
        for axis in backend.ax:
            axis.spines['right'].set_color('none')
            axis.spines['bottom'].set_position('zero')
            axis.spines['top'].set_color('none')
        plt.close(backend.fig)

    def generate_2D_symbolic(self, function_set, ax):
        if not function_set.limits:
            function_set.limits = [-5,5]
        #functions = {f.symbolic_function: f.free_variables[0] for f in function_set.functions}
        # for func, vars in functions.items():
        for f in function_set.functions:
            p1 = smp.plot(
                f.symbolic_function,
                (f.free_variables[0], function_set.limits[0], function_set.limits[1]),
                show = False
            )
            self.move_sympyplot_to_axes(p1, (ax,))
        # self._plot = ax

    def generate_3D_symbolic(self, function_set, ax):
        #x, y, z = smp.symbols('x y z')
        #functions = {f.symbolic_function: f.free_variables for f in function_set.functions}
        #free_vars = [*functions.values()][0] # only for the first function, todo: check if same vars for other functions

        for f in function_set.functions:
            p1 = smp.plotting.plot3d(
                f.symbolic_function, 
                (f.free_variables[0], function_set.limits[0], function_set.limits[1]), 
                (f.free_variables[1], function_set.limits[0], function_set.limits[1]),
                surface_color='green', show = False
            )
            self.move_sympyplot_to_axes(p1, (ax,))
        

    def generate_2D_points(self,function_set):
        # 2 graphen mit jeweils 3 Punkten:
        # x = [[x11, x21], [x12, x22], [x13, x23]]
        # y = [[y11, y21], [y12, y22], [y13, y23]]
        fx = [f.x for f in function_set.functions]
        fy = [f.y for f in function_set.functions]
        x = list(zip(*fx))
        y = list(zip(*fy))
        self._plot = plt.plot(x, y)  # list object, passt nicht zu smp.plotting ... was ist mit sympy.plotting.plot.Line2DBaseSeries
        print("plot-type", type(self._plot))

    def generate_diagram(self, function_set):
        
        try:
            plt.switch_backend('Agg')   # without GUI initialization, not needed
            fig = plt.figure(figsize=plt.figaspect(0.5))
            
            plt.rcParams['figure.figsize'] = 5 , 5
            plt.rcParams['legend.loc'] = 'upper right'
            max_vars = max([len(f.free_variables) for f in function_set.functions])
            if function_set.plot == "2D_points":
                ax = fig.add_subplot(1, 1, 1,)
                self.generate_2D_points(function_set)
            elif max_vars < 2:
                ax = fig.add_subplot(1, 1, 1,)
                self.generate_2D_symbolic(function_set, ax)
            elif max_vars < 3:
                ax = fig.add_subplot(1, 1, 1, projection='3d')
                self.generate_3D_symbolic(function_set, ax)
            
            plt.legend(loc='upper right')
            plt.xlabel(function_set.free_vars)  # todo: welche free_vars (mit set.difference)
            plt.tight_layout()
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=70)

            # Embed the result into html output
            self.figure = base64.b64encode(buffer.getbuffer()).decode("ascii")
        except Exception as ex:
            traceback.print_exc()
            self._err += str(ex)
        buffer.close()

