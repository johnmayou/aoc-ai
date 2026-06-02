import re

SAMPLE = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()


def parse(data: str) -> list[tuple[int, int, list[int]]]:
    machines = []
    for line in data.strip().split("\n"):
        match = re.search(r"\[([^\]]+)\]", line)
        assert match is not None
        diag = match.group(1)
        n_lights = len(diag)
        target = sum(1 << i for i, c in enumerate(diag) if c == "#")
        buttons = [sum(1 << int(x) for x in m.group(1).split(",")) for m in re.finditer(r"\(([^)]+)\)", line)]
        machines.append((n_lights, target, buttons))
    return machines


def min_presses(n_lights: int, target: int, buttons: list[int]) -> int:
    """
    Minimum button presses to reach target, solving Ax = b over GF(2).
    We enumerate the affine solution space and return the minimum Hamming weight.
    """
    m = len(buttons)
    n = n_lights

    # Build augmented matrix: row[i] encodes which buttons affect light i plus target bit
    rows = []
    for i in range(n):
        row = sum((1 << j) for j, btn in enumerate(buttons) if btn & (1 << i))
        row |= (target >> i & 1) << m
        rows.append(row)

    # Gaussian elimination over GF(2)
    pivot_row_of = [-1] * m
    cur_row = 0
    for col in range(m):
        found = next((r for r in range(cur_row, n) if rows[r] & (1 << col)), -1)
        if found == -1:
            continue
        rows[cur_row], rows[found] = rows[found], rows[cur_row]
        pivot_row_of[col] = cur_row
        for r in range(n):
            if r != cur_row and rows[r] & (1 << col):
                rows[r] ^= rows[cur_row]
        cur_row += 1

    pivot_cols = [c for c in range(m) if pivot_row_of[c] != -1]
    free_cols = [c for c in range(m) if pivot_row_of[c] == -1]

    # Particular solution: set all free variables to 0
    particular = sum((1 << col) for col in pivot_cols if (rows[pivot_row_of[col]] >> m) & 1)

    # One null-space basis vector per free column
    null_vecs = []
    for fc in free_cols:
        vec = (1 << fc) | sum((1 << col) for col in pivot_cols if rows[pivot_row_of[col]] & (1 << fc))
        null_vecs.append(vec)

    # Find minimum Hamming weight over all 2^|free| solutions
    min_w = bin(particular).count("1")
    for mask in range(1, 1 << len(null_vecs)):
        sol = particular
        for i, nv in enumerate(null_vecs):
            if mask & (1 << i):
                sol ^= nv
        w = bin(sol).count("1")
        if w < min_w:
            min_w = w

    return min_w


def solve(machines: list[tuple[int, int, list[int]]]) -> int:
    return sum(min_presses(n, t, btns) for n, t, btns in machines)


def main() -> None:
    with open("input/day_10.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 7


if __name__ == "__main__":
    main()
