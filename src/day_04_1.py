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
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "@":
                continue
            neighbors = sum(
                1
                for dr in (-1, 0, 1)
                for dc in (-1, 0, 1)
                if (dr, dc) != (0, 0) and 0 <= r + dr < rows and 0 <= c + dc < cols and grid[r + dr][c + dc] == "@"
            )
            if neighbors < 4:
                count += 1
    return count


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 13


def main() -> None:
    with open("input/day_04.txt") as f:
        data = f.read()
    print(solve(parse(data)))


if __name__ == "__main__":
    main()
