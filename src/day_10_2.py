import re
from fractions import Fraction

SAMPLE = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()


def parse(data: str) -> list[tuple[list[list[int]], list[int]]]:
    machines = []
    for line in data.strip().split("\n"):
        buttons = [[int(x) for x in m.group(1).split(",")] for m in re.finditer(r"\(([^)]+)\)", line)]
        joltage_match = re.search(r"\{([^}]+)\}", line)
        assert joltage_match is not None
        targets = [int(x) for x in joltage_match.group(1).split(",")]
        machines.append((buttons, targets))
    return machines


def solve(machines: list[tuple[list[list[int]], list[int]]]) -> int:
    return sum(_min_presses(buttons, targets) for buttons, targets in machines)


def _lp(
    A: list[list[Fraction]],
    b: list[Fraction],
    c: list[Fraction],
) -> tuple[Fraction, list[Fraction]] | None:
    """
    Solve LP: min c^T x s.t. Ax = b, x >= 0.
    Returns (optimal_value, x_solution) or None if infeasible.
    Two-phase simplex with exact Fraction arithmetic.
    """
    n = len(b)
    m = len(c)
    F = Fraction
    n_art = n
    n_total = m + n_art

    T = [A[i][:] + [F(1 if i == j else 0) for j in range(n_art)] + [b[i]] for i in range(n)]
    basis = list(range(m, n_total))

    def pivot(r: int, s: int) -> None:
        T[r] = [x / T[r][s] for x in T[r]]
        for i in range(n):
            if i != r and T[i][s]:
                f = T[i][s]
                T[i] = [T[i][k] - f * T[r][k] for k in range(n_total + 1)]
        basis[r] = s

    def elim(obj: list[Fraction], s: int, r: int) -> None:
        f = obj[s]
        if f:
            for k in range(n_total + 1):
                obj[k] -= f * T[r][k]

    def simplex(obj: list[Fraction], cols: range) -> None:
        while True:
            s = next((j for j in cols if obj[j] < 0), None)
            if s is None:
                break
            r, best_ratio = -1, Fraction(-1)
            for i in range(n):
                if T[i][s] > 0:
                    ratio = T[i][-1] / T[i][s]
                    if r == -1 or ratio < best_ratio or (ratio == best_ratio and basis[i] < basis[r]):
                        r, best_ratio = i, ratio
            if r == -1:
                break
            pivot(r, s)
            elim(obj, s, r)

    obj1: list[Fraction] = [F(-sum(A[i][j] for i in range(n))) for j in range(m)] + [F(0)] * n_art + [F(-sum(b))]
    simplex(obj1, range(n_total))

    if -obj1[-1] > 0:
        return None

    for i in range(n):
        if basis[i] >= m:
            for j in range(m):
                if T[i][j]:
                    pivot(i, j)
                    break

    obj2: list[Fraction] = list(c) + [F(0)] * n_art + [F(0)]
    for i in range(n):
        bj = basis[i]
        if bj < m and obj2[bj]:
            elim(obj2, bj, i)

    simplex(obj2, range(m))

    x: list[Fraction] = [F(0)] * m
    for i in range(n):
        if basis[i] < m:
            x[basis[i]] = T[i][-1]

    return (-obj2[-1], x)


def _min_presses(buttons: list[list[int]], targets: list[int]) -> int:
    """
    Solve: min sum(x) s.t. A*x = targets, x >= 0 integer.
    Uses branch-and-bound with LP relaxation via exact simplex.
    Ceil branch: substitute y = x - ceil (shift lb).
    Floor branch: add slack row x[j] + s = floor.
    """
    F = Fraction
    m_orig = len(buttons)
    n_orig = len(targets)

    A0 = [[F(0)] * m_orig for _ in range(n_orig)]
    for j, ctrs in enumerate(buttons):
        for i in ctrs:
            A0[i][j] = F(1)
    b0 = [F(t) for t in targets]
    c0 = [F(1)] * m_orig

    best: list[Fraction | None] = [None]

    def branch(
        A: list[list[Fraction]],
        b: list[Fraction],
        c: list[Fraction],
        fixed: Fraction,
    ) -> None:
        if any(bi < 0 for bi in b):
            return

        result = _lp(A, b, c)
        if result is None:
            return

        lp_val, x_sol = result
        lb = fixed + lp_val
        if best[0] is not None and lb >= best[0]:
            return

        frac_idx = next((j for j in range(m_orig) if x_sol[j].denominator != 1), None)

        if frac_idx is None:
            total = fixed + sum(c[j] * x_sol[j] for j in range(len(c)))
            if best[0] is None or total < best[0]:
                best[0] = total
            return

        fv = x_sol[frac_idx]
        fl = int(fv)
        cl = fl + 1

        # Ceil branch: x[frac_idx] >= cl
        new_b = [b[i] - cl * A[i][frac_idx] for i in range(len(b))]
        branch(A, new_b, c, fixed + cl)

        # Floor branch: x[frac_idx] <= fl via slack row
        if fl >= 0:
            new_A = [row[:] + [F(0)] for row in A]
            slack_row: list[Fraction] = [F(0)] * len(c) + [F(1)]
            slack_row[frac_idx] = F(1)
            new_A.append(slack_row)
            branch(new_A, b + [F(fl)], c + [F(0)], fixed)

    branch(A0, b0, c0, F(0))
    return int(best[0])  # type: ignore[arg-type]


def main() -> None:
    with open("input/day_10.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 33


if __name__ == "__main__":
    main()
