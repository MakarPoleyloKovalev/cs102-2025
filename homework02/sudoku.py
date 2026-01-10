import pathlib
import typing as tp
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i:i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos"""
    row, _ = pos
    return grid[row][:]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos"""
    _, col = pos
    return [grid[row][col] for row in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos"""
    row, col = pos
    block_row = (row // 3) * 3
    block_col = (col // 3) * 3

    result = []
    for r in range(block_row, block_row + 3):
        for c in range(block_col, block_col + 3):
            result.append(grid[r][c])
    return result


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле"""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '.':
                return (row, col)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции"""
    all_values = set("123456789")

    used_values = set()
    used_values.update(get_row(grid, pos))
    used_values.update(get_col(grid, pos))
    used_values.update(get_block(grid, pos))

    possible = all_values - used_values
    return possible


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    empty_pos = find_empty_positions(grid)

    if empty_pos is None:
        return grid

    row, col = empty_pos
    possible_values = find_possible_values(grid, (row, col))

    for value in possible_values:
        grid[row][col] = value
        solution = solve(grid)

        if solution is not None:
            return solution

        grid[row][col] = '.'

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    if len(solution) != 9 or any(len(row) != 9 for row in solution):
        return False

    for row in range(9):
        row_values = get_row(solution, (row, 0))
        if set(row_values) != set("123456789"):
            return False

    for col in range(9):
        col_values = get_col(solution, (0, col))
        if set(col_values) != set("123456789"):
            return False

    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block_values = get_block(solution, (block_row, block_col))
            if set(block_values) != set("123456789"):
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов"""
    grid = [['.' for _ in range(9)] for _ in range(9)]

    base_grid = [
        list("123456789"),
        list("456789123"),
        list("789123456"),
        list("234567891"),
        list("567891234"),
        list("891234567"),
        list("345678912"),
        list("678912345"),
        list("912345678")
    ]

    for _ in range(10):
        if random.random() > 0.5:
            block = random.randint(0, 2)
            rows = list(range(block * 3, block * 3 + 3))
            random.shuffle(rows)
            for i in range(3):
                base_grid[rows[0] + i], base_grid[rows[1] + i] = base_grid[rows[1] + i], base_grid[rows[0] + i]

    if N >= 81:
        return base_grid

    result = [row[:] for row in base_grid]
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)

    cells_to_remove = 81 - N
    for i in range(min(cells_to_remove, 81)):
        r, c = positions[i]
        result[r][c] = '.'

    return result


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)