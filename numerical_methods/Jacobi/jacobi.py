import time
import random


def wczytaj_dane(nazwa_pliku):
    A = []
    b = []
    with open(nazwa_pliku, 'r') as f:
        for linia in f:
            dane = list(map(float, linia.strip().split()))
            A.append(dane[:-1])
            b.append(dane[-1])
    return A, b


def wypisz_macierz_rozszerzona(A, b):
    n = len(A)
    print("Macierz rozszerzona [A | b]:")
    for i in range(n):
        wiersz = "  ".join(f"{A[i][j]:6.4f}" for j in range(n))
        print(f"{wiersz}  |  {b[i]:6.4f}")
    print()


def sprawdz_dominacje(A):
    n = len(A)
    slaba_dominacja = True
    ostra_dominacja = False

    for i in range(n):
        diag = abs(A[i][i])
        suma_poza_diag = sum(abs(A[i][j]) for j in range(n) if j != i)

        if diag < suma_poza_diag:
            slaba_dominacja = False
        if diag > suma_poza_diag:
            ostra_dominacja = True

    if slaba_dominacja and ostra_dominacja:
        print(
            "Macierz jest diagonalnie słabo dominująca i posiada dominację ostrą w co najmniej 1 wierszu. (Zbieżność gwarantowana)")
    elif slaba_dominacja:
        print("Macierz jest tylko słabo dominująca (brak dominacji ostrej). (Zbieżność mozliwa)")
    else:
        print("Macierz nie jest diagonalnie słabo dominująca. (Metoda może być rozbieżna)")
    print()


def jacobi(A, b, epsilon, max_iter=1000, wypisz_info=True):
    n = len(A)
    x = [0.0] * n
    x_new = [0.0] * n
    bledy = [0.0] * n

    for k in range(max_iter):
        max_blad = 0.0
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]

            blad = abs(x_new[i] - x[i])
            bledy[i] = blad
            if blad > max_blad:
                max_blad = blad

        x = x_new[:]

        if max_blad < epsilon:
            if wypisz_info:
                print_jacobi(epsilon, k + 1, x, bledy)
            return x, k + 1

    if wypisz_info:
        print(f"Osiągnięto limit iteracji ({max_iter}) dla epsilon={epsilon}.")
    return x, max_iter


def print_jacobi(epsilon, iteracje, x, bledy):
    print(f"--- Wyniki dla epsilon = {epsilon} ---")
    print(f"Liczba wykonanych iteracji: {iteracje}")
    for i in range(len(x)):
        print(f"x[{i}] = {x[i]:10.6f} | błąd = {bledy[i]:.6e}")
    print()


# Zadanie 2: Porównanie z metodą Gaussa

def gauss(A, b):
    n = len(A)
    M = [wiersz[:] for wiersz in A]
    v = b[:]

    # Eliminacja w przód
    for i in range(n):
        for j in range(i + 1, n):
            wspolczynnik = M[j][i] / M[i][i]
            for k in range(i, n):
                M[j][k] -= wspolczynnik * M[i][k]
            v[j] -= wspolczynnik * v[i]

    # Podstawianie wstecz
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (v[i] - suma) / M[i][i]
    return x


def generuj_macierz_dominujaca(n):
    A = [[random.uniform(-10, 10) for _ in range(n)] for _ in range(n)]
    b = [random.uniform(-50, 50) for _ in range(n)]

    # Wymuszamy dominację na przekątnej
    for i in range(n):
        suma_poza = sum(abs(A[i][j]) for j in range(n) if j != i)
        # Dodajemy losową wartość, aby zapewnić ostrą dominację
        A[i][i] = suma_poza + random.uniform(1, 10)
        if random.choice([True, False]):
            A[i][i] *= -1  # Losowość znaków

    return A, b


def porownaj_metody(lista_n):
    print("--- Zadanie 2: Gauss vs Jacobi ---")

    for n in lista_n:
        A, b = generuj_macierz_dominujaca(n)

        # Test Gaussa
        start_g = time.perf_counter()
        x_gauss = gauss(A, b)
        czas_g = time.perf_counter() - start_g

        # Test Jacobiego
        start_j = time.perf_counter()
        x_jacobi, iter_j = jacobi(A, b, epsilon=1e-6, wypisz_info=False)
        czas_j = time.perf_counter() - start_j

        # Obliczanie błędu między metodami
        blad_wzgledny = max(abs(x_gauss[i] - x_jacobi[i]) for i in range(n))

        print(f"Rozmiar układu n = {n}:")
        print(f"  Czas Gauss   : {czas_g:.6f} s")
        print(f"  Czas Jacobi  : {czas_j:.6f} s (iteracji: {iter_j})")
        print(f"  Różnica wyników (max błąd): {blad_wzgledny:.2e}")
        print("-" * 40)


if __name__ == "__main__":
    print("Zadanie 1: ")

    try:
        A_zad1, b_zad1 = wczytaj_dane('dane.txt')
        wypisz_macierz_rozszerzona(A_zad1, b_zad1)
        sprawdz_dominacje(A_zad1)

        # Uruchomienie dla epsilon = 0.001
        jacobi(A_zad1, b_zad1, epsilon=0.001)

        # Uruchomienie dla epsilon = 0.000001
        jacobi(A_zad1, b_zad1, epsilon=0.000001)

    except FileNotFoundError:
        print("Nie znaleziono pliku z danymi")

    # Wywołanie dla różnych wartości n
    porownaj_metody([10, 50, 100, 250, 500])