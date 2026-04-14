import numpy as np
import os


def wczytaj_dane(nazwa_pliku):
    """Pomocnicza funkcja do wczytywania macierzy z pliku"""
    if not os.path.exists(nazwa_pliku):
        print(f"Brak pliku: {nazwa_pliku}")
        return None
    try:
        with open(nazwa_pliku, 'r') as file:
            lines = file.readlines()
            n = int(lines[0].strip())
            macierz = []
            for line in lines[1:n + 1]:
                macierz.append([float(x) for x in line.split()])
            return np.array(macierz)
    except Exception as e:
        print(f"Błąd podczas odczytu pliku {nazwa_pliku}: {e}")
        return None


def gauss(Ab_input):
    """Oryginalna metoda eliminacji Gaussa (potrzebna do Zadania 3)."""
    Ab = np.copy(Ab_input).astype(float)
    n = Ab.shape[0]

    for i in range(n):
        if np.isclose(Ab[i, i], 0.0):
            print(f"  [BŁĄD] Wystąpiło 0 na przekątnej w wierszu {i}.")
            return None

        for j in range(i + 1, n):
            m = Ab[j, i] / Ab[i, i]
            Ab[j] = Ab[j] - m * Ab[i]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if np.isclose(Ab[i, i], 0.0):
            return None
        suma = sum(Ab[i, k] * x[k] for k in range(i + 1, n))
        x[i] = (Ab[i, -1] - suma) / Ab[i, i]

    return x


def gauss_wybor_wiersza(Ab_input):
    """Zadanie 1: Eliminacja Gaussa z częściowym wyborem elementu głównego (wiersze)."""
    Ab = np.copy(Ab_input).astype(float)
    n = Ab.shape[0]

    print("\nMacierz rozszerzona (przed obliczeniami):")
    print(Ab)

    # Postępowanie proste z wyborem wiersza
    for i in range(n):
        #Szukamy w kolumnie (od wiersza i w dół) elementu o największej wartości bezwzględnej
        max_row_index = np.argmax(np.abs(Ab[i:n, i])) + i

        # Zamiana wierszy (jeśli największy element nie jest na obecnej przekątnej)
        if max_row_index != i:
            Ab[[i, max_row_index]] = Ab[[max_row_index, i]]

        # Sprawdzenie po zamianie
        if np.isclose(Ab[i, i], 0.0):
            print("Układ jest osobliwy (brak jednoznacznego rozwiązania).")
            return None

        # Zwykła eliminacja (zerowanie elementów pod pivotem)
        for j in range(i + 1, n):
            m = Ab[j, i] / Ab[i, i]
            Ab[j] = Ab[j] - m * Ab[i]

    print("\nMacierz rozszerzona (po postępowaniu prostym):")
    print(np.round(Ab, 4))

    # Postępowanie odwrotne (podstawienie wstecz)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = sum(Ab[i, k] * x[k] for k in range(i + 1, n))
        x[i] = (Ab[i, -1] - suma) / Ab[i, i]

    print("\nRozwiązanie układu równań (x_0 - x_n):")
    for i in range(n):
        print(f"x_{i} = {x[i]:.4f}")

    return x


def gauss_crout(Ab_input):
    """Eliminacja Gaussa-Crouta ze zmianą po kolumnach."""
    Ab = np.copy(Ab_input).astype(float)
    n = Ab.shape[0]

    # Wektor przechowujący informację o numerach kolumn (x_0, x_1, ... x_n)
    kolumny = list(range(n))

    print("\nMacierz rozszerzona (przed obliczeniami):")
    print(Ab)

    # Postępowanie proste z wyborem kolumny
    for i in range(n):
        # Szukamy w obecnym wierszu (od kolumny i w prawo, pomijając kolumnę wyrazów wolnych)
        # elementu o największym module
        max_col_index = np.argmax(np.abs(Ab[i, i:n])) + i

        # Zamiana kolumn i aktualizacja wektora numerów kolumn
        if max_col_index != i:
            # Zamieniamy całe kolumny macierzy
            Ab[:, [i, max_col_index]] = Ab[:, [max_col_index, i]]
            # Zapisujemy zmianę w wektorze
            kolumny[i], kolumny[max_col_index] = kolumny[max_col_index], kolumny[i]

        if np.isclose(Ab[i, i], 0.0):
            print("Układ jest osobliwy (brak jednoznacznego rozwiązania).")
            return None

        # Zwykła eliminacja
        for j in range(i + 1, n):
            m = Ab[j, i] / Ab[i, i]
            Ab[j] = Ab[j] - m * Ab[i]

    print("\nMacierz rozszerzona (po postępowaniu prostym):")
    print(np.round(Ab, 4))

    print("\nWektor przechowujący informację o numerach kolumn:")
    print(kolumny)

    # Postępowanie odwrotne (podstawienie wstecz)
    x_obliczone = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = sum(Ab[i, k] * x_obliczone[k] for k in range(i + 1, n))
        x_obliczone[i] = (Ab[i, -1] - suma) / Ab[i, i]

    # Rekonstrukcja poprawnej kolejności wyników na podstawie wektora `kolumny`
    x_prawdziwe = np.zeros(n)
    for i in range(n):
        x_prawdziwe[kolumny[i]] = x_obliczone[i]

    print("\nRozwiązanie układu równań (x_0 - x_n):")
    for i in range(n):
        print(f"x_{i} = {x_prawdziwe[i]:.4f}")

    return x_prawdziwe


def zadanie_3():
    print("")
    print("---ZADANIE 3---")
    print("")

    # Przykład z zerem na przekątnej w trakcie eliminacji
    print("\n--- PRZYKŁAD A: Zero na przekątnej ---")
    Ab_zero = np.array([
        [0, 2, 4],
        [3, 1, 5]
    ], dtype=float)

    print("Zwykły Gauss:")
    wynik = gauss(Ab_zero)
    if wynik is not None: print(wynik)

    print("\nGauss z pivotingiem:")
    gauss_wybor_wiersza(Ab_zero)

    # Przykład z bardzo małym elementem
    print("\n--- PRZYKŁAD B: Bardzo mały element na przekątnej ---")
    eps = 1e-15
    Ab_male = np.array([
        [eps, 1, 1],
        [1, 1, 2]
    ], dtype=float)

    print("Zwykły Gauss:")
    wynik_bez = gauss(Ab_male)
    if wynik_bez is not None:
        print(f"Rozwiązanie z utratą precyzji: {np.round(wynik_bez, 4)}")

    print("\nGauss z pivotingiem (wybór wiersza):")
    wynik_z = gauss_wybor_wiersza(Ab_male)


if __name__ == "__main__":

    # print("ZADANIE 1")
    # Ab_zad1 = wczytaj_dane("RURL_dane3.txt")
    # if Ab_zad1 is not None:
    #     gauss_wybor_wiersza(Ab_zad1)

    # print("\n ZADANIE 2 ")
    # Ab_zad2 = wczytaj_dane("RURL_dane3.txt")
    # if Ab_zad2 is not None:
    #     gauss_crout(Ab_zad2)

    zadanie_3()