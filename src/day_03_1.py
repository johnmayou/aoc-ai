SAMPLE = """\
987654321111111
811111111111119
234234234234278
818181911112111"""


def parse(data: str) -> list[str]:
    return data.strip().splitlines()


def _max_joltage(bank: str) -> int:
    best = 0
    for i in range(len(bank) - 1):
        max_after = max(int(c) for c in bank[i + 1 :])
        best = max(best, int(bank[i]) * 10 + max_after)
    return best


def solve(parsed: list[str]) -> int:
    return sum(_max_joltage(bank) for bank in parsed)


def main() -> None:
    with open("input/day_03.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_day03_part1() -> None:
    assert solve(parse(SAMPLE)) == 357


if __name__ == "__main__":
    main()
