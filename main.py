import tkinter as tk
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

window = tk.Tk()
window.title("Calculus Calculator")
window.geometry("475x425")
window.resizable(False, False)
window.configure(bg = "#1e1e2e")

transformations = standard_transformations + (implicit_multiplication_application,)

safe_input = {
    "x": sp.Symbol("x"),
    "e": sp.E,
    "pi": sp.pi,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "csc": sp.csc,
    "sec": sp.sec,
    "cot": sp.cot,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "acsc": sp.acsc,
    "asec": sp.asec,
    "acot": sp.acot,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "csch": sp.csch,
    "sech": sp.sech,
    "coth": sp.coth,
    "log": lambda x: sp.log(x, 10),
    "ln": sp.log,
    "log10": lambda x: sp.log(x, 10),
    "sqrt": sp.sqrt,
    "cbrt": sp.cbrt,
    "exp": sp.exp,
    "abs": sp.Abs,
    "sign": sp.sign,
    "floor": sp.floor,
    "ceiling": sp.ceiling,
}

def sympy_to_display(expr):
    return str(expr).replace("log(", "ln(").replace("ln(x, 10)", "log(x)")

def validate_and_parse(user_input):
    clean_input = user_input.replace("^", "**")
    try:
        return parse_expr(clean_input, local_dict=safe_input, transformations=transformations)
    except:
        return None

def is_safe_x(user_input):
    try:
        float(user_input.strip())
        return True
    except ValueError:
        return False

def show_frame(frame):
    frame.tkraise()

menu_frame = tk.Frame(window, bg = "#1e1e2e")
limits_frame = tk.Frame(window, bg = "#1e1e2e")
derivatives_frame = tk.Frame(window, bg = "#1e1e2e")
integrals_frame = tk.Frame(window, bg = "#1e1e2e")

title = tk.Label(menu_frame, text = "Calculus Calculator", font = ("Arial", 20, "bold"), bg="#1e1e2e", fg="white")
title.pack(pady = 30)

for frame in (menu_frame, limits_frame, derivatives_frame, integrals_frame):
    frame.place(x=0, y=0, relwidth=1, relheight=1)

btn_limit = tk.Button(menu_frame, text = "Limits", width = 20, height = 2, font=("Arial", 12, "bold"), border=0, cursor="hand2", command=lambda: show_frame(limits_frame))
btn_limit.pack(pady = 10)

btn_derivative = tk.Button(menu_frame, text = "Derivatives", width = 20, height = 2, font=("Arial", 12, "bold"), border=0, cursor="hand2", command=lambda: show_frame(derivatives_frame))
btn_derivative.pack(pady = 10)

btn_integral = tk.Button(menu_frame, text = "Integrals", width = 20, height = 2, font=("Arial", 12, "bold"), border=0, cursor="hand2", command=lambda: show_frame(integrals_frame))
btn_integral.pack(pady = 10)

tk.Button(limits_frame, text = "Back", font = ("Arial", 12, "bold"), border = 0, cursor = "hand2", command = lambda: show_frame(menu_frame)).pack(pady=10)
tk.Button(derivatives_frame, text = "Back", font=("Arial", 12, "bold"), border = 0, cursor = "hand2", command = lambda: show_frame(menu_frame)).pack(pady=10)
tk.Button(integrals_frame, text = "Back", font=("Arial", 12, "bold"), border = 0, cursor = "hand2", command = lambda: show_frame(menu_frame)).pack(pady=10)

#Limits

tk.Label(limits_frame, text = "Enter a function in terms of x (e.g, x**2): ", font = ("Arial", 12), bg = "#1e1e2e").pack(pady=3)
func_input = tk.Entry(limits_frame, font = ("Arial", 12))
func_input.pack(pady = 3)

tk.Label(limits_frame, text = "Enter the value the function approaches: ", font = ("Arial", 12), bg = "#1e1e2e").pack(pady=3)
approach_x = tk.Entry(limits_frame, font = ("Arial", 12))
approach_x.pack(pady = 3)

limit_result_label = tk.Label(limits_frame, text = "", font = ("Arial", 12), bg = "#1e1e2e")
limit_result_label.pack(pady = 10)

