import base64
from io import BytesIO
import matplotlib.pyplot as plt

import function

class Diagram:
    def __init__(self):
        self.figure = None
        self._err = False

    def generate_2D_symbolic(self, functionSet):
        self.figure = ""
        plot1 = None
        plt.rcParams['figure.figsize'] = 5, 5
        if not functionSet.limit:
            functionSet.limit = [-5,5]
        return self.figure

    def generate_3D_symbolic(self, functions, err):
        pass

    def generate_2D_points(self,functions, err):
        pass

    def generate_diagram(self, functions, err):
        max_vars = max([len(f.free_variables) for f in functions])
        if not max_vars:
            self.generate_2D_points(functions, err)
        elif max_vars < 2:
            return self.generate_2D_symbolic(functions, err)
        elif max_vars < 3:
            return self.generate_3D_symbolic(functions, err)

