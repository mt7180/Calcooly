import keywords
from diagram import Diagram

class Calcooly():
    def __init__(self)-> None:
        self.key = "defaultkey"
        self.limit = []
        self.functions = []
        self._strategy = None
        self._err = ""
    
    def __str__(self):
        return str(self.functions)
        
    def extract_limit(self, expr: str)->str:
        """get limit at the end of input_str: "x^2; e^x [-1, 4]
           if something went wrong, original input_str is returned
        """
        if expr[-1] == ']':
            if '[' in expr:
                split_indx = expr.rfind("[")
                limits = expr[split_indx+1:-1]
                self.limits = [int(limit) for limit in limits.split(',')]
                return expr[:split_indx].strip()
            self.err += "limit error"
        return expr

    def extract_keywords(self, expr: str)-> str:
        split_indx = expr.find(":") # if no ":" in expr: split_indx=-1
        if ":" in expr: key = expr[:split_indx]
        else: key = 'default_function'
        self._strategy = keywords.keyword_map.get(key.lower())
        if not self._strategy:
            self._err += 'key: ' + key + ' not known!'
            raise ValueError(key)
        return expr[split_indx+1:]
    
    def parse_functions(self, expr):
        return self._strategy(expr, self)

    def parse_raw_input(self, raw_input):
        raw_input = self.extract_limit(raw_input)
        raw_input = self.extract_keywords(raw_input)
        self.parse_functions(raw_input)

    def get_latex_functions(self):
        latex_functions =[]
        for i,function in enumerate(self.functions):
            latex_functions.append(function.get_latex_description(i))
        return latex_functions

    def get_diagram(self):
        diagram = Diagram()
        return diagram.generate_diagram(self)

if __name__ == "__main__":
    app = Calcooly()
    print(keywords.keyword_map)
    raw_input = input("give function: ")
    app.parse_raw_input(raw_input)
    print(app)
    print(app.get_latex_functions())
    #diagram = app.get_diagram()