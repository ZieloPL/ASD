import numpy as np


def gauss_partial_pivoting(A, B):
    """
    Rozwiązuje układ równań liniowych Ax = B metodą eliminacji Gaussa
    z częściowym wyborem elementu głównego.
    """
    n = len(B)
    M = np.zeros((n, n + 1))
    M[:, :-1] = A
    M[:, -1] = B

    for i in range(n):
        max_row = i + np.argmax(np.abs(M[i:, i]))
        if i != max_row:
            M[[i, max_row]] = M[[max_row, i]]

        if M[i, i] == 0:
            raise ValueError("Macierz jest osobliwa, układ nie ma jednoznacznego rozwiązania.")

        for j in range(i + 1, n):
            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (M[i, -1] - np.dot(M[i, i + 1:n], x[i + 1:])) / M[i, i]

    return x


def calculate_polynomial(a_coeffs, x_val):
    """Oblicza wartość wielomianu dla zadanego x i współczynników a."""
    result = 0
    for j, a in enumerate(a_coeffs):
        result += a * (x_val ** j)
    return result


# Stopień wielomianu, węzły, wartości, wagi
degree = 1  # aproksymacja liniowa
x_nodes = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
y_values = np.array([2, 4, 3, 5, 6, 9, 11, 11], dtype=float)

# Wagi równe 1 dla wszystkich punktów
weights = np.ones(len(x_nodes), dtype=float)

n = degree
m = len(x_nodes) - 1  # m+1 to liczba punktów
num_nodes = m + 1


# Budowa układu równań (Macierz Grama i wektor F)

G = np.zeros((n + 1, n + 1))
F = np.zeros(n + 1)

for k in range(n + 1):
    for j in range(n + 1):
        # g_kj = sum( w_i * x_i^(k+j) )
        G[k, j] = np.sum(weights * (x_nodes ** (k + j)))

    # F_k = sum( w_i * y_i * x_i^k )
    F[k] = np.sum(weights * y_values * (x_nodes ** k))

# Rozwiązanie układu równań

# Rozwiązanie metodą Gaussa z częściowym wyborem elementu głównego
a_coeffs = gauss_partial_pivoting(G, F)

# Obliczenia końcowe i wypisywanie wyników

print(40 * "-")
print(" Wyniki aproksymacji średniokwadraturowej")
print(40 * "-")
print(f"Liczba węzłów: {num_nodes}")
print(f"Stopień wielomianu aproksymującego (n): {degree}\n")

print("Współczynniki wielomianu aproksymującego:")
for i, a in enumerate(a_coeffs):
    print(f" a_{i} = {a:.4f}")
print()

print(f"{'Węzeł x_i':>10} | {'Wartość y_i (dana)':>20} | {'Wartość F(x_i) (obliczona)':>25}")
print("-" * 68)

error_E = 0
for i in range(num_nodes):
    x_i = x_nodes[i]
    y_i = y_values[i]
    w_i = weights[i]

    # Obliczona wartość z wielomianu
    f_x_i = calculate_polynomial(a_coeffs, x_i)

    print(f"{x_i:10.1f} | {y_i:20.1f} | {f_x_i:25.4f}")

    # Sumowanie błędu średniokwadratowego:
    error_E += w_i * ((y_i - f_x_i) ** 2)

print("-" * 68)
print(f"\nWartość funkcjonału błędu E: {error_E:.4f}")