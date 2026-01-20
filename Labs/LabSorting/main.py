import time
import random
import copy
import heapq
from dataclasses import dataclass


# Klasa pomocnicza
@dataclass
class Student:
    id: int
    name: str
    score: float
    age: int

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', score={self.score}, age={self.age})"


# --- Główna klasa z rozwiązaniami ---
class AdvancedSorting:

    # 1. SORTOWANIE KUBEŁKOWE (Bucket Sort)

    def bucket_sort(self, arr):
        """
        Działa najlepiej dla liczb z rozkładu jednostajnego w przedziale [0, 1).
        Złożoność: O(n + k), gdzie k to liczba kubełków.
        """
        if not arr: return []

        # Tworzymy puste kubełki
        bucket_count = len(arr)
        buckets = [[] for _ in range(bucket_count)]

        # Rozdzielamy elementy do kubełków
        for num in arr:
            index = int(num * bucket_count)
            # Zabezpieczenie dla wartości 1.0 (powinna trafić do ostatniego kubła)
            if index == bucket_count:
                index -= 1
            buckets[index].append(num)

        # Sortujemy każdy kubełek (np. Insertion Sortem lub wbudowanym)
        # i łączymy wyniki
        sorted_arr = []
        for bucket in buckets:
            bucket.sort()  # Wewnątrz kubełka jest mało elementów, więc działa szybko
            sorted_arr.extend(bucket)

        return sorted_arr

    # 2. SORTOWANIE NIESTANDARDOWYCH DANYCH

    def sort_custom_objects(self, students, criteria='score'):
        """
        Sortuje listę obiektów Student według podanego kryterium.
        Wykorzystuje Pythona 'key'.
        """
        if criteria == 'score':
            # Sortowanie malejąco po wynikach
            return sorted(students, key=lambda s: s.score, reverse=True)
        elif criteria == 'name':
            # Sortowanie alfabetycznie po imieniu
            return sorted(students, key=lambda s: s.name)
        elif criteria == 'age_then_score':
            # Sortowanie złożone: najpierw wiek, potem wynik
            return sorted(students, key=lambda s: (s.age, -s.score))
        return students

    # 3. SORTOWANIE CZĄSTKOWE (Partial Sort)

    def partial_sort_top_k(self, arr, k):
        # heapq.nsmallest zwraca k najmniejszych elementów w czasie O(N log k)
        # heapq.nlargest dla największych
        return heapq.nsmallest(k, arr)


    # 4. HYBRYDOWY ALGORYTM SORTOWANIA

    def hybrid_sort(self, arr, threshold=32):
        """
        Połączenie QuickSorta z Insertion Sortem.
        Gdy podproblem jest mały (< threshold), używamy Insertion Sort,
        który jest szybszy dla małych zbiorów danych .
        """

        def insertion_sort(sub_arr):
            for i in range(1, len(sub_arr)):
                key = sub_arr[i]
                j = i - 1
                while j >= 0 and key < sub_arr[j]:
                    sub_arr[j + 1] = sub_arr[j]
                    j -= 1
                sub_arr[j + 1] = key
            return sub_arr

        def quick_sort_recursive(sub_arr):
            if len(sub_arr) < threshold:
                return insertion_sort(sub_arr)
            else:
                pivot = sub_arr[len(sub_arr) // 2]
                left = [x for x in sub_arr if x < pivot]
                middle = [x for x in sub_arr if x == pivot]
                right = [x for x in sub_arr if x > pivot]
                return quick_sort_recursive(left) + middle + quick_sort_recursive(right)

        return quick_sort_recursive(arr)

    # 5. IN-PLACE (HeapSort) vs OUT-OF-PLACE (MergeSort)

    def heap_sort_inplace(self, arr):
        n = len(arr)
        # Budowanie sterty
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        # Wyjmowanie elementów
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # Swap
            self._heapify(arr, i, 0)
        return arr

    def _heapify(self, arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]: largest = l
        if r < n and arr[r] > arr[largest]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest)

    def merge_sort(self, arr):
        if len(arr) <= 1: return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


if __name__ == "__main__":
    sorter = AdvancedSorting()

    print("--- 1. TEST SORTOWANIA KUBEŁKOWEGO ---")
    data_float = [random.random() for _ in range(10_000)]
    start = time.time()
    sorter.bucket_sort(data_float)
    t_bucket = time.time() - start

    start = time.time()
    sorted(data_float)  # Timsort (standardowy Python)
    t_standard = time.time() - start
    print(f"Bucket Sort: {t_bucket:.6f}s | Timsort: {t_standard:.6f}s")

    print("\n--- 2. TEST DANYCH NIESTANDARDOWYCH ---")
    students = [
        Student(1, "Ania", 4.5, 21),
        Student(2, "Bartek", 3.0, 22),
        Student(3, "Celina", 5.0, 20),
        Student(4, "Darek", 4.5, 23)
    ]
    print("Oryginalnie:", students)
    print("Wg oceny (malejąco):", sorter.sort_custom_objects(students, 'score'))
    print("Wg wieku potem oceny:", sorter.sort_custom_objects(students, 'age_then_score'))

    print("\n--- 3. TEST SORTOWANIA CZĄSTKOWEGO (Top K) ---")
    big_data = [random.randint(0, 100000) for _ in range(1_000_000)]
    k = 10
    start = time.time()
    top_k = sorter.partial_sort_top_k(big_data, k)
    t_partial = time.time() - start

    start = time.time()
    full_sort_slice = sorted(big_data)[:k]
    t_full = time.time() - start

    print(f"Pobranie {k} najmniejszych z 1mln elementów.")
    print(f"Partial Sort (Heap): {t_partial:.6f}s | Full Sort + Slice: {t_full:.6f}s")
    print("Wynik Partial:", top_k)

    print("\n--- 4. TEST HYBRYDOWY ---")
    data_hybrid = [random.randint(0, 1000) for _ in range(5000)]
    start = time.time()
    sorter.hybrid_sort(data_hybrid)
    print(f"Czas Hybrydowy (Quick+Insert): {time.time() - start:.6f}s")

    print("\n--- 5. IN-PLACE vs OUT-OF-PLACE ---")
    data_ipc = [random.randint(0, 10000) for _ in range(20_000)]
    data_oop = list(data_ipc)  # Kopia

    start = time.time()
    sorter.heap_sort_inplace(data_ipc)
    t_in = time.time() - start

    start = time.time()
    sorter.merge_sort(data_oop)
    t_out = time.time() - start

    print(f"HeapSort (In-Place): {t_in:.6f}s | MergeSort (Out-of-Place): {t_out:.6f}s")