from itertools import combinations
from pathlib import Path

SAMPLE = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


def parse(data: str) -> list[tuple[int, int]]:
    points = []
    for line in data.strip().splitlines():
        x, y = line.split(",")
        points.append((int(x), int(y)))
    return points


def solve(points: list[tuple[int, int]]) -> int:
    best = 0
    for (x1, y1), (x2, y2) in combinations(points, 2):
        area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
        if area > best:
            best = area
    return best


def main() -> None:
    data = Path("input/day_09.txt").read_text()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 50


if __name__ == "__main__":
    main()
