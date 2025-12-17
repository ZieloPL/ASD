from collections import deque
import heapq


class Wierzcholek:
    def __init__(self, wartosc):
        self.wartosc = wartosc
        self.sasiedzi = []

        self.wagi = {}

    def dodaj_sasiada(self, sasiad, koszt=0):
        if sasiad not in self.sasiedzi:
            self.sasiedzi.append(sasiad)
        self.wagi[sasiad] = koszt

    def __lt__(self, other):
        return self.wartosc < other.wartosc

    def __repr__(self):
        return str(self.wartosc)


class UnionFind:
    def __init__(self, wierzcholki):
        self.parent = {w: w for w in wierzcholki}
        self.rank = {w: 0 for w in wierzcholki}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            return True
        return False


class Graf:
    def __init__(self):
        self.wierzcholki = {}
        self.lista_krawedzi = []

    def dodaj_wierzcholek(self, wartosc):
        if wartosc not in self.wierzcholki:
            nowy_wierzcholek = Wierzcholek(wartosc)
            self.wierzcholki[wartosc] = nowy_wierzcholek
        return self.wierzcholki[wartosc]

    def dodaj_krawedz(self, zrodlo, cel, koszt, skierowany=False):
        w_zrodlo = self.dodaj_wierzcholek(zrodlo)
        w_cel = self.dodaj_wierzcholek(cel)

        w_zrodlo.dodaj_sasiada(w_cel, koszt)

        if not skierowany:
            w_cel.dodaj_sasiada(w_zrodlo, koszt)

        self.lista_krawedzi.append((koszt, w_zrodlo, w_cel))

    def kruskal_mst(self):
        mst = []
        calkowity_koszt = 0

        posortowane = sorted(self.lista_krawedzi, key=lambda x: x[0])
        uf = UnionFind(self.wierzcholki.values())

        print("--- Przebieg algorytmu Kruskala ---")
        for koszt, u, v in posortowane:
            if uf.union(u, v):
                print(f"Dodano most: {u.wartosc}-{v.wartosc} (koszt: {koszt})")
                mst.append((u.wartosc, v.wartosc, koszt))
                calkowity_koszt += koszt
            else:
                print(f"Pominieto most: {u.wartosc}-{v.wartosc} (koszt: {koszt}) - utworzylby cykl")

        print(f"\nCalkowity koszt minimalnego drzewa (MST): {calkowity_koszt}")

    def bfs(self, start_wartosc):
        if start_wartosc not in self.wierzcholki: return
        start_node = self.wierzcholki[start_wartosc]
        odwiedzone = set([start_node])
        kolejka = deque([start_node])
        wynik = []
        while kolejka:
            obecny = kolejka.popleft()
            wynik.append(obecny.wartosc)
            for sasiad in obecny.sasiedzi:
                if sasiad not in odwiedzone:
                    odwiedzone.add(sasiad)
                    kolejka.append(sasiad)
        print(f"BFS: {wynik}")

    def dfs(self, start_wartosc):
        if start_wartosc not in self.wierzcholki: return
        start_node = self.wierzcholki[start_wartosc]
        odwiedzone = set()
        wynik = []
        def _dfs_rek(wezel):
            odwiedzone.add(wezel)
            wynik.append(wezel.wartosc)
            for sasiad in wezel.sasiedzi:
                if sasiad not in odwiedzone:
                    _dfs_rek(sasiad)
        _dfs_rek(start_node)
        print(f"DFS: {wynik}")

    def algorytm_prima(self, start_wartosc):
        if start_wartosc not in self.wierzcholki:
            print("Wierzcholek startowy nie istnieje.")
            return

        start_node = self.wierzcholki[start_wartosc]

        min_heap = [(0, start_node, start_node)]

        odwiedzone = set()
        mst_krawedzie = []
        calkowity_koszt = 0

        print(f"--- Algorytm Prima (Start: {start_wartosc}) ---")

        while min_heap:
            koszt, u, v = heapq.heappop(min_heap)

            if v in odwiedzone:
                continue

            odwiedzone.add(v)

            if u != v:
                calkowity_koszt += koszt
                mst_krawedzie.append((u.wartosc, v.wartosc, koszt))

            for sasiad in v.sasiedzi:
                if sasiad not in odwiedzone:
                    # Pobieramy wage z naszego slownika
                    waga = v.wagi[sasiad]
                    heapq.heappush(min_heap, (waga, v, sasiad))

        # Wypisanie wyniku
        print("Minimalne Drzewo Rozpinajace (MST) wg Prima:")
        for u, v, k in mst_krawedzie:
            print(f"Polaczenie: {u} - {v} (Koszt): {k})")
        print(f"Calkowity koszt budowy sieci: {calkowity_koszt}")


if __name__ == "__main__":
    g = Graf()


    g.dodaj_krawedz("A", "B", 1)
    g.dodaj_krawedz("A", "C", 4)
    g.dodaj_krawedz("B", "C", 2)
    g.dodaj_krawedz("B", "D", 7)
    g.dodaj_krawedz("C", "D", 3)
    g.dodaj_krawedz("C", "E", 1)
    g.dodaj_krawedz("D", "F", 5)
    g.dodaj_krawedz("E", "F", 5)

    print("--- Zad 1 ---")
    g.bfs("A")
    g.dfs("A")

    print("\n--- Zad 2 ---")
    g.kruskal_mst()

    g2 = Graf()
    polaczenia = [
        ("A", "B", 6), ("A", "C", 1), ("A", "D", 5),
        ("B", "C", 5), ("B", "E", 3),
        ("C", "D", 5), ("C", "E", 6), ("C", "F", 4),
        ("D", "F", 2), ("E", "F", 6)
    ]

    for u, v, k in polaczenia:
        g2.dodaj_krawedz(u, v, k)

    print("\n--- Zad 3 ---")
    g2.algorytm_prima("A")



