SAMPLE = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def parse(data: str) -> list[list[str]]:
    return [list(line) for line in data.strip().splitlines()]


def solve(grid: list[list[str]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    total = 0
    while True:
        removable = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if grid[r][c] == "@"
            and sum(
                1
                for dr in (-1, 0, 1)
                for dc in (-1, 0, 1)
                if (dr, dc) != (0, 0) and 0 <= r + dr < rows and 0 <= c + dc < cols and grid[r + dr][c + dc] == "@"
            )
            < 4
        ]
        if not removable:
            break
        for r, c in removable:
            grid[r][c] = "."
        total += len(removable)
    return total


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 43


def main() -> None:
    with open("input/day_04.txt") as f:
        data = f.read()
    print(solve(parse(data)))


if __name__ == "__main__":
    main()
