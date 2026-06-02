SAMPLE = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


def parse(data: str) -> list[tuple[int, int, int]]:
    boxes = []
    for line in data.strip().splitlines():
        x, y, z = line.split(",")
        boxes.append((int(x), int(y), int(z)))
    return boxes


def _dist2(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def _find(parent: list[int], x: int) -> int:
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def _union(parent: list[int], rank: list[int], x: int, y: int) -> bool:
    px, py = _find(parent, x), _find(parent, y)
    if px == py:
        return False
    if rank[px] < rank[py]:
        px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]:
        rank[px] += 1
    return True


def solve(boxes: list[tuple[int, int, int]]) -> int:
    k = len(boxes)
    pairs = sorted(
        ((i, j) for i in range(k) for j in range(i + 1, k)),
        key=lambda p: _dist2(boxes[p[0]], boxes[p[1]]),
    )

    parent = list(range(k))
    rank = [0] * k
    components = k

    for i, j in pairs:
        if _union(parent, rank, i, j):
            components -= 1
            if components == 1:
                return boxes[i][0] * boxes[j][0]

    raise ValueError("could not form a single circuit")


def main() -> None:
    with open("input/day_08.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 25272


if __name__ == "__main__":
    main()
