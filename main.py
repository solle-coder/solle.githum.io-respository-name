from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt

@dataclass
class Calculation:
    expression: str
    answer: float
    category: str
    
@dataclass
class Settings:
    degree_mode:bool
    show_grid: bool
    graph_color: str
    
@dataclass
class State:
    calculations: list[Calculation]
    settings: Settings
    current_page: str
    last_answer: float
    

@route
def index(state: State) -> Page:
    
    return Page(state, [
        Header("Scientific Calculator"),
        "Welcome to the Scientific Calculator!\n",
        "With this calculator, you can perform many different equations through basic arithmetic to plotting on a graph.\n",
        "In this calculator, you have 4 types of calculators to choose from:\n",
        
        BulletedList([
            "Arithmetic",
            "Algebra",
            "Trigonometry",
            "Graph Plotting"
        ]),
        
        "\nSelect a calculator you want to use for your experiment:\n",
        
        Button("Arithmetic Calculator", arithmetic),
        Button("Algebra Calculator", algebra),
        Button("Trigonometry Calculator", trigonometry),
        Button("Graphing Calculator", graph)
    ])

def arithmetic_calculation(num1: float, num2: float, operation: str) -> str:
    if operation == "+":
        return str(num1 + num2)
    elif operation == "-":
        return str(num1 - num2)
    elif operation == "*":
        return str(num1 * num2)
    elif operation == "/":
        if num2 == 0:
            return "Error: Cannot divide by zero!"
        return str(num1 / num2)
    return "Invalid Operation"
    
assert_equal(arithmetic_calculation(2.0, 3.5, "+"), "5.5")
assert_equal(arithmetic_calculation(5.0, 3.0, "-"), "2.0")
assert_equal(arithmetic_calculation(12.0, 3.0, "*"), "36.0")
assert_equal(arithmetic_calculation(6.0, 3.0, "/"), "2.0")
assert_equal(arithmetic_calculation(4.0, 0.0, "/"), "Error: Cannot divide by zero!")

@route
def arithmetic(state: State) -> Page:
    state.current_page = "Arithmetic"
    return Page(state, [
        Header("Arithmetic Calculator"),
        "You can use this calculator to perform basic arithmetic equations such as addition, division, multiplication and many more.",
        "Enter first number",
        TextBox("number1"),
        "Enter second number",
        TextBox("number2"),
        "Choose an Operator",
        SelectBox("operation", ["+", "-", "*", "/"]),
        Button("Calculate", calculate_arithmetic),
        "Result: " + str(state.last_answer),
        Button("Home", index)
    ])

@route
def calculate_arithmetic(state: State, number1: str, number2: str, operation: str) -> Page:
    first = float(number1)
    second = float(number2)
    """
    Gathers at least two numbers to perform a simple equation courtesy of addition subtraction multiplicationa amd division
    There is no round function as the number1 and number 2 is a float.
    This layout wasd inspired by AI and it is similar through out the code.
    There is more stuff to add at a later date
    """
    if operation == "/" and second == 0.0:
        return Page(state, ["Error: Cannot divide by zero!", Button("Back", arithmetic)])
    answer = arithmetic_calculation(first, second, operation)
    state.last_answer = answer
    
    expression = str(first) + " " + operation + " " + str(second)
    state.calculations.append(
        Calculation(expression, answer, "Arithmetic")
    )
    
    return arithmetic(state)


def discriminant(a: float, b: float, c: float) -> float:
    return b * b - 4 * a * c

assert_equal(discriminant(5.0, 2.5, 2.0), -33.75)


def root_format(roots: list[float]) -> str:
    if len(roots) == 0:
        return "No real solutions"
    result = ""
    for i in range(len(roots)):
        if i > 0:
            result = result + " or "
        result = result + "x = " + str(roots[i])
    return result

assert_equal(root_format([-1.0, 5.0]), "x = -1.0 or x = 5.0")

def form_equation(a: float, b: float, c: float) -> str:
    return str(a) + "x^2 + " + str(b) + "x + " + str(c) + " = 0"

assert_equal(form_equation(1.0, 2.0, 1.0), "1.0x^2 + 2.0x + 1.0 = 0")

def solve_linear_equation(a: float, b: float, c: float) -> float:
    return (c - b) / a

assert_equal(solve_linear_equation(2.0, 5.0, 10.0), 2.5)

