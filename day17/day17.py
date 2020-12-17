
from collections import defaultdict

def count_active_neighbors(state, c):
    active_ct = 0
    # print(f"Checking for {c}")
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if (i, j, k) != (0, 0, 0):
                    c_neighbor = (c[0] + i, c[1] + j, c[2] + k)
                    # print(f"State for neighbor {c_neighbor} = {state[c_neighbor]}")
                    if state[c_neighbor] == "#":
                        active_ct += 1

    # print(c, active_ct)
    return active_ct

def get_range(state):
    min_range = [None for i in range(0, 3)]
    max_range = [None for i in range (0, 3)]
    for c in state:
        # print(f"{c} in state")
        # print("Before", min_range, max_range)
        for i in range(0, 3):
            if min_range[i] is None or c[i] < min_range[i]:
                min_range[i] = c[i]
            if max_range[i] is None or c[i] > max_range[i]:
                max_range[i] = c[i]
        # print("After", min_range, max_range)
    return min_range, max_range


def print_state(state):
    min_range, max_range = get_range(state)
    print("range_print:", min_range, max_range)
    for z in range(min_range[2]-1, max_range[2]+2):
        print(f"z={z}")
        for y in range(min_range[1]-1, max_range[1]+2):
            line = ""
            for x in range(min_range[0]-1, max_range[0]+1):
                line += state[(x,y,z)]
            print(line)

def count_active(state):
    return len([v for v in state.values() if v == "#"])

def step(state):
    new_state = state.copy()
    min_range, max_range = get_range(state)
    # print("range step:", min_range, max_range)
    for i in range(min_range[0]-1, max_range[0]+2):
        for j in range(min_range[1] - 1, max_range[1] + 2):
            for k in range(min_range[2] - 1, max_range[2] + 2):
                c = (i, j, k)
                active_ct = count_active_neighbors(state, c)
                if state[c] == "#" and (active_ct < 2 or active_ct > 3):
                    new_state[c] = "."
                if state[c] == "." and active_ct == 3:
                    new_state[c] = "#"


    return new_state

if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    state = defaultdict(lambda: ".")

    for y in range(0, len(lines)):
        line = lines[y]
        for x in range(0, len(lines[0])):
            state[(x, y, 0)] = lines[y][x]

    print_state(state)
    for n in range(0, 6):
        state = step(state)
        print(f"After {n+1} cycles:")
        # print_state(state)
        print(count_active(state))




