"""Wczytanie siatki MES z pliku .txt i wypisanie węzłów oraz elementów.

Użycie:
    python mes_siatka.py plik.txt
"""
import sys


class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class Element:
    def __init__(self, id, node_ids):
        self.id = id
        self.node_ids = node_ids


class Grid:
    def __init__(self):
        self.nodes = []
        self.elements = []


def read_grid(path):
    grid = Grid()
    section = None

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Nagłówek sekcji, np. *Node, *Element, type=DC2D4, *BC
            if line.startswith("*"):
                section = line[1:].split(",")[0].strip().lower()
                continue

            values = line.replace(",", " ").split()
            if section == "node":
                grid.nodes.append(Node(int(values[0]), float(values[1]), float(values[2])))
            elif section == "element":
                grid.elements.append(Element(int(values[0]), [int(v) for v in values[1:]]))

    return grid


def print_grid(grid):
    print(f"Węzły ({len(grid.nodes)}):")
    print(f"{'ID':>5} {'x':>14} {'y':>14}")
    for n in grid.nodes:
        print(f"{n.id:>5} {n.x:>14.8f} {n.y:>14.8f}")

    print(f"\nElementy ({len(grid.elements)}):")
    for e in grid.elements:
        print(f"{e.id:>5}: " + ", ".join(str(i) for i in e.node_ids))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    print_grid(read_grid(sys.argv[1]))
