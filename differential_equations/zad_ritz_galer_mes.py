import numpy as np
from scipy import integrate
import pandas as pd

# 1. DEFINICJA PROBLEMU I ROZWIĄZANIE DOKŁADNE

# Przedział [a, b]
a = 0
b = np.pi / 4


# Rozwiązanie dokładne
def y_exact(x):
    return -1 / 3 * np.cos(2 * x) - (np.sqrt(2) / 6) * np.sin(2 * x) + 1 / 3 * np.cos(x)


n_parts = 5
nodes = np.linspace(a, b, n_parts + 1)


# 2. IMPLEMENTACJA METOD GLOBALNYCH (RITZ / GALERKIN)


def solve_global(basis_funcs, d_basis_funcs, N):
    """
    Rozwiązuje problem y'' + 4y = cos(x) metodą ważonych reziduów.
    Forma słaba: integral(y'w' - 4yw)dx = - integral(cos(x)w)dx
    Dla operatora samosprzężonego macierze Ritza i Galerkina są identyczne,
    różnicę wprowadzamy dobierając różne funkcje bazowe.
    """
    K = np.zeros((N, N))
    F = np.zeros(N)


    rhs_func = lambda x: np.cos(x)

    for i in range(N):
        for j in range(N):

            integrand_k = lambda x: d_basis_funcs[j](x) * d_basis_funcs[i](x) - 4 * basis_funcs[j](x) * basis_funcs[i](
                x)
            K[i, j], _ = integrate.quad(integrand_k, a, b)


        integrand_f = lambda x: -rhs_func(x) * basis_funcs[i](x)
        F[i], _ = integrate.quad(integrand_f, a, b)

    coeffs = np.linalg.solve(K, F)

    # Konstrukcja funkcji wynikowej
    def solution(x):
        return sum(coeffs[k] * basis_funcs[k](x) for k in range(N))

    return solution


# --- METODA 1: RITZA (Baza Wielomianowa) ---
N_ritz = 4  # Liczba funkcji bazowych (dopasowana do liczby węzłów wewnętrznych w MES)
ritz_basis = [lambda x, k=k: (x ** k) * (b - x) for k in range(1, N_ritz + 1)]
d_ritz_basis = [lambda x, k=k: k * (x ** (k - 1)) * (b - x) - x ** k for k in range(1, N_ritz + 1)]

y_ritz_func = solve_global(ritz_basis, d_ritz_basis, N_ritz)

# --- METODA 2: GALERKINA (Baza Trygonometryczna) ---
N_galerkin = 4
galerkin_basis = [lambda x, k=k: np.sin(4 * k * x) for k in range(1, N_galerkin + 1)]
d_galerkin_basis = [lambda x, k=k: 4 * k * np.cos(4 * k * x) for k in range(1, N_galerkin + 1)]

y_galerkin_func = solve_global(galerkin_basis, d_galerkin_basis, N_galerkin)


# 3. IMPLEMENTACJA METODY ELEMENTÓW SKOŃCZONYCH (MES)


def solve_fem(n_elements):
    # Generowanie siatki
    x_nodes = np.linspace(a, b, n_elements + 1)
    h = x_nodes[1] - x_nodes[0]  # Długość elementu

    n_nodes = n_elements + 1
    K_global = np.zeros((n_nodes, n_nodes))
    F_global = np.zeros(n_nodes)


    k_local_diff = (1 / h) * np.array([[1, -1], [-1, 1]])

    k_local_mass = 4 * (h / 6) * np.array([[2, 1], [1, 2]])

    k_local = k_local_diff - k_local_mass

    # Agregacja
    for i in range(n_elements):
        # Indeksy węzłów elementu
        idx = [i, i + 1]


        K_global[np.ix_(idx, idx)] += k_local

        x_elem = np.linspace(x_nodes[i], x_nodes[i + 1], 11)

        phi1 = (x_nodes[i + 1] - x_elem) / h
        phi2 = (x_elem - x_nodes[i]) / h

        val1 = integrate.simpson(-np.cos(x_elem) * phi1, x_elem)
        val2 = integrate.simpson(-np.cos(x_elem) * phi2, x_elem)

        F_global[i] += val1
        F_global[i + 1] += val2


    # Lewy brzeg (indeks 0)
    K_global[0, :] = 0
    K_global[:, 0] = 0
    K_global[0, 0] = 1
    F_global[0] = 0

    # Prawy brzeg (indeks -1)
    K_global[-1, :] = 0
    K_global[:, -1] = 0
    K_global[-1, -1] = 1
    F_global[-1] = 0

    # Rozwiązanie
    U = np.linalg.solve(K_global, F_global)
    return U


y_fem_values = solve_fem(n_parts)

# 4. GENEROWANIE TABELI WYNIKÓW


data = []
for i, x_val in enumerate(nodes):
    exact = y_exact(x_val)

    # Wartości przybliżone
    val_ritz = y_ritz_func(x_val)
    val_gal = y_galerkin_func(x_val)
    val_fem = y_fem_values[i]

    # Błędy bezwzględne
    err_ritz = abs(val_ritz - exact)
    err_gal = abs(val_gal - exact)
    err_fem = abs(val_fem - exact)

    data.append([
        x_val,
        exact,
        val_ritz, err_ritz,
        val_gal, err_gal,
        val_fem, err_fem
    ])

# DataFrame
columns = [
    "x", "Dokładna",
    "Ritz (Wielomian)", "|Błąd R|",
    "Galerkin (Sinus)", "|Błąd G|",
    "MES (Liniowe)", "|Błąd MES|"
]

df = pd.DataFrame(data, columns=columns)


pd.options.display.float_format = '{:,.6f}'.format
print("Tabela wyników dla podziału na 5 części:\n")
print(df.to_string(index=False))

import matplotlib.pyplot as plt

x_plot = np.linspace(a, b, 100)
plt.figure(figsize=(10, 6))
plt.plot(x_plot, y_exact(x_plot), 'k-', linewidth=2, label='Dokładne')
plt.plot(x_plot, [y_ritz_func(x) for x in x_plot], 'r--', label='Ritz (Wielomian)')
plt.plot(x_plot, [y_galerkin_func(x) for x in x_plot], 'g:', label='Galerkin (Sinus)')
plt.plot(nodes, y_fem_values, 'bo-', label='MES (węzły)')
plt.legend()
plt.title("Porównanie metod: Ritz, Galerkin, MES")
plt.grid(True)
plt.xlabel("x")
plt.ylabel("y(x)")
plt.show()