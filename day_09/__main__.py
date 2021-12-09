from __future__ import annotations
from pathlib import Path
from typing import List, Set, Tuple
from functools import reduce

data: List[str]
with (Path(__file__).resolve().parent / 'input.txt').open() as f:
    data = f.readlines()

lows = []
indices = []
measurements = []
for i in range(len(data)):
    row = data[i].strip()
    row_data = []
    if row:
        for j in range(len(row)):
            item = int(row[j])
            row_data.append(item)
            neighbors = []
            if i >= 1:
                neighbors.append(data[i - 1][j])
            if i < len(data) - 1:
                neighbors.append(data[i + 1][j])
            if j >= 1:
                neighbors.append(data[i][j-1])
            if j < len(row) - 1:
                neighbors.append(data[i][j+1])
            flag = True
            for neighbor in map(int, neighbors):
                if neighbor <= item:
                    flag = False
            if flag:
                lows.append(item)
                indices.append((i, j))
        measurements.append(row_data)

print(sum(lows) + len(lows))

def branch(data, src: int, index: Tuple[int, int], basin: Set[Tuple[int, int]]):
    if index not in basin:
        i, j = index
        row = data[i]
        item = row[j]
        if item != 9 and item > src:
            basin.add(index)
            if i >= 1:
                branch(data, item, (i - 1, j), basin)
            if i < len(data) - 1:
                branch(data, item, (i + 1, j), basin)
            if j >= 1:
                branch(data, item, (i, j - 1), basin)
            if j < len(row) - 1:
                branch(data, item, (i, j + 1), basin)

totals = []
for i, j in indices:
    item = measurements[i][j]
    items = set()
    items.add(item)
    if i >= 1:
        branch(measurements, item, (i - 1, j), items)
    if i < len(measurements) - 1:
        branch(measurements, item, (i + 1, j), items)
    if j >= 1:
        branch(measurements, item, (i, j - 1), items)
    if j < len(measurements[i]) - 1:
        branch(measurements, item, (i, j + 1), items)
    totals.append(len(items))

totals.sort(reverse=True)
print(reduce(lambda x, y: x * y, totals[:3], 1))
