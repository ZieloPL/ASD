import numpy as np
import matplotlib.pyplot as plt


# Rozwiązuje zagadnienie początkowe metodą Eulera.
def euler_method(f, x0, y0, x_end, N):
    h = (x_end - x0) / N
    x, y = x0, y0
    for _ in range(N):
        y = y + h * f(x, y)
        x = x + h
    return y

# Rozwiązuje zagadnienie początkowe metodą RK2
def rk2_method(f, x0, y0, x_end, N):
    h = (x_end - x0) / N
    x, y = x0, y0
    for _ in range(N):
        k1 = f(x, y)
        k2 = f(x + h, y + h * k1)
        y = y + (h / 2) * (k1 + k2)
        x = x + h
    return y


# Rozwiązuje zagadnienie początkowe metodą RK4
def rk4_method(f, x0, y0, x_end, N):
    h = (x_end - x0) / N
    x, y = x0, y0
    for _ in range(N):
        k1 = f(x, y)
        k2 = f(x + h / 2, y + h * k1 / 2)
        k3 = f(x + h / 2, y + h * k2 / 2)
        k4 = f(x + h, y + h * k3)
        y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x = x + h
    return y

problems = [
    {
        "name": "y'(x) = x^2 + y",
        "f": lambda x, y: x ** 2 + y,
        "x0": 0.0,
        "y0": 0.1,
        "x_end": 1.0,
        "exact": lambda x:  - x ** 2 - 2 * x + 2.1 * np.exp(x) - 2  # Rozwiazanie analityczne
    },
    {
        "name": "y'(x) = x + y",
        "f": lambda x, y: x + y,
        "x0": 0.0,
        "y0": 0.1,
        "x_end": 1.0,
        "exact": lambda x: 1.1 * np.exp(x) - x - 1  # Rozwiazanie analityczne
    }
]

N_fixed = 10
print(f'\n--- WYNIKI DLA N = {N_fixed} ---')

for prob in problems:
    h = (prob["x_end"] - prob["x0"]) / N_fixed
    y_euler = euler_method(prob["f"], prob["x0"], prob["y0"], prob["x_end"], N_fixed)
    y_rk2 = rk2_method(prob["f"], prob["x0"], prob["y0"], prob["x_end"], N_fixed)
    y_rk4 = rk4_method(prob["f"], prob["x0"], prob["y0"], prob["x_end"], N_fixed)

    print(f"\nRównanie: {prob['name']}")
    print(f"1. Warunek początkowy: y({prob['x0']}) = {prob['y0']}")
    print(f"2. Punkt końcowy: x = {prob['x_end']}")
    print(f"3. Krok obliczeń (h): {h}")
    print(f"4. Rozwiązanie Euler: {y_euler:.6f}")
    print(f"5. Rozwiązanie RK2:   {y_rk2:.6f}")
    print(f"6. Rozwiązanie RK4:   {y_rk4:.6f}")
    print(f"   (Wartość dokładna: {prob['exact'](prob['x_end']):.6f})")


# Rozne wartosic N
N_values = [2, 4, 10, 20, 50, 100, 200]

for prob in problems:
    errors_euler = []
    errors_rk2 = []
    errors_rk4 = []

    exact_val = prob['exact'](prob['x_end'])

    for N in N_values:
        err_e = abs(euler_method(prob["f"], prob["x0"], prob["y0"], prob["x_end"], N) - exact_val)
        err_rk2 = abs(rk2_method(prob["f"], prob["x0"], prob["y0"], prob["x_end"], N) - exact_val)
        err_rk4 = abs(rk4_method(prob["f"], prob["x0"], prob["y0"], prob["x_end"], N) - exact_val)

        errors_euler.append(err_e)
        errors_rk2.append(err_rk2)
        errors_rk4.append(err_rk4)

    # Tworzenie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(N_values, errors_euler, marker='o', label='Błąd Eulera')
    plt.plot(N_values, errors_rk2, marker='s', label='Błąd RK2')
    plt.plot(N_values, errors_rk4, marker='^', label='Błąd RK4')

    plt.yscale('log')
    plt.xscale('log')
    plt.title(f"Badanie zbieżności dla równania: {prob['name']}")
    plt.xlabel("Liczba kroków (N)")
    plt.ylabel("Błąd bezwzględny")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.show()