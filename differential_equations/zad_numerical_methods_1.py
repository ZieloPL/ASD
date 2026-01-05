import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# 1. DEFINICJA PROBLEMU I ROZWIĄZANIA DOKŁADNEGO

def f(t, y):
    """Prawa strona równania y' = f(t,y)"""
    return t * np.exp(-t) - y


def exact_solution(t):
    """Rozwiązanie analityczne: y(t) = e^(-t) * (0.5*t^2 + 1)"""
    return np.exp(-t) * (0.5 * t ** 2 + 1)


# Parametry zadania
t_start, t_end = 0.0, 2.0
y0 = 1.0
epsilon = 1e-5  # Kryterium dokładności
report_points_count = 11  # 10 odcinków = 11 punktów (od 0 do 10)

#
report_times = np.linspace(t_start, t_end, report_points_count)


# 2. IMPLEMENTACJA METOD NUMERYCZNYCH (Krok pojedynczy)


def step_euler(t, y, h):
    return y + h * f(t, y)


def step_midpoint(t, y, h):
    k1 = f(t, y)
    return y + h * f(t + 0.5 * h, y + 0.5 * h * k1)


def step_rk4(t, y, h):
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = f(t + h, y + h * k3)
    return y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def step_taylor3(t, y, h):

    yp = t * np.exp(-t) - y
    ypp = np.exp(-t) * (1 - t) - yp
    yppp = np.exp(-t) * (t - 2) - ypp

    return y + h * yp + (h ** 2 / 2) * ypp + (h ** 3 / 6) * yppp


# 3. ALGORYTM ADAPTACYJNY


def solve_adaptive(method_step_func, method_name):
    N = 10  # Początkowa liczba podziałów
    h = (t_end - t_start) / N

    prev_report_values = np.full(report_points_count, np.inf)

    iteration = 0

    print(f"\n--- Metoda {method_name} ---")

    while True:
        iteration += 1
        t_values = np.linspace(t_start, t_end, N + 1)
        y_values = np.zeros(N + 1)
        y_values[0] = y0


        for i in range(N):
            y_values[i + 1] = method_step_func(t_values[i], y_values[i], h)


        step_factor = N // (report_points_count - 1)
        current_report_values = y_values[::step_factor]

        delta = np.max(np.abs(current_report_values - prev_report_values))

        if delta < epsilon and iteration > 1:
            print(f"-> Zbieżność osiągnięta po {iteration} iteracjach (h={h:.6f}).")
            return current_report_values, h, N

        prev_report_values = current_report_values
        N *= 2
        h /= 2

        if N > 1000000:  # Zabezpieczenie przed pętlą nieskończoną
            print("! Przekroczono limit iteracji !")
            return current_report_values, h, N


# 4. URUCHOMIENIE I PREZENTACJA WYNIKÓW

methods = [
    (step_euler, "Eulera"),
    (step_midpoint, "Punktu Środkowego"),
    (step_rk4, "Rungego-Kutty 4"),
    (step_taylor3, "Taylora rzędu 3")
]

results = {}

for step_func, name in methods:
    y_num, final_h, final_N = solve_adaptive(step_func, name)

    # Obliczenie dokładnych wartości i błędów
    y_exact_vals = exact_solution(report_times)
    errors = np.abs(y_num - y_exact_vals)

    results[name] = y_num

    # Tworzenie tabeli
    df = pd.DataFrame({
        't_j': report_times,
        'y_num': y_num,
        'y_dokł': y_exact_vals,
        '|Błąd|': errors
    })

    print(f"\nTabela wyników dla metody {name}:")
    print(df.to_string(index=False, float_format=lambda x: "{:.6f}".format(x)))

# 5. WYKRES

plt.figure(figsize=(10, 6))
t_plot = np.linspace(t_start, t_end, 200)
plt.plot(t_plot, exact_solution(t_plot), 'k-', linewidth=2, label='Rozwiązanie dokładne')

markers = ['o', 's', '^', 'x']
colors = ['red', 'green', 'blue', 'orange']

for i, (method_func, name) in enumerate(methods):
    # Rysujemy punkty raportowe dla każdej metody
    plt.plot(report_times, results[name], marker=markers[i], linestyle='--',
             color=colors[i], label=f'Metoda {name}', markersize=6)

plt.title(f"Porównanie metod numerycznych (Zadanie 1, epsilon={epsilon})")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.grid(True)
plt.legend()
plt.show()