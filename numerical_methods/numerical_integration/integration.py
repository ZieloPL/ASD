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


# Definicje funkcji podcałkowych oraz ich właściwości do wyświetlenia
functions_to_integrate = [
    {
        "formula": "sin(x)",
        "func": lambda x: np.sin(x),
        "a": 0.5,
        "b": 2.5
    },
    {
        "formula": "x^2 + 2x + 5",
        "func": lambda x: x ** 2 + 2 * x + 5,
        "a": 0.5,
        "b": 5.0
    },
    {
        "formula": "exp(x)",
        "func": lambda x: np.exp(x),
        "a": 0.5,
        "b": 5.0
    }
]

print("--- Zadanie 1  ---\n")

n_fixed = 20

for item in functions_to_integrate:
    f = item["func"]
    a = item["a"]
    b = item["b"]
    formula = item["formula"]

    rect_val = rectangle_method(f, a, b, n_fixed)
    trap_val = trapezoidal_method(f, a, b, n_fixed)
    simp_val = simpson_method(f, a, b, n_fixed)

    print(f"Wzór całkowanej funkcji: f(x) = {formula}")
    print(f"Przedział całkowania: <{a}, {b}>")
    print(f"Liczba przedziałów: {n_fixed}")
    print(f" Metoda prostokątów: {rect_val:.6f}")
    print(f" Metoda trapezów:    {trap_val:.6f}")
    print(f" Metoda Simpsona:     {simp_val:.6f}")
    print("-" * 40)
    print()

# ZADANIE 2

n_values = [2, 4, 6, 8, 10, 20, 30, 40, 50]
# n_values = [3, 5, 7, 9, 11, 21, 31, 41, 51]

for item in functions_to_integrate:
    f = item["func"]
    a = item["a"]
    b = item["b"]
    formula = item["formula"]

    rect_results = []
    trap_results = []
    simp_results = []

    for n in n_values:
        rect_results.append(rectangle_method(f, a, b, n))
        trap_results.append(trapezoidal_method(f, a, b, n))
        simp_results.append(simpson_method(f, a, b, n))

    # Rysowanie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, rect_results, marker='o', label='Metoda prostokątów', linestyle='--')
    plt.plot(n_values, trap_results, marker='s', label='Metoda trapezów', linestyle='-.')
    plt.plot(n_values, simp_results, marker='^', label='Metoda Simpsona', linestyle=':')

    plt.title(f"Analiza dokladnosci dla całki z f(x) = {formula} w przedziale <{a}, {b}>")
    plt.xlabel("Liczba przedziałów (n)")
    plt.ylabel("Obliczona wartość calki")

    plt.legend()
    plt.grid(True)

    plt.show()