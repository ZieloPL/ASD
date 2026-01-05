import sympy as sp

# 1. DEFINICJA ZMIENNYCH I MACIERZY
t = sp.symbols('t')
C1, C2, C3 = sp.symbols('C1 C2 C3')

# Macierz układu A (z Zadania 1)
A = sp.Matrix([
    [2, -1, -1],
    [1, 0, -1],
    [1, -1, 0]
])

# Wektor wymuszenia F(t) (z Zadania 1)
F = sp.Matrix([
    [sp.exp(t)],
    [0],
    [sp.exp(-t)]
])

# 2. OBLICZENIA (Wartości własne, wektory, P, D)
eigen_info = A.eigenvects()
P, D = A.diagonalize()


exp_Dt = sp.exp(D * t) # Ponieważ D jest diagonalna, e^Dt to exp na przekątnej
exp_At = P * exp_Dt * P.inv()

# 4. ROZWIĄZANIE OGÓLNE UKŁADU NIEJEDNORODNEGO


# Rozwiązanie jednorodne (X_h)
C_vec = sp.Matrix([C1, C2, C3])
X_h = exp_At * C_vec

# Rozwiązanie szczególne (X_p)
inv_exp_At = P * sp.exp(D * -t) * P.inv() # e^(-At)
integrand = inv_exp_At * F
integral_result = sp.integrate(integrand, t)
X_p = exp_At * integral_result

# Rozwiązanie całkowite
X_sol = X_h + X_p
X_sol_simplified = sp.simplify(X_sol)


# WYPISYWANIE WYNIKÓW

print("=== 1. WARTOŚCI WŁASNE I WEKTORY WŁASNE ===")
for val, mult, vec in eigen_info:
    print(f"Wartość własna: {val}, Krotność: {mult}")
    print("Wektor własny:")
    sp.pprint(vec)

print("\n=== 2. MACIERZ P (Wektory własne) I D (Diagonalna) ===")
sp.pprint(P)
print("\nMacierz D:")
sp.pprint(D)

print("\n=== 3. MACIERZ e^(At) ===")
# Wyświetlamy w uproszczonej formie
sp.pprint(sp.simplify(exp_At))

print("\n=== 4. ROZWIĄZANIE KOŃCOWE X(t) ===")
# Rozbijamy na x1(t), x2(t), x3(t) dla czytelności
rows = ["x1(t)", "x2(t)", "x3(t)"]
for i in range(3):
    print(f"\n{rows[i]} =")
    sp.pprint(X_sol_simplified[i])




X_numeric = X_sol_simplified.subs({C1: 1, C2: 1, C3: 1})
f1 = sp.lambdify(t, X_numeric[0], 'numpy')
f2 = sp.lambdify(t, X_numeric[1], 'numpy')
f3 = sp.lambdify(t, X_numeric[2], 'numpy')

import numpy as np
import matplotlib.pyplot as plt

t_vals = np.linspace(0, 3, 100)
plt.figure(figsize=(10, 6))
plt.plot(t_vals, f1(t_vals), label='x1(t)')
plt.plot(t_vals, f2(t_vals), label='x2(t)')
plt.plot(t_vals, f3(t_vals), label='x3(t)')
plt.title("Przykładowe rozwiązanie (dla C1=C2=C3=1)")
plt.xlabel("Czas t")
plt.ylabel("Wartość")
plt.legend()
plt.grid(True)
plt.show()