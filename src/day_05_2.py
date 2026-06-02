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


def parse(data: str) -> list[tuple[int, int]]:
    ranges_part = data.strip().split("\n\n")[0]
    return [(int(lo), int(hi)) for lo, hi in (line.split("-") for line in ranges_part.splitlines())]


def solve(ranges: list[tuple[int, int]]) -> int:
    merged: list[tuple[int, int]] = []
    for lo, hi in sorted(ranges):
        if merged and lo <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return sum(hi - lo + 1 for lo, hi in merged)


def main() -> None:
    data = Path("input/day_05.txt").read_text()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 14


if __name__ == "__main__":
    main()
