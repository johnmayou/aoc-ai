from functools import cache

SAMPLE = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""


def parse(data: str) -> dict[str, list[str]]:
    graph = {}
    for line in data.strip().splitlines():
        device, _, rest = line.partition(": ")
        graph[device] = rest.split()
    return graph


def solve(graph: dict[str, list[str]]) -> int:
    @cache
    def count_paths(node: str) -> int:
        if node == "out":
            return 1
        return sum(count_paths(child) for child in graph.get(node, []))

    return count_paths("you")


def main() -> None:
    with open("input/day_11.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 5


if __name__ == "__main__":
    main()
