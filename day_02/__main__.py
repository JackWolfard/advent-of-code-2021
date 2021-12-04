from pathlib import Path
from typing import Generator, Tuple

def get_data(input_path: Path) -> Generator[Tuple[int, int], None, None]:
    with input_path.open() as f:
        while True:
            line = f.readline().strip().split()
            if len(line) == 2:
                direction, value = line
                value = int(value)
                if direction == 'forward':
                    yield value, 0
                elif direction == 'up':
                    yield 0, -value
                else:
                    yield 0, value
            else:
                return None

def calculate_final_position(
    moves: Generator[Tuple[int, int], None, None]
) -> int:
    x, y = 0, 0
    for dx, dy in moves:
        x += dx
        y += dy
    return x * y

def calculate_final_position_w_aim(
    moves: Generator[Tuple[int, int], None, None]
) -> int:
    horizontal, depth, aim = 0, 0, 0
    for dx, dy in moves:
        horizontal += dx
        depth += aim * dx
        aim += dy
    return horizontal * depth

if __name__ == '__main__':
    input_path = Path(__file__).resolve().parent / 'sample.txt'
    moves = get_data(input_path)
    position = calculate_final_position(moves)
    print(f'final position: {position}')
    moves = get_data(input_path)
    position = calculate_final_position_w_aim(moves)
    print(f'final position w/ aim: {position}')
