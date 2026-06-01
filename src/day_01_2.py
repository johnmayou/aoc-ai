SAMPLE = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def parse(data: str) -> list[tuple[str, int]]:
    result = []
    for line in data.strip().splitlines():
        result.append((line[0], int(line[1:])))
    return result


def zeros_passed(pos: int, direction: str, distance: int) -> int:
    if direction == "L":
        first_hit = pos if pos > 0 else 100
    else:
        first_hit = (100 - pos) % 100 or 100
    if distance < first_hit:
        return 0
    return (distance - first_hit) // 100 + 1


def solve(instructions: list[tuple[str, int]]) -> int:
    pos = 50
    count = 0
    for direction, distance in instructions:
        count += zeros_passed(pos, direction, distance)
        pos = (pos + (-distance if direction == "L" else distance)) % 100
    return count


def main() -> None:
    data = open("input/day_01.txt").read()
    print(solve(parse(data)))


def test_part2() -> None:
    assert solve(parse(SAMPLE)) == 6


if __name__ == "__main__":
    main()
