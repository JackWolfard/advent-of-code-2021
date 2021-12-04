from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, Union

def get_data(input_path: Path) -> Generator[int, str, None]:
    with input_path.open() as f:
        line = f.readline().strip()
        yield len(line)
        yield line
        while True:
            line = f.readline().strip()
            if line:
                yield line
            else:
                return None

def power_consumption(size: int, report: List[str]) -> int:
    gamma = ''
    for i in range(size):
        gamma += most_common_bit(i, report)
    gamma = int(gamma, 2)
    epsilon = ~gamma & ((1 << size) - 1)
    return gamma * epsilon

def most_common_bit(index: int, report: List[str], filter_uncommon: bool = False,
                    least_common: bool = False
                    ) -> Union[str, Tuple[str, List[str]]]:
    num_ones = 0
    ones = []
    zeroes = []
    for bits in report:
        num_ones += int(bits[index])
        if bits[index] == '1':
            ones.append(bits)
        else:
            zeroes.append(bits)
    threshold = len(report) / 2
    common_bit: str
    filtered: List[str]
    if (num_ones < threshold and least_common 
        or num_ones >= threshold and not least_common):
        common_bit = '1'
        filtered = ones
    else:
        common_bit = '0'
        filtered = zeroes
    if filter_uncommon:
        return common_bit, filtered
    return common_bit

def oxygen_rating(size: int, report: List[str]) -> int:
    rating = ''
    for i in range(size):
        bit, report = most_common_bit(i, report, filter_uncommon=True)
        rating += bit
        if len(report) == 1:
            rating = report[0]
            break
    return int(rating, 2)

def c02_rating(size: int, report: List[str]) -> int:
    rating = ''
    for i in range(size):
        bit, report = most_common_bit(i, report, filter_uncommon=True,
                                      least_common=True)
        rating += bit
        if len(report) == 1:
            rating = report[0]
            break
    return int(rating, 2)

if __name__ == '__main__':
    input_path = Path(__file__).resolve().parent / 'input.txt'
    report = get_data(input_path)
    size = next(report)
    report = list(report)
    power = power_consumption(size, report)
    oxygen = oxygen_rating(size, report)
    c02 = c02_rating(size, report)
    life_support = oxygen * c02
    print(f'power consumption: {power}')
    print(f'life support rating: {life_support}')
