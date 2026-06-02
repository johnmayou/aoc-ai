from collections import deque
from pathlib import Path

SAMPLE = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


def parse(data: str) -> list[tuple[int, int]]:
    points = []
    for line in data.strip().splitlines():
        x, y = line.split(",")
        points.append((int(x), int(y)))
    return points


def _compress(keys: list[int]) -> list[tuple[int, int]]:
    """
    Build a compressed axis from sorted unique coordinates.
    Each entry is (representative_original_value, width_in_original_coords).
    Includes one-cell exterior strips on each side.
    """
    result = [(keys[0] - 1, 1)]  # exterior strip before first key
    for i, k in enumerate(keys):
        if i > 0 and k > keys[i - 1] + 1:
            result.append((keys[i - 1] + 1, k - keys[i - 1] - 1))  # interior gap
        result.append((k, 1))
    result.append((keys[-1] + 1, 1))  # exterior strip after last key
    return result


def solve(points: list[tuple[int, int]]) -> int:
    n = len(points)

    xs = sorted({x for x, _ in points})
    ys = sorted({y for _, y in points})

    cx = _compress(xs)  # [(rep_x, width), ...]
    cy = _compress(ys)  # [(rep_y, height), ...]

    x_to_ci = {rep: i for i, (rep, _) in enumerate(cx)}
    y_to_ri = {rep: i for i, (rep, _) in enumerate(cy)}

    CW, CH = len(cx), len(cy)

    # Mark compressed cells that lie on a polygon edge
    cboundary: set[tuple[int, int]] = set()
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        if x1 == x2:
            ci = x_to_ci[x1]
            for r in range(y_to_ri[min(y1, y2)], y_to_ri[max(y1, y2)] + 1):
                cboundary.add((ci, r))
        else:
            ri = y_to_ri[y1]
            for c in range(x_to_ci[min(x1, x2)], x_to_ci[max(x1, x2)] + 1):
                cboundary.add((c, ri))

    # Flood fill exterior; (0,0) is always the outer-left/outer-top strip
    exterior: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque([(0, 0)])
    exterior.add((0, 0))
    while queue:
        c, r = queue.popleft()
        for dc, dr in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nc, nr = c + dc, r + dr
            if 0 <= nc < CW and 0 <= nr < CH and (nc, nr) not in exterior and (nc, nr) not in cboundary:
                exterior.add((nc, nr))
                queue.append((nc, nr))

    # Weighted grid: each valid cell contributes its actual original-coord area
    grid = [[0] * CW for _ in range(CH)]
    for c, (_, xw) in enumerate(cx):
        for r, (_, yh) in enumerate(cy):
            if (c, r) not in exterior:
                grid[r][c] = xw * yh

    # 2D prefix sum over weighted grid
    ps = [[0] * (CW + 1) for _ in range(CH + 1)]
    for r in range(CH):
        for c in range(CW):
            ps[r + 1][c + 1] = grid[r][c] + ps[r][c + 1] + ps[r + 1][c] - ps[r][c]

    def rect_sum(r1: int, c1: int, r2: int, c2: int) -> int:
        return ps[r2 + 1][c2 + 1] - ps[r1][c2 + 1] - ps[r2 + 1][c1] + ps[r1][c1]

    # Check every pair of red tiles as opposite rectangle corners
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            rx1, rx2 = min(x1, x2), max(x1, x2)
            ry1, ry2 = min(y1, y2), max(y1, y2)
            c1, c2 = x_to_ci[rx1], x_to_ci[rx2]
            r1, r2 = y_to_ri[ry1], y_to_ri[ry2]
            area = (rx2 - rx1 + 1) * (ry2 - ry1 + 1)
            if rect_sum(r1, c1, r2, c2) == area and area > best:
                best = area

    return best


def main() -> None:
    data = Path("input/day_09.txt").read_text()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 24


if __name__ == "__main__":
    main()
