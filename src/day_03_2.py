SAMPLE = """\
987654321111111
811111111111119
234234234234278
818181911112111"""


def parse(data: str) -> list[str]:
    return data.strip().splitlines()


def _largest_k_digit(bank: str, k: int) -> int:
    n = len(bank)
    result = []
    start = 0
    for i in range(k):
        end = n - k + i + 1
        best_pos = start
        for j in range(start + 1, end):
            if bank[j] > bank[best_pos]:
                best_pos = j
        result.append(bank[best_pos])
        start = best_pos + 1
    return int("".join(result))


def solve(parsed: list[str]) -> int:
    return sum(_largest_k_digit(bank, 12) for bank in parsed)


def main() -> None:
    with open("input/day_03.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_day03_part2() -> None:
    assert solve(parse(SAMPLE)) == 3121910778619


if __name__ == "__main__":
    main()
