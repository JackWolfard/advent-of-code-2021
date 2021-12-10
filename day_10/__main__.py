from __future__ import annotations
from pathlib import Path
from typing import List, Set, Tuple
from functools import reduce

lines: List[str]
with (Path(__file__).resolve().parent / 'input.txt').open() as f:
    lines = f.readlines()


pop = '}])>'
push = '{[(<'


# ): 3 points.
# ]: 57 points.
# }: 1197 points.
# >: 25137 points.
match = {
 '{': '}',
 '[': ']',
 '(': ')',
 '<': '>'
}

points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

completion_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

total = 0

completions = []
for i, line in enumerate(lines):
    line = line.strip()
    stack = []
    corrupt = False
    for char in line:
        if char in push:
            stack.append(char)
        elif char in pop:
            item = match[stack.pop()]
            if char != item:
                total += points[char]
                corrupt = True
                break
    if not corrupt and stack:
        total = 0
        while len(stack):
            total *= 5
            total += completion_points[match[stack.pop()]]
        completions.append(total)

print('part 1', total)
completions.sort()
print('part 2', completions[len(completions) // 2])