def calculate_limit():
    raw_x = approach_x.get()
    raw_f = func_input.get()
    f = validate_and_parse(raw_f)
    if f is None or not is_safe_x(raw_x):
        limit_result_label.config(text = "Invalid or unsafe code")
        return
    try:
        x = sp.Symbol("x")
        app_val = float(raw_x)
        limit_f = sp.limit(f, x, app_val)
        limit_result_label.config(text=f"{func_input.get()} approaches {sympy_to_display(limit_f.evalf(4))} when x = {app_val}")
    except Exception as e:
        limit_result_label.config(text="Error in expression")
        print(e)

def graph_limit():
    f_sym = validate_and_parse(func_input.get())
    if f_sym is None:
        limit_result_label.config(text="Invalid or unsafe code")
        return
    try:
        x_obj = float(approach_x.get())
        x_val = x_obj
        f_num = sp.lambdify(sp.Symbol("x"), f_sym, "numpy")
        x_axis = np.linspace(x_val - 3, x_val + 3, 3000)
        y_axis = f_num(x_axis)
        y_axis = np.where(np.abs(y_axis) > 100, np.nan, y_axis)
        plt.figure()
        plt.plot(x_axis, y_axis, label = ("f(x) = " + str(func_input.get())))
        limit_val = sp.limit(f_sym, sp.Symbol("x"), x_obj)
        if limit_val.is_infinite or limit_val == sp.zoo:
            plt.ylim(-20, 20)
            plt.axvline(x=x_val, color="red", linestyle="--", label="Asymptote", linewidth=2.5, zorder=5)
        else:
            center_y = float(limit_val.evalf())
            plt.ylim(center_y - 10, center_y + 10)
            f_at_point = f_sym.subs(sp.Symbol("x"), x_obj)
            if sp.zoo == f_at_point or sp.nan == f_at_point:
                plt.plot(x_val, float(limit_val), "o", color="white", markeredgecolor="black", markersize=4, label = "The function is not continuous")
            else:
                plt.plot(x_val, float(limit_val), "o", color="black", markersize=4, label = "The function is continuous")
        plt.legend()
        plt.title(f"Graph of {func_input.get()}")
        plt.grid(True)
        plt.show()
    except Exception as e:
        limit_result_label.config(text="Error in expression")
        print(e)

tk.Button(limits_frame, text = "Calculate", font = ("Arial", 12, "bold"), border = 0,  command = calculate_limit).pack(pady=10)
tk.Button(limits_frame, text = "Graph", font = ("Arial", 12, "bold"), border = 0, command = graph_limit).pack(pady=10)

#Derivative

tk.Label(derivatives_frame, text = "Enter a function to differentiate: ", font = ("Arial", 12), bg = "#1e1e2e").pack(pady=3)
deriv_input = tk.Entry(derivatives_frame, font = ("Arial", 12))
deriv_input.pack(pady=3)

deriv_result_label = tk.Label(derivatives_frame, text = "", font = ("Arial", 12), bg = "#1e1e2e")
deriv_result_label.pack(pady=3)

def differentiation():
    f = validate_and_parse(deriv_input.get())
    if f is None:
        deriv_result_label.config(text = "Invalid function")
        return
    try:
        x = sp.Symbol("x")
        f_prime = sp.diff(f, x)
        deriv_result_label.config(text="d/dx of " + deriv_input.get() + " = " + sympy_to_display(f_prime))
    except Exception as e:
        deriv_result_label.config(text = "Error in expression")
        print(e)

tk.Button(derivatives_frame, text = "Calculate derivative", font = ("Arial", 12, "bold"), border = 0, command = differentiation).pack(pady=3)
tk.Label(derivatives_frame, text = "Enter the x-value for instantaneous rate of change", font = ("Arial", 12), bg = "#1e1e2e").pack(pady=3)
deriv_x = tk.Entry(derivatives_frame, font = ("Arial", 12))
deriv_x.pack(pady=3)

