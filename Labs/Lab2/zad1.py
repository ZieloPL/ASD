# Napisz funkcję, która wczyta dane z pliku i utworzy listę obiektów reprezentujących prezydentów.
# Każdy węzeł listy powinien zawierać pełny zestaw informacji.

def wczytaj_prezydentow(nazwa_pliku):
    prezydenci = []
    with open(nazwa_pliku, "r", encoding="utf-8") as plik:
        for linia in plik:
            linia = linia.strip()
            if not linia:
                continue

            dane = linia.split()

            for i, element in enumerate(dane):
                if "-" in element:  # zakres lat
                    start, end = element.split("-")
                    imie_nazwisko = " ".join(dane[:i])
                    partia = " ".join(dane[i+1:])
                    prezydent = [imie_nazwisko, int(start), int(end), partia]
                    prezydenci.append(prezydent)
                    break
    return prezydenci


lista_prezydentow = wczytaj_prezydentow("presidents.txt")
for p in lista_prezydentow:
    print(p)
