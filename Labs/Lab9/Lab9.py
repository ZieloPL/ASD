import time

class TextAlgorithms:
    def __init__(self, filepath="", pattern="hobbit"):
        """
        Konstruktor wczytuje tekst do zadań 1 i 2.
        """
        self.pattern = pattern.lower()
        self.m = len(self.pattern)
        self.text = ""

        # Próba wczytania pliku
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.text = f.read().lower()
            except FileNotFoundError:
                print(f"BŁĄD: Nie znaleziono pliku '{filepath}'. Używam tekstu zastępczego.")
                self.text = ("In a hole in the ground there lived a hobbit. " * 5000).lower()
        else:
            self.text = ("In a hole in the ground there lived a hobbit. " * 5000).lower()

        self.n = len(self.text)


    # ZADANIE 1

    def search_naive(self):
        start = time.time()
        count = 0
        for i in range(self.n - self.m + 1):
            if self.text[i: i + self.m] == self.pattern:
                count += 1
        return count, time.time() - start

    # ZADANIE 2

    def search_rabin_karp(self):
        start = time.time()
        count = 0
        d = 256;
        q = 101
        p = 0;
        t = 0;
        h = 1

        for i in range(self.m - 1):
            h = (h * d) % q

        for i in range(self.m):
            p = (d * p + ord(self.pattern[i])) % q
            t = (d * t + ord(self.text[i])) % q

        for i in range(self.n - self.m + 1):
            if p == t:
                if self.text[i: i + self.m] == self.pattern:
                    count += 1
            if i < self.n - self.m:
                t = (d * (t - ord(self.text[i]) * h) + ord(self.text[i + self.m])) % q
                if t < 0: t += q
        return count, time.time() - start

    def search_kmp(self):
        start = time.time()
        count = 0
        # Budowanie tablicy LPS
        lps = [0] * self.m
        length = 0;
        i = 1
        while i < self.m:
            if self.pattern[i] == self.pattern[length]:
                length += 1;
                lps[i] = length;
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0; i += 1

        # Wyszukiwanie
        i = 0;
        j = 0
        while i < self.n:
            if self.pattern[j] == self.text[i]:
                i += 1;
                j += 1
            if j == self.m:
                count += 1;
                j = lps[j - 1]
            elif i < self.n and self.pattern[j] != self.text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return count, time.time() - start

    def search_boyer_moore(self):
        start = time.time()
        count = 0
        bad_char = {self.pattern[i]: i for i in range(self.m)}
        s = 0
        while s <= self.n - self.m:
            j = self.m - 1
            while j >= 0 and self.pattern[j] == self.text[s + j]:
                j -= 1
            if j < 0:
                count += 1
                s += (self.m - bad_char.get(self.text[s + self.m], -1) if s + self.m < self.n else 1)
            else:
                s += max(1, j - bad_char.get(self.text[s + j], -1))
        return count, time.time() - start


    # ZADANIE 3

    def solve_longest_prefix_suffix(self, input_text):
        n = len(input_text)
        lps = [0] * n
        length = 0
        i = 1
        while i < n:
            if input_text[i] == input_text[length]:
                length += 1;
                lps[i] = length;
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0; i += 1

        return input_text[:lps[-1]]

    # ZADANIE 4

    def solve_wildcard(self, text, pattern):
        n, m = len(text), len(pattern)
        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True

        for j in range(1, m + 1):
            if pattern[j - 1] == '*': dp[0][j] = dp[0][j - 1]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if pattern[j - 1] == text[i - 1] or pattern[j - 1] == '?':
                    dp[i][j] = dp[i - 1][j - 1]
                elif pattern[j - 1] == '*':
                    dp[i][j] = dp[i][j - 1] or dp[i - 1][j]

        return dp[n][m]

    # ZADANIE 5: Wyszukiwanie w tablicy 2D

    def solve_2d_search(self, grid, word):
        rows = len(grid);
        cols = len(grid[0])
        results = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != word[0]: continue

                for dr, dc in directions:
                    end_r = r + (len(word) - 1) * dr
                    end_c = c + (len(word) - 1) * dc
                    if 0 <= end_r < rows and 0 <= end_c < cols:
                        match = True
                        for k in range(1, len(word)):
                            if grid[r + k * dr][c + k * dc] != word[k]:
                                match = False;
                                break
                        if match:
                            results.append(f"Start: [{r}, {c}], Kierunek: ({dr},{dc})")
        return results

if __name__ == "__main__":

    algo = TextAlgorithms(filepath="Hobbit.txt", pattern="hobbit")

    print(f"\n=== ZADANIE 1 i 2 ===")
    print(f"{'Algorytm':<20} | {'Liczba wystąpień':<18} | {'Czas [s]':<10}")
    print("-" * 55)

    cnt, t = algo.search_naive()
    print(f"{'Naiwny':<20} | {cnt:<18} | {t:.6f}")

    cnt, t = algo.search_rabin_karp()
    print(f"{'Rabin-Karp':<20} | {cnt:<18} | {t:.6f}")

    cnt, t = algo.search_kmp()
    print(f"{'KMP':<20} | {cnt:<18} | {t:.6f}")

    cnt, t = algo.search_boyer_moore()
    print(f"{'Boyer-Moore':<20} | {cnt:<18} | {t:.6f}")

    print("\n=== ZADANIE 3 ===")
    test_str = "aabcdaabc"
    result = algo.solve_longest_prefix_suffix(test_str)
    print(f"Input: {test_str}")
    print(f"Output: {result}")

    print("\n=== ZADANIE 4 ===")
    t1, p1 = "baaabab", "baa?bab"
    t2, p2 = "baaabab", "a*ab"
    print(f"Tekst: {t1}, Wzorzec: {p1} -> {algo.solve_wildcard(t1, p1)}")
    print(f"Tekst: {t2}, Wzorzec: {p2} -> {algo.solve_wildcard(t2, p2)}")

    print("\n=== ZADANIE 5 ===")
    grid = [
        ['a', 'b', 'c', 'd'],
        ['e', 'k', 'g', 'h'],
        ['i', 'g', 'o', 'x'],
        ['m', 'o', 't', 't']
    ]
    word_2d = "kot"
    print("Tablica:")
    for row in grid: print(row)
    print(f"Szukane słowo: {word_2d}")
    results_2d = algo.solve_2d_search(grid, word_2d)
    for res in results_2d:
        print(res)