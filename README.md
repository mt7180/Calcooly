# Calcooly

#### Description:

Calcooly is a flask web application, which is an advanced calculator based on python to calculate and visualize 2d and 3d functions.
Also systems of equations like linear/ nonlinear sets of equations or even differential equations (ODEs), but also simple calculations
with numbers can be executed.

Since the python module Sympy is used to parse the user input, the program is able to find functions and function variables, to execute
mathematical operations on these equations like converting and calculating them and to plot the functions over the detected variables.

Notation Conventions and Manual:
--------------------------------

- You can type any mathematical function that can be given as e.g "x^2" or "f(x)=x^2" and it will be simplified and printed to a diagram.
- You can enter any mathematical expression that e.g. can be entered into a hand calculator.
- You may give several functions at once, separated by **";"**.
- Use only small letters for function variables.
- To expand the input window for e.g. more complex systems of equations, press the "+" button
- To specify the range of the x-axis, enter **limit[xmin, xmax]** at the end of the function. => "x^2; e^x [-1, 4]"
- Use the **keyword "Integral:"** to calculate the integral(s) of your function(s). => "Integral: x^2; e^x"
- Use the **keyword "Derivative:"** to calculate the derivative(s) of your function(s). => "Derivative: x^2; e^x"
- Use keyword **"ODE:"** for solving ordinary differential equations separated by ";" - each starting condition given after each differential equation, also seperated by ";"
  Example=> "ODE: theta(t).diff(t) = omega; pi / 4; omega(t).diff(t) = -sin(theta) ;0"
- Additionally, you may use Python SymPy syntax for more complex calculations. -> https://docs.sympy.org/latest/tutorial/solvers.html
- To reuse the last function again, just click on the input text below, it will be copied into the input text field and can be edited.
- To save a fuction, click the corresponding button.
- To view all saved functions, click on the link "History".
- To find notation conventions and program description, click on the link "Notation Conventions".

Behind the Scenes:
------------------

I decided to have a clean and google-like, focussed design for the index page. Only the logo, the input field and the two links "Notation Conventions" and
"History" are shown at first glance.
After the function(s) is/ are typed and the Calc-Button is clicked, an output field is put below, which gives the input functions in latex notation
using the MathJax-script (same method as used for displaying functions in the jupyter notebooks) and on the left side the functions are plotted into a matplotlib
diagram, which is embedded as figure via base64 encryption.

The saved functions are stored in a sqlite3-database, I decided to not make them user-related, so no login is necessary here.
All saved functions are shown in descending order with the last saved function at the top. They are inserted as a link via flask "url_for" statement,
where each link has a specific URL parameter, its SQL-id. If you click on it, the number is transferred via the URL parameter, while flask receives it with
the GET request. After that the index page looks up the corresponding function in the database and copies it into the input field. Finally the input is
excecute by a DOM event listener, which also looks for a parameter in the url.

Files:
------

- app.py: Flask web application, main program, it has the routes "/" (and "/index/<fid>"), "/history" and "/notation"
- myFunctions.py: holds the class "Function", which represents a single function with some instance variables
    - fun: parsed function
    - x: list of x-points if no function is given (for plotting ODE output)
    - y: list of y-points if no function is given (for plotting ODE output)
    - tag: optional tag for extra functions to be processed
    - num: # of function in function set
    - free: list of free variables
    - plot: flag for plotting into diagram
- myFunctionSet.py: holds the class "FunctionSet", which represents the whole set of functions with class variable "last_id" and some instance variables
and methods
    - functionSet : list of functions stored in the functionset
    - err: holds first error description, if an error occurs while processing the functions (is flashed to the index page)
    - tag: when a keyword like Integral:, Derivative: or ODE: is given by the user, it is stored here
    - limit: x-axis limit for diagram to be plotted

    - add_function(self, fun, free, plot, tag=""): adds a function to the functionSet
    - add_function_withpoints(self, x, y, ode_list, plot, tag): adds a function with x/ y points to the functionSet
    - functions2diagram(self): draws diagram for set of functions, returns: (out, fig64, True/False)
    - input2functionset(self, input_raw): parse raw input string and put functions to function set
    - extrafunc(self, input_raw): parse input for keywords for extra-function and give tags/ call extra-functions
    - ode2functionset(self, input_raw): Parse, calculate and put ode into Function set

templates:
- index.html: starting and input page
- notation.html: page with notation conventions and manual:
- history.html: page with saved functions shown in descending order with the last saved function at the top

data:
- CalcoolyHistory.db: sqlite database
    '''CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dt DATETIME default(datetime(current_timestamp)));'''

static:
- styles.css: definition of styles for html pages
