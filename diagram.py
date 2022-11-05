import base64
from io import BytesIO
import matplotlib.pyplot as plt

import function

class Diagram:
    def __init__(self):
        self.figure = None
        self._err = False

    def generate_2D_symbolic(self, function_set):
        self.figure = ""
        plot1 = None
        plt.rcParams['figure.figsize'] = 5, 5
        if not function_set.limit:
            function_set.limit = [-5,5]
        return self

    def generate_3D_symbolic(self, functions):
        pass

    def generate_2D_points(self,function_set):
        pass

    def generate_diagram(self, function_set):
        max_vars = max([len(f.free_variables) for f in function_set.functions])
        if not max_vars:
            self.generate_2D_points(function_set)
        elif max_vars < 2:
            return self.generate_2D_symbolic(function_set)
        elif max_vars < 3:
            return self.generate_3D_symbolic(function_set)

