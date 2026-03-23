import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Zad 1
def oblicz_ilorazy_roznicowe(x, y):
    n = len(x)
    b = list(y)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            b[i] = (b[i] - b[i - 1]) / (x[i] - x[i - j])
    return b


def wartosc_wielomianu(wezly_x, b_k, punkt_x):
    n = len(b_k)
    wynik = b_k[0]
    p_k = 1.0
    for k in range(1, n):
        p_k *= (punkt_x - wezly_x[k - 1])
        wynik += b_k[k] * p_k
    return wynik


def zadanie_1():
    print("Zadanie 1:\n")
    plik = "newton.csv"

    if not os.path.exists(plik):
        print(f"Błąd: Nie znaleziono pliku {plik}")
        return

    # a) Pobieranie węzłów i wartości z pliku
    df = pd.read_csv(plik)
    wezly_x = df['x'].tolist()
    wartosci_y = df['y'].tolist()
    liczba_wezlow = len(df)

    # b) Pobieranie punktu
    try:
        punkt = float(input("Podaj punkt x, w którym chcesz obliczyć wartość wielomianu: "))
    except ValueError:
        print("Błąd: Podano nieprawidłową wartość.")
        return

    # Obliczenia
    wspolczynniki_bk = oblicz_ilorazy_roznicowe(wezly_x, wartosci_y)
    wynik = wartosc_wielomianu(wezly_x, wspolczynniki_bk, punkt)

    # c) Wypisywanie wyników
    print("\nZadanie 1\n")
    print(f"Liczba węzłów: {liczba_wezlow}")
    print("Dane (węzły i wartości funkcji):")
    for i in range(liczba_wezlow):
        print(f"  x[{i}] = {wezly_x[i]}, f(x[{i}]) = {wartosci_y[i]}")

    print(f"\nPunkt obliczeniowy x: {punkt}")
    print(f"Współczynniki wielomianu Newtona (b_k): {[round(b, 4) for b in wspolczynniki_bk]}")
    print(f"Wartość wielomianu (y) Newtona w punkcie {punkt}: {wynik}\n")


# Zad 2
def funkcja_rungego(x):
    return 1 / (1 + 25 * x ** 2)


def oscylacje():
    print("Zadanie 2")
    x_dokladne = np.linspace(-1, 1, 500)
    y_dokladne = funkcja_rungego(x_dokladne)

    plt.figure(figsize=(10, 6))
    plt.plot(x_dokladne, y_dokladne, label="Funkcja oryginalna (Rungego)", linewidth=2, color='black')

    #
    for n in [5, 11, 15]:
        wezly_x = np.linspace(-1, 1, n)
        wartosci_y = funkcja_rungego(wezly_x)

        wspolczynniki = oblicz_ilorazy_roznicowe(wezly_x, wartosci_y)
        y_interpolowane = [wartosc_wielomianu(wezly_x, wspolczynniki, x) for x in x_dokladne]

        plt.plot(x_dokladne, y_interpolowane, '--', label=f"Interpolacja Newtona (n={n})")
        plt.scatter(wezly_x, wartosci_y, color='red', zorder=5)  # Punkty węzłowe

    plt.title("Zadanie 2")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.ylim(-1, 2)
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    #zadanie_1()
    oscylacje()