def instant_rate_of_change():
    raw_f = deriv_input.get()
    raw_x = deriv_x.get()
    f = validate_and_parse(raw_f)
    if f is None or not is_safe_x(raw_x):
        rate_of_change_result.config(text="Invalid or unsafe input")
        return
    try:
        x = sp.Symbol("x")
        f_prime = sp.diff(f, x)
        x_target = float(raw_x)
        rate_of_change = f_prime.subs(x, x_target)
        rate_of_change_result.config(text = "Rate of change is: " + str(rate_of_change.evalf(4)))
    except Exception as e:
        rate_of_change_result.config(text = "Error in expression")
        print(e)

rate_of_change_result = tk.Label(derivatives_frame, text="", font=("Arial", 12), bg="#1e1e2e")
rate_of_change_result.pack(pady=3)
tk.Button(derivatives_frame, text = "Calculate instantaneous rate of change", font = ("Arial", 12, "bold"), border = 0, bg = "#1e1e2e", command = instant_rate_of_change).pack(pady=3)

def graph_derivative():
    raw_f = deriv_input.get()
    raw_x = deriv_x.get()
    f = validate_and_parse(raw_f)
    if f is None or not is_safe_x(raw_x):
        rate_of_change_result.config(text="Invalid or unsafe input")
        return
    try:
        x = sp.Symbol("x")
        f_prime = sp.diff(f, x)
        x_obj = float(raw_x)
        x_val = x_obj
        f_val = f.subs(x, x_val)
        rate_of_change = f_prime.subs(x, x_val)
        tangent = rate_of_change * (x - x_val) + f.subs(x, x_val)
        tangent_equation = sp.expand(tangent)
        x_axis = np.linspace(x_val - 3, x_val + 3, 1000)
        f_lambdify = sp.lambdify(x, f, "numpy")
        tangent_lambdify = sp.lambdify(x, tangent, "numpy")
        y_values = f_lambdify(x_axis)
        y_values = np.where(np.abs(y_values) > 100, np.nan, y_values)
        plt.figure()
        plt.title("Graph of " + str(deriv_input.get() + " and its tangent at x = " + str(deriv_x.get())))
        plt.plot(x_axis, y_values, label=deriv_input.get())
        plt.plot(x_axis, tangent_lambdify(x_axis), label=("Tangent: " + str(tangent_equation)))
        if f_val.is_real:
            f_float = float(f_val.evalf())
            plt.ylim(f_float - 10, f_float + 10)
            plt.plot(x_val, (f.subs(x, x_val)).evalf(), "o", color="red", label=f"Point: ({x_val}, {float(f.subs(x, x_val)):.2f})")
        else:
            plt.ylim(-20, 20)
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        deriv_result_label.config(text="Error in expression")
        print(e)

tk.Button(derivatives_frame, text = "Graph", font = ("Arial", 12, "bold"), bg = "#1e1e2e", border = 0, command = graph_derivative).pack(pady=3)

#Integrals

tk.Label(integrals_frame, text = "Enter a function f to integrate: ", font = ("Arial", 12), bg = "#1e1e2e").pack(pady=3)
f_input = tk.Entry(integrals_frame, font = ("Arial", 12))
f_input.pack(pady=3)
antiderivative_label = tk.Label(integrals_frame, text = "", font = ("Arial", 12), bg = "#1e1e2e")
antiderivative_label.pack(pady=3)

def antiderivative():
    raw_f = f_input.get()
    f = validate_and_parse(raw_f)
    if f is None:
        antiderivative_label.config(text = "Invalid or unsafe input")
        return
    try:
        x = sp.Symbol("x")
        F = sp.integrate(f, x)
        antiderivative_label.config(text="∫ " + f_input.get() + " = " + sympy_to_display(F))
    except Exception as e:
        antiderivative_label.config(text = "Error in expression")
        print(e)

tk.Button(integrals_frame, text = "Find antiderivative", font = ("Arial", 12, "bold"), border = 0, command = antiderivative).pack(pady=3)

tk.Label(integrals_frame, text = "Enter a function g for definite integral (enter 0 for only f): ", font = ("Arial", 12), bg = "#1e1e2e").pack(pady=3)
g_input = tk.Entry(integrals_frame, font = ("Arial", 12))
g_input.pack(pady=3)

