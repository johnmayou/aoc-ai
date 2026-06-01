SAMPLE = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"


def _is_invalid(n: int) -> bool:
    s = str(n)
    length = len(s)
    return any(s == s[:d] * (length // d) for d in range(1, length) if length % d == 0)


def parse(data: str) -> list[tuple[int, int]]:
    parts = data.strip().split(",")
    return [(int(a), int(b)) for p in parts for a, b in [p.strip().split("-")]]


def solve(parsed: list[tuple[int, int]]) -> int:
    return sum(n for start, end in parsed for n in range(start, end + 1) if _is_invalid(n))


def main() -> None:
    with open("input/day_02.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_day02_part2() -> None:
    assert solve(parse(SAMPLE)) == 4174379265


if __name__ == "__main__":
    main()
