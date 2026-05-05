import numpy as np
import matplotlib.pyplot as plt

def rectangle_method(f, a, b, n):
    """Oblicza całkę metodą prostokątów"""
    s = (b - a) / n
    integral = 0
    for i in range(n):
        integral += f(a + i * s + 0.5 * s)
    return s * integral


def trapezoidal_method(f, a, b, n):
    """Oblicza całkę metodą trapezów."""
    s = (b - a) / n
    integral = 0
    for i in range(n):
        integral += (s / 2) * (f(a + i * s) + f(a + (i + 1) * s))
    return integral


def simpson_method(f, a, b, n):
    """Oblicza całkę z metody Simpsona dla parzystej liczby przedziałów."""
    # if n % 2 != 0:
    #     raise ValueError("Liczba przedziałów 'n' w metodzie Simpsona musi być parzysta.")

    h = (b - a) / n
    integral = f(a) + f(b)

    for i in range(1, n):
        x_i = a + i * h
        if i % 2 == 0:
            integral += 2 * f(x_i)
        else:
            integral += 4 * f(x_i)

    return integral * (h / 3)


def gauss_legendre_method(f, a, b, n):
    """Oblicza całkę metodą Gaussa-Legendre'a"""
    if n == 2:
        nodes = [-np.sqrt(1 / 3), np.sqrt(1 / 3)]
        weights = [1.0, 1.0]
    elif n == 3:
        nodes = [-np.sqrt(3 / 5), 0.0, np.sqrt(3 / 5)]
        weights = [5 / 9, 8 / 9, 5 / 9]
    elif n == 4:
        val1 = np.sqrt(525 + 70 * np.sqrt(30)) / 35
        val2 = np.sqrt(525 - 70 * np.sqrt(30)) / 35
        w1 = (18 - np.sqrt(30)) / 36
        w2 = (18 + np.sqrt(30)) / 36

        nodes = [-val1, -val2, val2, val1]
        weights = [w1, w2, w2, w1]
    else:
        raise ValueError("Ta implementacja obsługuje tylko n równe 2, 3 lub 4.")

    integral = 0.0
    for x_i, A_i in zip(nodes, weights):
        # Przeskalowanie zadania do przedziału [-1, 1]
        t_i = (a + b) / 2 + ((b - a) / 2) * x_i
        integral += A_i * f(t_i)

    # Mnożenie sumy przez współczynnik skalujący
    return ((b - a) / 2) * integral


functions_to_integrate = [
    {
        "formula": "sin(x)",
        "func": lambda x: np.sin(x),
        "a": 0.5,
        "b": 2.5,
        "exact": np.cos(0.5) - np.cos(2.5)
    },
    {
        "formula": "x^2 + 2x + 5",
        "func": lambda x: x ** 2 + 2 * x + 5,
        "a": 0.5,
        "b": 5.0,
        "exact": ((5.0 ** 3) / 3 + 5.0 ** 2 + 5 * 5.0) - ((0.5 ** 3) / 3 + 0.5 ** 2 + 5 * 0.5)
    },
    {
        "formula": "exp(x)",
        "func": lambda x: np.exp(x),
        "a": 0.5,
        "b": 5.0,
        "exact": np.exp(5) - np.exp(0.5)
    }
]

print("--- Zadanie 1  ---\n")

n_fixed = 20

for item in functions_to_integrate:
    f = item["func"]
    a = item["a"]
    b = item["b"]
    formula = item["formula"]
    exact_val = item["exact"]

    # Obliczenia dla metod z poprzedniego laba
    rect_val = rectangle_method(f, a, b, n_fixed)
    trap_val = trapezoidal_method(f, a, b, n_fixed)
    simp_val = simpson_method(f, a, b, n_fixed)

    # Obliczenia metodą Gaussa-Legendre'a
    gl_2 = gauss_legendre_method(f, a, b, 2)
    gl_3 = gauss_legendre_method(f, a, b, 3)
    gl_4 = gauss_legendre_method(f, a, b, 4)

    print(f"Wzór całkowanej funkcji: f(x) = {formula}")
    print(f"Przedział całkowania: <{a}, {b}>")
    print(f"\nWartość dokładna (analityczna): {exact_val:.6f}\n")
    print("-" * 45)
    print(f" Metoda prostokątów (n={n_fixed}): {rect_val:.6f}")
    print(f" Metoda trapezów    (n={n_fixed}): {trap_val:.6f}")
    print(f" Metoda Simpsona    (n={n_fixed}): {simp_val:.6f}")
    print("-" * 45)
    print(f" Metoda Gaussa-Legendre'a (n=2): {gl_2:.6f}")
    print(f" Metoda Gaussa-Legendre'a (n=3): {gl_3:.6f}")
    print(f" Metoda Gaussa-Legendre'a (n=4): {gl_4:.6f}")
    print("-" * 45)
    print()
