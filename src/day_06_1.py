SAMPLE = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """


def parse(data: str) -> list[str]:
    return data.splitlines()


def solve(lines: list[str]) -> int:
    max_len = max(len(line) for line in lines)
    padded = [line.ljust(max_len) for line in lines]

    sep_cols = {col for col in range(max_len) if all(row[col] == " " for row in padded)}

    problems: list[list[int]] = []
    current: list[int] = []
    for col in range(max_len):
        if col in sep_cols:
            if current:
                problems.append(current)
                current = []
        else:
            current.append(col)
    if current:
        problems.append(current)

    num_rows = padded[:-1]
    op_row = padded[-1]

    total = 0
    for cols in problems:
        op = next(op_row[c] for c in cols if op_row[c] != " ")
        numbers = []
        for row in num_rows:
            segment = "".join(row[c] for c in cols).strip()
            if segment:
                numbers.append(int(segment))

        if op == "*":
            result = 1
            for n in numbers:
                result *= n
        else:
            result = sum(numbers)

        total += result

    return total


def main() -> None:
    with open("input/day_06.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 4277556


if __name__ == "__main__":
    main()
