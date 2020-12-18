
from collections import defaultdict

def adj_list_offset(n, l=None):
    """Return a generator with offsets"""
    if l is None:
        l = [[]]
    if n == 0:
        return l
    else:
        return adj_list_offset(n-1, ([i, *c] for c in l for i in [-1, 0, 1]))


def adj_list(c, l=None):
    """Return a generator with offsets"""
    if l is None:
        l = [()]
    if len(c) == 0:
        return l
    else:
        return adj_list(c[0:-1], ((c[-1] + i,) + subc for subc in l for i in [-1, 0, 1]))


def range_coord(c_min, c_max, l=None):
    """Return a generator with offsets"""
    if l is None:
        l = [()]
    if len(c_min) == 0:
        return l
    else:
        return range_coord(c_min[0:-1], c_max[0:-1], ((c_min[-1] + i,) + subc for subc in l for i in range(0, c_max[-1]-c_min[-1]+1)))


def count_active_neighbors(state, c):
    active_ct = 0
    for c_neighbor in adj_list(c):
        if c_neighbor != c:
            # print(f"State for neighbor {c_neighbor} = {state[c_neighbor]}")
            if state[c_neighbor] == "#":
                active_ct += 1

    return active_ct

def get_range(state, n):
    min_range = [None for i in range(0, n)]
    max_range = [None for i in range (0, n)]
    for c in state:
        for i in range(0, n):
            if min_range[i] is None or c[i] < min_range[i]:
                min_range[i] = c[i]
            if max_range[i] is None or c[i] > max_range[i]:
                max_range[i] = c[i]
    return min_range, max_range

def print_state(state, n):
    min_range, max_range = get_range(state, n)
    for c in range_coord(min_range[2:], max_range[2:]):
        print(f"c={c}")
        print_2d_state(state,min_range[0:2], max_range[0:2],c)

def print_2d_state(state, min_range, max_range, c=()):
    line = ["." for i in range(max_range[0] - min_range[0]+1)]
    lines = [line.copy() for i in range(max_range[1] - min_range[1]+1)]
    for d in range_coord(min_range[0:2], max_range[0:2]):
        lines[d[1]][d[0]] = state[d+c]
    print("\n".join(["".join(line) for line in lines]))

def count_active(state):
    return len([v for v in state.values() if v == "#"])

def step(state):
    seen = set()
    new_state = state.copy()
    for c in list(state.keys()).copy():
        if state[c] == "#":
            for c_adj in adj_list(c):
                if c_adj in seen:
                    continue
                seen.add(c_adj)
                active_ct = count_active_neighbors(state, c_adj)
                if state[c_adj] == "#" and (active_ct < 2 or active_ct > 3):
                    new_state[c_adj] = "."
                if state[c_adj] == "." and active_ct == 3:
                    new_state[c_adj] = "#"
    return new_state


if __name__ == "__main__":
    with open("input-test.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    state = defaultdict(lambda: ".")

    for y in range(0, len(lines)):
        line = lines[y]
        for x in range(0, len(lines[0])):
            state[(x, y, 0)] = lines[y][x]

    # print_2d_state(state, (0, 0), (2,2), c=(0,))
    print_state(state, 3)
    for n in range(0, 6):
        state = step(state)
        print(f"After {n+1} cycles:")
        print(count_active(state))

    # part 2

    state = defaultdict(lambda: ".")

    for y in range(0, len(lines)):
        line = lines[y]
        for x in range(0, len(lines[0])):
            state[(x, y, 0, 0)] = lines[y][x]

    # print_state(state, 4)

    for n in range(0, 6):
        state = step(state)
        print(f"After {n+1} cycles:")
        print(count_active(state))

    # print_state(state, 4)



