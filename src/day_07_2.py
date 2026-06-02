from bisect import bisect_left
from functools import cache

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
    cols = len(grid[0])

    s_row = s_col = 0
    for r, row in enumerate(grid):
        if "S" in row:
            s_row, s_col = r, row.index("S")
            break

    splitters_by_col: dict[int, tuple[int, ...]] = {}
    for c in range(cols):
        col_splitters = tuple(r for r, row in enumerate(grid) if row[c] == "^")
        if col_splitters:
            splitters_by_col[c] = col_splitters

    @cache
    def count_timelines(col: int, start_row: int) -> int:
        if col < 0 or col >= cols:
            return 1
        col_splitters = splitters_by_col.get(col)
        if col_splitters is None:
            return 1
        idx = bisect_left(col_splitters, start_row)
        if idx >= len(col_splitters):
            return 1
        hit_row = col_splitters[idx]
        return count_timelines(col - 1, hit_row) + count_timelines(col + 1, hit_row)

    return count_timelines(s_col, s_row)


def main() -> None:
    with open("input/day_07.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 40


if __name__ == "__main__":
    main()
