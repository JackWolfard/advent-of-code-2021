from pathlib import Path
from typing import Dict, Generator, List, Set, Tuple
from functools import reduce

class BingoBoard:
    _numbers_to_positions: Dict[int, Tuple[int, int]]
    _board: List[List[bool]]
    _unmarked: Set[int]
    _last_draw: int = 0

    def __init__(self, board: List[List[int]]):
        self._numbers_to_positions = {}
        self._unmarked = set()
        self._board = [[False] * len(board[0]) for _ in range(len(board))] 
        for i, row in enumerate(board):
            for j, number in enumerate(row):
                self._unmarked.add(number)
                self._numbers_to_positions[number] = (i, j)
    
    def draw(self, draw: int) -> bool:
        self._last_draw = draw
        if draw in self._numbers_to_positions:
            try:
                self._unmarked.remove(draw)
            except:
                pass
            position = self._numbers_to_positions[draw]
            self._board[position[0]][position[1]] = True
            return self.check_bingo()
        return False
    
    def check_bingo(self) -> bool:
        # row
        for row in self._board:
            if self.check_row(row):
                return True
        # col
        for i in range(len(self._board[0])):
            if self.check_row([row[i] for row in self._board]):
                return True
        # diagonal
        # length = len(self._board)
        # major = [self._board[i][i] for i in range(length)]
        # minor = [self._board[i][length - (i + 1)] for i in range(length)]
        # if self.check_row(major) or self.check_row(minor):
        #     return True
        return False
    
    def check_row(self, row: List[int]) -> bool:
        return reduce(lambda x, y: x and y, row)
    
    def score(self) -> int:
        return sum(self._unmarked) * self._last_draw
    
def get_data(input_path: Path) -> Generator[List[int], BingoBoard, None]:
    data: List[List[int]] = []
    with input_path.open() as f:
        line = f.readline().strip()
        yield list(map(int, line.split(',')))
        while True:
            line = f.readline()
            if not line:
                if len(data) > 0:
                    yield BingoBoard(data)
                return None
            line = line.strip()
            if line:
                data.append(list(map(int, line.split())))
            elif len(data) > 0:
                yield BingoBoard(data)
                data = []

def get_first_winner(draws: List[int], boards: List[BingoBoard]) -> BingoBoard:
    for draw in draws:
        for board in boards:
            if board.draw(draw):
                return board

def get_last_winner(draws: List[int], boards: List[BingoBoard]) -> BingoBoard:
    winners = []
    for draw in draws:
        non_winning_boards = []
        if len(boards) == 0:
            break
        for board in boards:
            if board.draw(draw):
                winners.append(board)
            else:
                non_winning_boards.append(board)
        boards = non_winning_boards
    return winners[-1]

if __name__ == '__main__':
    input_path = Path(__file__).resolve().parent / 'input.txt'
    gen = get_data(input_path)
    draws: List[int] = next(gen)
    boards: List[BingoBoard] = list(gen)
    winner = get_first_winner(draws, boards)
    last_winner = get_last_winner(draws, boards)
    print(f'score of winning board: {winner.score()}')
    print(f'score of last winning board: {last_winner.score()}')
