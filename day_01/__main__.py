from pathlib import Path
from typing import List

def get_data(input_path: Path) -> List[int]:
    with input_path.open() as f:
        raw = f.read()
    data: List[str] = raw.strip().split()
    return list(map(int, data))

def count_increases(data: List[int]) -> int:
    increases = 0
    for i in range(len(data) - 1):
        increases += int(data[i] < data[i + 1])
    return increases

def count_sliding_increases(data: List[int], window: int = 3) -> int:
    increases = 0
    for i in range(len(data) - window):
        a = sum(data[i:i+window])
        b = sum(data[(i + 1):(i+1)+window])
        increases += int(a < b)
    return increases

if __name__ == '__main__':
    input_path = Path(__file__).resolve().parent / 'input.txt'
    data: List[int] = get_data(input_path)
    increases = count_increases(data)
    print(f'number of increases: {increases}')
    window = 3
    increases = count_sliding_increases(data, window)
    print(f'number of sliding increases w/ window={window}: {increases}')
