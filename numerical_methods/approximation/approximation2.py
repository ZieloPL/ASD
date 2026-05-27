import numpy as np

def inner_product(u, v, weights):
    """Oblicza dyskretny iloczyn skalarny z wagami."""
    return np.sum(weights * u * v)


def evaluate_phi(x_val, j, alphas):
    """
    Oblicza wartość wielomianu bazowego phi_j(x) w dowolnym punkcie x_val.
    Zgodnie ze wzorem korzysta z rekurencji i zapisanych współczynników rzutu alpha.
    """
    # Baza rekurencji dla phi_0(x) = 1
    if j == 0:
        return np.ones_like(x_val, dtype=float)

    # phi_j(x) = x^j - sum( alpha_{jk} * phi_k(x) )
    phi_val = x_val ** j
    for k in range(j):
        phi_val = phi_val - alphas[j, k] * evaluate_phi(x_val, k, alphas)

    return phi_val


def evaluate_F(x_val, a_coeffs, alphas):
    """Oblicza ostateczną wartość wielomianu aproksymującego F(x)."""
    F_val = np.zeros_like(x_val, dtype=float)
    for j in range(len(a_coeffs)):
        F_val += a_coeffs[j] * evaluate_phi(x_val, j, alphas)
    return F_val

degree = 1
x_nodes = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
y_values = np.array([2, 4, 3, 5, 6, 9, 11, 11], dtype=float)
weights = np.ones_like(x_nodes, dtype=float)

n = degree
m = len(x_nodes) - 1
num_nodes = m + 1

# Macierz do przechowywania wartości wielomianów phi w węzłach
# wiersz = j-ty wielomian, kolumna = i-ty węzeł
phi_nodes = np.zeros((n + 1, num_nodes))
alphas = np.zeros((n + 1, n + 1))

# phi_0 = 1
phi_nodes[0] = np.ones(num_nodes)

# Konstrukcja kolejnych wielomianów
for j in range(1, n + 1):
    x_j = x_nodes ** j

    # Obliczanie rzutów alphas
    for k in range(j):
        num = inner_product(x_j, phi_nodes[k], weights)
        den = inner_product(phi_nodes[k], phi_nodes[k], weights)
        alphas[j, k] = num / den

    # Wyliczanie wartości phi_j w węzłach
    phi_nodes[j] = x_j.copy()
    for k in range(j):
        phi_nodes[j] -= alphas[j, k] * phi_nodes[k]

# Wyznaczanie współczynników aproksymacji a_j
norms = np.zeros(n + 1)  # <phi_j, phi_j>
f_phi = np.zeros(n + 1)  # <f, phi_j>
a_coeffs = np.zeros(n + 1)  # a_j

for j in range(n + 1):
    norms[j] = inner_product(phi_nodes[j], phi_nodes[j], weights)
    f_phi[j] = inner_product(y_values, phi_nodes[j], weights)
    a_coeffs[j] = f_phi[j] / norms[j]


print("--- APROKSYMACJA W BAZIE WIELOMIANÓW ORTOGONALNYCH ---\n")
print(f"Liczba węzłów: {num_nodes}")
print(f"Stopień wielomianu (n): {n}\n")

print("Iloczyny skalarne:")
for j in range(n + 1):
    print(f" <phi_{j}, phi_{j}> = {norms[j]:.4f}")
    print(f" <f, phi_{j}>     = {f_phi[j]:.4f}")
print()

print("Weryfikacja ortogonalności (<phi_i, phi_j> dla i != j):")
for i in range(n + 1):
    for j in range(i + 1, n + 1):
        dot_val = inner_product(phi_nodes[i], phi_nodes[j], weights)
        print(f" <phi_{i}, phi_{j}> = {dot_val:.4e}")
print()

print("Współczynniki wielomianu aproksymującego:")
for j in range(n + 1):
    print(f" a_{j} = {a_coeffs[j]:.6f}")
print()

print("Tabela wartości w węzłach:")
print(f"{'x_i':>6} | {'y_i (zadane)':>15} | {'F(x_i) (obliczone)':>20}")
print("-" * 48)
error_E = 0.0
# Ewaluacja dla każdego węzła
F_nodes = evaluate_F(x_nodes, a_coeffs, alphas)

for i in range(num_nodes):
    print(f"{x_nodes[i]:6.1f} | {y_values[i]:15.1f} | {F_nodes[i]:20.4f}")
    error_E += weights[i] * ((y_values[i] - F_nodes[i]) ** 2)
print("-" * 48)

print(f"\nWartość funkcjonału błędu E: {error_E:.4f}")

print("\nTesty punktów spoza węzłów:")
test_points = np.array([0.0, 4.5, 9.0])
F_test = evaluate_F(test_points, a_coeffs, alphas)
for i in range(len(test_points)):
    print(f" F({test_points[i]:.1f}) = {F_test[i]:.4f}")

# PORÓWNANIE DO POPRZEDNIEGO ĆWICZENIA
print("\n--- PORÓWNANIE DO BAZY JEDNOMIANÓW ---")
print("Ostateczny wielomian aproksymujący jest zbudowany z wyznaczonych funkcji bazowych (phi):")
print(f" F(x) = {a_coeffs[0]:.4f} * phi_0(x) + {a_coeffs[1]:.4f} * phi_1(x)")
print("Wspolczynniki z poprzedniego zadania = (0.1071, 1.3929)")