def solve_quadratic_equation(a: float, b:float, c:float) -> list[float]:
    discriminant_value = discriminant(a, b, c)
    if discriminant_value < 0:
        return []
    elif discriminant_value == 0:
        return [-b / (2 * a)]
    return [(-b + (discriminant_value ** 0.5)) / (2 * a), (-b - (discriminant_value ** 0.5)) / (2 * a)]
    

assert_equal(solve_quadratic_equation(1.0, 0.0, 1.0), [])

@route
def algebra(state: State) -> Page:
    state.current_page = "Algebra"
    return Page(state, [
        Header("Algebra Calculator"),
        "This section of the calculator can help solve equations such as linear or quadratic. It can also help solve equation and obtain values for the give variable",
        "Select equation type: Linear or Quadratic",
        SelectBox("equation", ["Linear", "Quadratic"]),
        "Enter a value",
        TextBox("coefficient_a"),
        "Enter b value",
        TextBox("coefficient_b"),
        "Enter c value",
        TextBox("coefficient_c"),
        Button("Solve", calculate_algebra),
        "Result: " + str(state.last_answer),
        Button("Home", index)
    ])

@route
def calculate_algebra(state: State, equation: str, coefficient_a: str, coefficient_b: str, coefficient_c: str) -> Page:
    a = float(coefficient_a)
    b = float(coefficient_b)
    c = float(coefficient_c)
    """
    Gathers at least two to three numbers depending on the equation wanted to solve or perform allowing you
    to find the value of the variable x shown in the code.
    In this code you will also be able to find the value of x and use those values to determine
    number of real roots.
    More updates to this is expected
    """
    
    if a == 0.0 :
        return Page(state, [
            "Error: a cannot be 0",
            Button("Back", algebra)
        ])
    
    if equation == "Linear":
        answer = solve_linear_equation(a, b, c)
        expression = coefficient_a + "x + " + coefficient_b + " = " + coefficient_c
        state.last_answer = answer
        state.calculations.append(Calculation(expression, answer, "Algebra"))
    elif equation == "Quadratic":
        roots = solve_quadratic_equation(a, b ,c)
        expression = coefficient_a + "x^2 + " + coefficient_b + "x + " + coefficient_c + " = 0"
        state.last_answer = roots
        state.calculations.append(Calculation(expression, roots, "Algebra"))

    return algebra(state)

def trig_calculator(angle: float, trig_operation: str, degree_mode: bool) -> float:
    if degree_mode == True:
        angle_in_radians = math.radians(angle)
    else:
        angle_in_radians = angle
        
    if trig_operation == "sin":
        return round(math.sin(angle_in_radians), 4)
    elif trig_operation == "cos":
        return round(math.cos(angle_in_radians), 4)
    elif trig_operation == "tan":
        return round(math.tan(angle_in_radians), 4)
    
assert_equal(trig_calculator(0.0, "sin", True), 0.0)
assert_equal(trig_calculator(math.pi / 2, "sin", False), 1.0)

@route
def trigonometry(state: State) -> Page:
    state.current_page = "Trigonmetry"
    if state.settings.degree_mode == True:
        mode = "Degrees"
    else:
        mode = "Radians"

    return Page(state, [
        Header("Trigonometry Calculator"),
        "Select trig function:",
        SelectBox("operation", ["sin", "cos", "tan"]),
        "Enter angle:",
        TextBox("angle"),
        "Use Degrees (uncheck for Radians):",
        CheckBox("degree_mode", state.settings.degree_mode),
        Button("Calculate", calculate_trigonometry),
        "Result: " + str(state.last_answer),
        Button("Home", index)
    ])

@route
def calculate_trigonometry(state: State, operation: str, angle: str, degree_mode: bool ) -> Page:
    """
    In this calculator you will use trig functions to find out the values of angles. Using the "import math", we are able to use the
    value of pi when you are find out values in radians.
    There is also a CheckBox for easy access to switch from on mode to another
    More updates are expected soon
    """
    state.settings.degree_mode = degree_mode
    angle_value = float(angle)
     
    if operation == "tan" and state.settings.degree_mode and (angle_value % 180 == 90):
        return Page(state, [
            "Error: tan(" + angle + "°) is undefined.",
            Button("Back", trigonometry)
        ])
    
    answer = trig_calculator(angle_value, operation, state.settings.degree_mode)
    state.last_answer = answer
    
    expression = operation + "(" + angle + ")"
    state.calculations.append(Calculation(expression, answer, "Trigonometry"))
    
    return trigonometry(state)

