from pathlib import Path

SAMPLE = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def parse(data: str) -> tuple[list[tuple[int, int]], list[int]]:
    ranges_part, ids_part = data.strip().split("\n\n")
    ranges = []
    for line in ranges_part.splitlines():
        lo, hi = line.split("-")
        ranges.append((int(lo), int(hi)))
    ids = [int(line) for line in ids_part.splitlines()]
    return ranges, ids


def solve(parsed: tuple[list[tuple[int, int]], list[int]]) -> int:
    ranges, ids = parsed
    return sum(1 for ingredient_id in ids if any(lo <= ingredient_id <= hi for lo, hi in ranges))


def main() -> None:
    data = Path("input/day_05.txt").read_text()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 3


if __name__ == "__main__":
    main()
