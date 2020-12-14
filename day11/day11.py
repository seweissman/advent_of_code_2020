"""
--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?

--- Part Two ---
As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

.............
.L.L.#.#.#.#.
.............
The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?

"""

from collections import defaultdict

def count_adjacent(grid, seat):
    x, y = seat
    adjacent = [
                grid[(x-1, y-1)], grid[(x, y-1)], grid[(x+1, y-1)],
                grid[(x-1, y)], grid[(x+1, y)],
                grid[(x-1, y+1)], grid[(x, y+1)], grid[(x+1, y+1)]
                ]
    return len([c for c in adjacent if c == "#"])

def count_visible(grid, seat, range_x, range_y):
    x, y = seat
    vis_ct = 0
    # nw
    i = 1
    while x - i >= 0 and y - i >= 0:
        if grid[(x-i, y-i)] == "L":
            break
        if grid[(x-i, y-i)] == "#":
            vis_ct += 1
            break
        i += 1
    # n
    i = 1
    while y - i >= 0:
        if grid[(x, y-i)] == "L":
            break
        if grid[(x, y-i)] == "#":
            vis_ct += 1
            break
        i += 1
    # ne
    i = 1
    while y - i >= 0 and x + i < range_x:
        if grid[(x+i, y-i)] == "L":
            break
        if grid[(x+i, y-i)] == "#":
            vis_ct += 1
            break
        i += 1
    # e
    i = 1
    while x + i < range_x:
        if grid[(x+i, y)] == "L":
            break
        if grid[(x+i, y)] == "#":
            vis_ct += 1
            break
        i += 1
    # se
    i = 1
    while x + i < range_x and y + i < range_y:
        if grid[(x+i, y+i)] == "L":
            break
        if grid[(x+i, y+i)] == "#":
            vis_ct += 1
            break
        i += 1
    # s
    i = 1
    while y + i < range_y:
        if grid[(x, y+i)] == "L":
            break
        if grid[(x, y+i)] == "#":
            vis_ct += 1
            break
        i += 1
    # sw
    i = 1
    while x - i >= 0 and y + i < range_y:
        if grid[(x-i, y+i)] == "L":
            break
        if grid[(x-i, y+i)] == "#":
            vis_ct += 1
            break
        i += 1
    # w
    i = 1
    while x - i >= 0:
        if grid[(x-i, y)] == "L":
            break
        if grid[(x-i, y)] == "#":
            vis_ct += 1
            break
        i += 1
    return vis_ct

def count_occupied(grid):
    occ_ct = 0
    for c in grid:
        if grid[c] == "#":
            occ_ct += 1
    return occ_ct

def print_grid(grid, range_x, range_y):
    for y in range(0, range_y):
        grid_row = ""
        for x in range(0, range_x):
            grid_row += grid[(x,y)]
        print(grid_row)
    print("")


if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    grid = defaultdict(lambda: ".")
    range_x = len(lines[0])
    range_y = len(lines)

    # intitialize grid
    for y in range(0, range_y):
        for x in range(0, range_x):
            grid[(x,y)] = lines[y][x]
    # part 1
    old_grid = grid.copy()
    round = 0
    while True:
        new_grid = old_grid.copy()
        round += 1
        for y in range(0, range_y):
            for x in range(0, range_x):
                if old_grid[(x,y)] == "L" and count_adjacent(old_grid, (x,y)) == 0:
                    new_grid[(x,y)] = "#"
                if old_grid[(x,y)] == "#" and count_adjacent(old_grid, (x,y)) >= 4:
                    new_grid[(x,y)] = "L"
        if count_occupied(old_grid) == count_occupied(new_grid):
            print(f"Done at round {round}, with {count_occupied(old_grid)} seats")
            break
        old_grid = new_grid

    # for c in grid.keys():
    #     print(c, count_visible(grid, c, range_x, range_y))

    # part 2
    old_grid = grid.copy()
    round = 0
    while True:
        new_grid = old_grid.copy()
        # print_grid(new_grid, range_x, range_y)
        round += 1
        for y in range(0, range_y):
            for x in range(0, range_x):
                if old_grid[(x,y)] == "L" and count_visible(old_grid, (x,y), range_x, range_y) == 0:
                    new_grid[(x,y)] = "#"
                if old_grid[(x,y)] == "#" and count_visible(old_grid, (x,y), range_x, range_y) >= 5:
                    new_grid[(x,y)] = "L"
        # print(round, count_occupied(new_grid), count_occupied(old_grid))
        if count_occupied(old_grid) == count_occupied(new_grid):
            print(f"Done at round {round}, with {count_occupied(old_grid)} seats")
            break
        old_grid = new_grid

        # for c in new_grid.keys():
        #     if new_grid[c] == "#":
        #         print(c, count_visible(new_grid, c, range_x, range_y))
