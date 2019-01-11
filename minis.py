#!/usr/bin/env python3

import pathlib

# This is size, count, name
MINIS_SRC = """
20 3 Goblin Cutter
20 3 Goblin Archer
20 1 Regis
20 1 Goblin Champion

25 1 Artemis Entreri
25 3 Drow Duelist
25 1 Drow Wizard
25 3 Hunting Drake
25 3 Hypnotic Spirit
25 1 Spider Swarm (stack)
25 1 Bruenor
25 3 Water Elemental
25 1 Drizzt
25 1 Guenhwyvar
25 1 Methil El-Viddenvelp
25 1 Wulfgar
25 1 Catti-Brie
25 1 Athrogate
25 1 Jarlaxle Baenre
25 1 Yochlol (Drow Form)
25 1 Yvonnel Baenre

50 2 Feral Troll
50 1 Dinin Do'urden
50 1 Shimmergloom

75 1 Errtu
"""


MINIS = []

for r in MINIS_SRC.split("\n"):
    r = r.strip()
    parts = r.split(None, 2)
    if len(parts) < 3:
        continue
    MINIS.append((int(parts[0]), int(parts[1]), parts[2]))


def miniskey(a):
    return (a[0], a[-1])


MINIS.sort(key=miniskey)

SIZE = 0
COUNT = 1
NAME = 2


def main():
    from pprint import pprint

    pprint(MINIS)

    images = []
    for fn in pathlib.Path("Source Photos").iterdir():
        images.append(fn.stem)

    total = 0
    counts = {}
    for size, count, name in MINIS:
        total += count
        counts[size] = counts.get(size, 0) + count
        if name in images:
            images.remove(name)
        else:
            print("*** Missing:", name)

    print("Total:", total)
    print("Unique:", len(MINIS))
    pprint(counts)
    print()
    print("Not mentioned:", images)


if __name__ == "__main__":
    main()