def generate_x_values(x_min: float, x_max: float) -> list[float]:
    x_values = []
    for x in range(x_min, x_max + 1):
        x_values.append(float(x))
    return x_values

assert_equal(generate_x_values(-2, 2), [-2.0, -1.0, 0.0, 1.0, 2.0])

def calculate_y_values(equation_type: str, a: float, b: float, c: float, x_values: list[float]) -> list[float]:
    y_values = []
    for x in x_values:
        if equation_type == "Linear":
            y = (a * x) + b
        else:
            y = (a * (x ** 2)) + (b * x) + c
        y_values.append(round(y, 2))
    return y_values

assert_equal(calculate_y_values("Linear", 2.0, 1.0, 0.0, [-1.0, 0.0, 1.0]), [-1.0, 1.0, 3.0])
assert_equal(calculate_y_values("Quadratic", 1.0, 0.0, -4.0, [-2.0, 0.0, 2.0]), [0.0, -4.0, 0.0])

def format_equation(equation_type: str, a: float, b: float, c: float) -> str:
    if equation_type == "Linear":
        return "y = " + str(a) + "x + " + str(b)
    return "y = " + str(a) + "x^2 + " + str(b) + "x + " + str(c)

assert_equal(format_equation("Linear", 2.0, 3.0, 0.0), "y = 2.0x + 3.0")
assert_equal(format_equation("Quadratic", 1.0, -2.0, 5.0), "y = 1.0x^2 + -2.0x + 5.0")

def build_plot(x_values: list[float], y_values: list[float], title: str, settings: Settings):
    fig, axes = plt.subplots()
    axes.plot(x_values, y_values, color=settings.line_color, marker="o")
    axes.axhline(0, color="black", linewidth=0.8)
    axes.axvline(0, color="black", linewidth=0.8)
    axes.grid(settings.show_grid)
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_title(title)
    return fig

@route
def graph(state: State) -> Page:
    state.current_page = "Graph"
    return Page(state, [
        Header("Function Grapher"),
        "Select function type (Linear: y = ax + b | Quadratic: y = ax^2 + bx + c):",
        SelectBox("equation_type", ["Linear", "Quadratic"]),
        "Enter a value:",
        TextBox("coef_a"),
        "Enter b value:",
        TextBox("coef_b"),
        "Enter c value (ignored for Linear):",
        TextBox("coef_c", "0"),
        "Select line color:",
        SelectBox("line_color", ["blue", "red", "green", "purple", "orange", "black"]),
        Button("Plot Graph", plot_graph),
        Button("Home", index)
    ])


@route
def plot_graph(state: State, equation_type: str, coef_a: str, coef_b: str, coef_c: str, line_color: str) -> Page:
    """
    This code is fully AI structured I made some tweak to the code to ensure it properly runs to own
    understanding. This code is the graphing side where you can use coefficients to linear and quadratic equations to ensure
    you get a graph with plots included
    More updates to this are garuanteed for easily understanding and access
    """
    a = float(coef_a)
    b = float(coef_b)
    c = float(coef_c)
    
    state.settings.line_color = line_color
    
    x_values = [float(x) for x in range(-10, 11)]
    y_values = []

    if equation_type == "Linear":
        expression = "y = " + coef_a + "x + " + coef_b
        for x in x_values:
            y_values.append(a*x + b)
    else:
        expression = "y = " + coef_a + "x^2 + " + coef_b + "x + " + coef_c
        for x in x_values:
            y_values.append(a * (x ** 2) + b * x + c)
                
    fig = build_plot(x_values, y_values, expression, state.settings)

    state.last_answer = "Plotted " + expression
    state.calculations.append(Calculation(expression, "Graphed", "Graph"))

    return Page(state, [
        Header("Graph Result: " + expression),
        MatPlotLibPlot(),
        Button("Graph Another Function", graph),
        Button("Home", index)
    ])

        
start_server(
    State(
        calculations = [],
        settings = Settings(True, True, "Blue"),
        current_page = "Home",
        last_answer = 0
    )   
)
