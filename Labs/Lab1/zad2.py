# Dana jest prostokątna plansza o wymiarach N x M. Na planszy rozmieszczono pionki w k
# kolorach. Napisz funkcję NajSąsiadów, która znajdzie kolor, dla którego pionki mają najwięcej
# sąsiadów tego samego koloru. Podaj specyfikację wejścia-wyjścia. Narysuj schemat blokowy
# funkcji.

# Ja przyjalem ze kazdy pionek to jest inny przypadek do rozpatrzenia, czyli
# pionek [i][j] jest sasiadem dla [i][j+1} i vice versa



def NajSasiadow(tab):

    count_x = len(tab)
    count_y = len(tab[0])
    colours = {}

    for i in range(count_x):
        for j in range(count_y):
           try:
               if tab[i][j] == tab[i][j-1]:
                   colours[tab[i][j]] = colours.get(tab[i][j], 0) + 1
           except:
               pass
           try:
               if tab[i][j] == tab[i][j+1]:
                   colours[tab[i][j]] = colours.get(tab[i][j], 0) + 1
           except:
               pass

    max_colour = max(colours, key=colours.get)
    return max_colour



plansza = [
    ['czarny', 'czarny', 'czarny', 'czerwony','zielony'],
    ['zielony', 'czerwony', 'czerwony', 'zielony','zielony'],
    ['zolty', 'niebieski', 'czarny', 'czerwony','zielony'],
    ['zolty', 'zolty', 'czarny', 'zielony','zielony'],
    ['czerwony', 'czerwony', 'czerwony', 'czerwony','niebieski'],
    ['pomaranczowy', 'fioletowy', 'fioletowy', 'zolty','zolty'],
]

print(NajSasiadow(plansza))