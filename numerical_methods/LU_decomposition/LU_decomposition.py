

def calc_lu(nazwa_pliku):

    # Pobieranie danych z pliku
    try:
        with open(nazwa_pliku, 'r') as f:
            linie = f.readlines()
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {nazwa_pliku}.")
        return

    A = []
    B = []

    # Parsowanie wierszy
    for linia in linie:
        elementy = list(map(float, linia.split()))
        A.append(elementy[:-1])
        B.append(elementy[-1])

    n = len(A)

    # Wypisanie macierzy rozszerzonej przed obliczeniami
    print("--- Macierz rozszerzona [A | B] ---")
    for i in range(n):
        wiersz_str = "  ".join(f"{A[i][j]:5.2f}" for j in range(n))
        print(f"[{wiersz_str}  | {B[i]:6.2f} ]")
    print("\n")

    # Utworzenie i wyzerowanie macierzy L i U
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    # W macierzy L elementom na głównej przekątnej przypisujemy 1
    for i in range(n):
        L[i][i] = 1.0

    # Obliczanie rozkładu LU
    for i in range(n):
        # Obliczanie elementów macierzy U (dla j >= i)
        for j in range(i, n):
            suma_u = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - suma_u

        # Sprawdzenie, czy na przekątnej macierzy U nie pojawiło się zero
        if U[i][i] == 0:
            print(f"Wystąpiło 0 na przekątnej macierzy U (u_{i},{i}).")
            return

        # Obliczanie elementów macierzy L (dla j > i)
        for j in range(i + 1, n):
            suma_l = sum(L[j][k] * U[k][i] for k in range(i))
            L[j][i] = (A[j][i] - suma_l) / U[i][i]

    # Wypisywanie macierzy L i U
    print("--- Macierz L ---")
    for wiersz in L:
        print("  ".join(f"{val:6.2f}" for val in wiersz))
    print("\n")

    print("--- Macierz U ---")
    for wiersz in U:
        print("  ".join(f"{val:6.2f}" for val in wiersz))
    print("\n")

    # Obliczanie wektora Y (L * Y = B)
    Y = [0.0] * n
    for i in range(n):
        suma_y = sum(L[i][j] * Y[j] for j in range(i))
        Y[i] = B[i] - suma_y

    print("--- Wektor Y ---")
    for i, val in enumerate(Y):
        print(f"y_{i} = {val:6.2f}")
    print("\n")

    # Obliczanie wektora X (U * X = Y)
    X = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma_x = sum(U[i][j] * X[j] for j in range(i + 1, n))
        X[i] = (Y[i] - suma_x) / U[i][i]

    print("--- Rozwiązanie układu równań (Wektor X) ---")
    for i, val in enumerate(X):
        print(f"x_{i} = {val:6.2f}")


calc_lu('RURL_dane3.txt')