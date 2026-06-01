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


def solve(data: str) -> int:
    pos = 50
    count = 0
    for line in data.strip().splitlines():
        direction, distance = line[0], int(line[1:])
        pos = (pos + (-distance if direction == "L" else distance)) % 100
        if pos == 0:
            count += 1
    return count


def main() -> None:
    with open("input/day_01.txt") as f:
        data = f.read()
    print(solve(data))


def test_part1() -> None:
    assert solve(SAMPLE) == 3


if __name__ == "__main__":
    main()
