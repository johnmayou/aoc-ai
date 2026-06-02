from functools import cache

SAMPLE = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

# Bitmask: bit 0 = dac visited, bit 1 = fft visited
_DAC = 1
_FFT = 2
_FULL = _DAC | _FFT


def parse(data: str) -> dict[str, list[str]]:
    graph = {}
    for line in data.strip().splitlines():
        device, _, rest = line.partition(": ")
        graph[device] = rest.split()
    return graph


def solve(graph: dict[str, list[str]]) -> int:
    @cache
    def count_paths(node: str, mask: int) -> int:
        if node == "dac":
            mask |= _DAC
        elif node == "fft":
            mask |= _FFT
        if node == "out":
            return 1 if mask == _FULL else 0
        return sum(count_paths(child, mask) for child in graph.get(node, []))

    return count_paths("svr", 0)


def main() -> None:
    with open("input/day_11.txt") as f:
        data = f.read()
    print(solve(parse(data)))


def test_sample() -> None:
    assert solve(parse(SAMPLE)) == 2


if __name__ == "__main__":
    main()
