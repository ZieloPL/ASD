import numpy as np
import os


def rozwiaz_gauss(nazwa_pliku):
    # Pobierane danych
    if not os.path.exists(nazwa_pliku):
        print(f"Nie znaleziono pliku: {nazwa_pliku}")
        return

    try:
        with open(nazwa_pliku, 'r') as file:
            lines = file.readlines()
            # Wczytanie wymiaru macierzy
            n = int(lines[0].strip())

            # Wczytanie reszty wierszy
            macierz = []
            for line in lines[1:n + 1]:
                macierz.append([float(x) for x in line.split()])

            Ab = np.array(macierz)
    except Exception as e:
        print(f"Błąd podczas odczytu pliku {nazwa_pliku}: {e}")
        return

    # Wypisywanie macierzy przed obliczeniami
    print("\nMacierz rozszerzona (przed obliczeniami):")
    print(Ab)

    # Postępowanie proste
    for i in range(n):
        # Sprawdzenie czy na przekątnej nie ma zera
        if np.isclose(Ab[i, i], 0.0):
            print(f"\nWystąpiło 0 na przekątnej w wierszu {i}!")
            return

        # Zerowanie elementów pod przekatna
        for j in range(i + 1, n):
            m = Ab[j, i] / Ab[i, i]
            Ab[j] = Ab[j] - m * Ab[i]

    # Wypisywanie macierzy po postepowaniu prostym
    print("\nMacierz rozszerzona po postępowanie proste:")
    print(np.round(Ab, 4))

    # Postępowanie odwrotne (podstawienie wstecz)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if np.isclose(Ab[i, i], 0.0):
            print(f"\nWystąpiło 0 na przekatnej podczas podstawiania wstecz w wierszu {i}")
            return
        # Obliczanie sumy
        suma = sum(Ab[i, k] * x[k] for k in range(i + 1, n))
        x[i] = (Ab[i, -1] - suma) / Ab[i, i]

    # Wypisywanie ostatecznego rozwiązania
    print("\nRozwiązanie ukladu równań (x_0 - x_n):")
    for i in range(n):
        print(f"x_{i} = {x[i]:.3f}")


if __name__ == "__main__":
    plik = "RURL_dane1.txt"
    rozwiaz_gauss(plik)