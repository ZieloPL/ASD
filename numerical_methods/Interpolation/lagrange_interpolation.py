''' Węzły interpolacji i wartości funkcji w węzłach oraz liczba węzłów są zmiennymi
pobieranymi z pliku tekstowego.
b) Punkt, w którym obliczamy wartość wielomianu jest parametrem podawanym
z klawiatury przez użytkownika.
c) W wyniku działania program wypisuje:
• Liczbę węzłów
• Dane: węzły interpolacji i wartości funkcji w węzłach
• Punkt, w którym liczymy wartość wielomianu
• Wartość wielomianu Lagrange’a w danym punkcie '''

import pandas

#wczytanie danych
path = 'plik.csv'
table = pandas.read_csv(path)

# Pobranie węzłów
x_nodes = table['x'].tolist()
y_nodes = table['y'].tolist()
amount_of_nodes = len(x_nodes)

point_to_calc = float(input('Podaj punkt do policzenia: '))

lagrange_result = 0.0  #wynik

for j in range(amount_of_nodes):

    l_j = 1.0 #do przechowania wartosci wielomianu

    # Liczenie ułamkow i ich mnożenie
    for m in range(amount_of_nodes):
        if m != j:
            licznik = point_to_calc - x_nodes[m]
            mianownik = x_nodes[j] - x_nodes[m]
            l_j = l_j * (licznik / mianownik)

    lagrange_result = lagrange_result + (y_nodes[j] * l_j)

print(f"Liczba węzłów: {amount_of_nodes}")
print("Dane węzły interpolacji i wartości funkcij:")

for i in range(amount_of_nodes):
    print(f"Punkt {i}: x = {x_nodes[i]}, f(x) = {y_nodes[i]}")

print(f"Punkt podany od użytkownika: {point_to_calc}")
print(f"Wartość wielomianu w danym punkcie wynosi: {lagrange_result}")