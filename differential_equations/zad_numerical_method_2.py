import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# 1. PARAMETRY I ROZWIĄZANIE DOKŁADNE

def get_exact_constants():

    exp10 = np.exp(10)
    C2 = -0.2 / (4 + exp10)
    C1 = 4 * C2 + 0.4
    return C1, C2


C1, C2 = get_exact_constants()


def exact_solution(x):
    return C1 + C2 * np.exp(5 * x) + 0.4 * x


# Parametry zadania
a, b = 0.0, 2.0
epsilon = 1e-5
report_points_count = 11
report_x = np.linspace(a, b, report_points_count)


# 2. METODA RÓŻNIC SKOŃCZONYCH (MRS)

def solve_fdm(N):
    h = (b - a) / N
    x = np.linspace(a, b, N + 1)

    # Macierz systemu A * y = rhs
    A = np.zeros((N + 1, N + 1))
    rhs = np.zeros(N + 1)

    # 1. Warunek brzegowy LEWY (x=0, i=0): y(0) - y'(0) = 0
    A[0, 0] = 2 * h + 3
    A[0, 1] = -4
    A[0, 2] = 1
    rhs[0] = 0

    # 2. Węzły WEWNĘTRZNE (i=1...N-1)
    coeff_minus = 1 + 2.5 * h
    coeff_diag = -2.0
    coeff_plus = 1 - 2.5 * h
    rhs_val = -2 * h ** 2

    for i in range(1, N):
        A[i, i - 1] = coeff_minus
        A[i, i] = coeff_diag
        A[i, i + 1] = coeff_plus
        rhs[i] = rhs_val

    # 3. Warunek brzegowy PRAWY (x=2, i=N): y(2) = 1
    A[N, N] = 1.0
    rhs[N] = 1.0

    # Rozwiązanie układu
    y = np.linalg.solve(A, rhs)
    return x, y


# 3. PĘTLA ADAPTACYJNA


def adaptive_solver():
    N = 10  # Startowa liczba podprzedziałów
    print(f"Kryterium błędu: {epsilon}")

    # Inicjalizacja "poprzednich" wyników (dla N=10)
    x_prev, y_prev = solve_fdm(N)

    y_report_prev = y_prev[::(N // 10)]

    iteration = 0
    while True:
        iteration += 1
        N_new = 2 * N  # Zagęszczanie siatki x2

        x_new, y_new = solve_fdm(N_new)

        step_factor = N_new // 10
        y_report_new = y_new[::step_factor]

        # Obliczenie różnicy (błąd między iteracjami)
        delta = np.max(np.abs(y_report_new - y_report_prev))

        print(f"Iteracja {iteration}: N={N_new}, delta={delta:.2e}")

        if delta < epsilon:
            print(f"-> Zbieżność osiągnięta dla N={N_new}")
            return x_new, y_new, y_report_new, N_new

        # Aktualizacja do następnego kroku
        N = N_new
        y_report_prev = y_report_new

        if N > 100000:
            print("Przekroczono limit węzłów!")
            break


# 4. PREZENTACJA WYNIKÓW

x_final, y_final, y_report_final, N_final = adaptive_solver()
y_exact_report = exact_solution(report_x)
errors = np.abs(y_report_final - y_exact_report)

# Tabela
df = pd.DataFrame({
    'x_j': report_x,
    'y_num': y_report_final,
    'y_dokł': y_exact_report,
    '|Błąd|': errors
})

print("\n=== Tabela wyników końcowych ===")
print(df.to_string(index=False, float_format=lambda x: "{:.6f}".format(x)))

# Wykres
plt.figure(figsize=(10, 6))
x_plot = np.linspace(a, b, 200)
plt.plot(x_plot, exact_solution(x_plot), 'k-', linewidth=1.5, label='Rozwiązanie dokładne')
plt.plot(x_final[::(N_final // 20)], y_final[::(N_final // 20)], 'r--', label=f'MRS (N={N_final})')
plt.plot(report_x, y_report_final, 'bo', label='Punkty kontrolne')

plt.title(f"Rozwiązanie zadania 1 (Zadanie numeryczne 2)\nN={N_final}, epsilon={epsilon}")
plt.xlabel("x")
plt.ylabel("y(x)")
plt.legend()
plt.grid(True)
plt.show()