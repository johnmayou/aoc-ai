from bisect import bisect_left
from collections import defaultdict

SAMPLE = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


def parse(data: str) -> list[str]:
    return data.splitlines()


def solve(grid: list[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])

    s_row = s_col = 0
    for r, row in enumerate(grid):
        if "S" in row:
            s_row, s_col = r, row.index("S")
            break

    splitters_by_col: dict[int, list[int]] = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "^":
                splitters_by_col[c].append(r)

    hit_splitters: set[tuple[int, int]] = set()
    visited_beams: set[tuple[int, int]] = set()
    stack: list[tuple[int, int]] = [(s_col, s_row)]

    while stack:
        col, start_row = stack.pop()
        if col < 0 or col >= cols:
            continue
        if (col, start_row) in visited_beams:
            continue
        visited_beams.add((col, start_row))

        col_splitters = splitters_by_col[col]
        idx = bisect_left(col_splitters, start_row)
        if idx >= len(col_splitters):
            continue

        hit_row = col_splitters[idx]
        if (hit_row, col) in hit_splitters:
            continue

        hit_splitters.add((hit_row, col))
        stack.append((col - 1, hit_row))
        stack.append((col + 1, hit_row))

    return len(hit_splitters)


def main() -> None:
    with open("input/day_07.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 21


if __name__ == "__main__":
    main()