tk.Label(integrals_frame, text = "Enter lower and upper x-values for definite integral: ", font = ("Arial", 12), bg = "#1e1e2e").pack(pady=3)
input_frame = tk.Frame(integrals_frame, bg = "#1e1e2e")
input_frame.pack(pady = 3)

tk.Label(input_frame, text = "Lower: ", font = ("Arial", 12), bg = "#1e1e2e").grid(row = 0, column = 0, padx = 5)
lower_input = tk.Entry(input_frame, font = ("Arial", 12), width = 6)
lower_input.grid(row = 0, column = 1, padx = 5)

tk.Label(input_frame, text = "Upper:", font = ("Arial", 12), bg = "#1e1e2e").grid(row=0, column=2, padx=5)
upper_input = tk.Entry(input_frame, font = ("Arial", 12), width = 6)
upper_input.grid(row=0, column=3, padx=5)

area_label = tk.Label(integrals_frame, text = "", font = ("Arial", 12), bg = "#1e1e2e")
area_label.pack(pady = 3)

def definite_integral():
    raw_x1 = lower_input.get()
    raw_x2 = upper_input.get()
    if not is_safe_x(raw_x1) or not is_safe_x(raw_x2):
        area_label.config(text = "Invalid or unsafe input")
        return
    raw_f = f_input.get()
    raw_g = g_input.get()
    f = validate_and_parse(raw_f)
    g = validate_and_parse(raw_g)
    if f is None or g is None:
        area_label.config(text = "Invalid or unsafe input")
        return
    try:
        x = sp.Symbol("x")
        x1 = float(raw_x1)
        x2 = float(raw_x2)
        if x1 >= x2:
            area_label.config(text = "Lower bound must be less than upper bound")
            return
        else:
            F = sp.integrate(f, (x, x1, x2))
            G = sp.integrate(g, (x, x1, x2))
            if F.is_infinite or G.is_infinite or F == sp.zoo or G == sp.zoo:
                area_label.config(text = "Error, a function approaches infinity")
                return
            else:
                area = round(float(sp.Abs(F - G)), 4)
                area_label.config(text = f"The area between {f} and {g} is {area}")
    except Exception as e:
        area_label.config(text = "Error in expression")
        print(e)

tk.Button(integrals_frame, text = "Calculate area", font = ("Arial", 12, "bold"), border = 0, command = definite_integral).pack(pady=3)

def graph_integral():
    raw_x1 = lower_input.get()
    raw_x2 = upper_input.get()
    if not is_safe_x(raw_x1) or not is_safe_x(raw_x2):
        area_label.config(text="Invalid or unsafe input")
        return
    raw_f = f_input.get()
    raw_g = g_input.get()
    f = validate_and_parse(raw_f)
    g = validate_and_parse(raw_g)
    if f is None or g is None:
        area_label.config(text="Invalid or unsafe input")
        return
    try:
        x = sp.Symbol("x")
        x1 = float(raw_x1)
        x2 = float(raw_x2)
        if x1 >= x2:
            area_label.config(text = "Lower bound must be less than upper bound")
            return
        else:
            f_np = sp.lambdify(x, f, "numpy")
            g_np = sp.lambdify(x, g, "numpy")
        x_vals = np.linspace(x1-1, x2+1, 1000)
        f_vals = f_np(x_vals)
        g_vals = g_np(x_vals)
        f_vals = np.where(np.abs(f_vals) > 100, np.nan, f_vals)  
        g_vals = np.where(np.abs(g_vals) > 100, np.nan, g_vals)
        plt.figure()
        plt.title(f"Area between {raw_f} and {raw_g}")
        plt.plot(x_vals, f_vals, label=f"f(x) = {raw_f}")
        plt.plot(x_vals, g_vals, label=f"g(x) = {raw_g}")
        x_fill = np.linspace(x1, x2, 1000)
        plt.fill_between(x_fill, f_np(x_fill), g_np(x_fill), alpha = 0.3, label = "Area")
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        area_label.config(text = "Error in expression")
        print(e)
tk.Button(integrals_frame, text = "Graph", font = ("Arial", 12, "bold"), border = 0, command = graph_integral).pack(pady = 3)

show_frame(menu_frame)
window.mainloop()
