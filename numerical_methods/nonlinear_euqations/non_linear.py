import numpy as np

# Definicje funkcji badanych i ich pochodnych

# Funkcja 1
def f1(x):
    return -x ** 3 + 10 * x + 5


def df1(x):
    return -3 * x ** 2 + 10


# Funkcja 2
def f2(x):
    return x ** 4 - 3 * x ** 2 + 2


def df2(x):
    return 4 * x ** 3 - 6 * x


# Funkcja 3
def f3(x):
    return x ** 3 - 7 * x ** 2 + 14 * x - 6


def df3(x):
    return 3 * x ** 2 - 14 * x + 14


# Implementacja metod numerycznych

def newton_method(f, df, x0, max_iter, epsilon):
    """
    Rozwiązuje równanie nieliniowe metodą stycznych (Newtona).
    """
    print("\n--- Metoda stycznych (Newtona) ---")
    x = x0

    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)

        # Zabezpieczenie przed dzieleniem przez 0
        if dfx == 0:
            print(f"Błąd: Pochodna w punkcie {x} wynosi 0. Przerwanie algorytmu.")
            return None

        x_new = x - fx / dfx

        err_x = abs(x_new - x)
        err_f = abs(f(x_new))

        print(
            f"Iteracja {i + 1}: x = {x_new:.6f}, f(x) = {f(x_new):.6f}, błąd x = {err_x:.6f}, błąd f(x) = {err_f:.6f}")

        # Sprawdzenie warunków stopu
        if err_x < epsilon:
            print(f"Osiągnięto zadaną dokładność błędu przyrostu x (|x_k+1 - x_k| < {epsilon}).")
            return x_new
        if err_f < epsilon:
            print(f"Osiągnięto zadaną dokładność błędu wartości funkcji (|f(x_k+1)| < {epsilon}).")
            return x_new

        x = x_new

    print(f"Osiągnięto maksymalną liczbę iteracji ({max_iter}).")
    return x


def secant_method(f, x0, max_iter, epsilon):
    """
    Rozwiązuje równanie nieliniowe metodą siecznych.
    """
    print("\n--- Metoda siecznych ---")
    x_prev = x0 - 0.1
    x_curr = x0

    for i in range(max_iter):
        f_prev = f(x_prev)
        f_curr = f(x_curr)

        # Zabezpieczenie przed dzieleniem przez 0
        if f_curr - f_prev == 0:
            print(f"Błąd: f(x_k) - f(x_k-1) wynosi 0. Przerwanie algorytmu.")
            return None

        x_new = x_curr - f_curr * ((x_curr - x_prev) / (f_curr - f_prev))

        err_x = abs(x_new - x_curr)
        err_f = abs(f(x_new))

        print(
            f"Iteracja {i + 1}: x = {x_new:.6f}, f(x) = {f(x_new):.6f}, błąd x = {err_x:.6f}, błąd f(x) = {err_f:.6f}")

        # Sprawdzenie warunków stopu
        if err_x < epsilon:
            print(f"Osiągnięto zadaną dokładność błędu przyrostu x (|x_k+1 - x_k| < {epsilon}).")
            return x_new
        if err_f < epsilon:
            print(f"Osiągnięto zadaną dokładność błędu wartości funkcji (|f(x_k+1)| < {epsilon}).")
            return x_new

        x_prev = x_curr
        x_curr = x_new

    print(f"Osiągnięto maksymalną liczbę iteracji ({max_iter}).")
    return x_curr

# Wywołania programu dla poszczególnych funkcji

epsilon = 1e-5

print(48*"-")
print("Funkcja 1: f(x) = -x^3 + 10x + 5")
print(48*"-")
newton_method(f1, df1, x0=6.0, max_iter=10, epsilon=epsilon)
print("\nWartość dokładna: x = 3.3876")
secant_method(f1, x0=6.0, max_iter=10, epsilon=epsilon)
print("\nWartość dokładna: x = 3.3876\n")


print(48*"-")
print("Funkcja 2: f(x) = x^4 - 3x^2 + 2")
print(48*"-")
newton_method(f2, df2, x0=2.0, max_iter=10, epsilon=epsilon)
print("\nWartość dokładna: x = 1.4142 (sqrt(2)) lub x = 1.0")
secant_method(f2, x0=2.0, max_iter=10, epsilon=epsilon)
print("\nWartość dokładna: x = 1.4142 (sqrt(2)) lub x = 1.0\n")


print(48*"-")
print("Funkcja 3: f(x) = x^3 - 7x^2 + 14x - 6")
print(48*"-")
newton_method(f3, df3, x0=4.0, max_iter=10, epsilon=epsilon)
print(
    "\nWartość dokładna: x = 3.4142 (2 + sqrt(2)) lub x = 3 lub x = 0.58579 (2 - sqrt(2))")
secant_method(f3, x0=4.0, max_iter=10, epsilon=epsilon)
print(
    "\nWartość dokładna: x = 3.4142 (2 + sqrt(2)) lub x = 3 lub x = 0.58579 (2 - sqrt(2))")