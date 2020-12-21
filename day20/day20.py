
import numpy as np
import re
from collections import defaultdict

DIRS = ["n", "e", "s", "w"]

SEA_MONSTER = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #
"""
SEA_MONSTER = SEA_MONSTER[1:]


def opposite_dir(d):
    return DIRS[(DIRS.index(d) + 2)%4]

def reverse_dir(d):
    if len(d) > 1:
        return d[0:1]
    return d + "r"

def test_opposite_dir():
    assert(opposite_dir("e") == "w")
    assert(opposite_dir("s") == "n")

class Tile:
    def __init__(self, num, tile_list):
        self.num = num
        self.data = np.array(tile_list)

    def get_edge(self, d, reversed=False):
        edge = []
        if d == "n":
            edge = self.north()
        elif d == "s":
            edge = self.south()
        elif d == "e":
            edge = self.east()
        elif d == "w":
            edge = self.west()
        if reversed:
            return edge[::-1]
        return edge

    def north(self):
        return "".join(self.data[0])

    def south(self):
        return "".join(self.data[-1])

    def west(self):
        return "".join(self.data.transpose()[0])

    def east(self):
        return "".join(self.data.transpose()[-1])

    def __repr__(self):
        return f"Tile({self.num})"

    def flip_rotate(self, from_dir, to_dir):
        d = from_dir[0:1]
        # np.rot90(a)
        # np.fliplr / np.flipud
        if from_dir[-1] == "r":
            # do a flip
            if d in ["n", "s"]:
                self.data = np.fliplr(self.data)
            else:
                self.data = np.flipud(self.data)
        from_dir = d
        i = DIRS.index(from_dir)
        while DIRS[i % 4] != to_dir:
            i += 1
            self.data = np.rot90(self.data, axes=(1,0))

def test_tile():
    """
    .#.
    ..#
    #.#
    :return:
    """
    tile = Tile(123, [[".", "#", "."], [".", ".", "#"], ["#", ".", "#"]])
    assert(tile.north() == ".#.")
    assert(tile.east() == ".##")
    assert(tile.south() == "#.#")
    assert(tile.west() == "..#")
    tile.flip_rotate("n", "e")
    assert(tile.east() == ".#.")
    assert(tile.south() == "##.")
    assert(tile.west() == "#.#")
    assert(tile.north() == "#..")


def check_monster(grid, monster_array):
    for c in monster_array:
        if c[0] >= len(grid) or c[1] >= len(grid):
            return False
        if grid[tuple(c)] == ".":
            return False
    return True

if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    tile = None
    tile_lines = []
    tiles = {}
    for line in lines:
        m = re.match(r"^Tile (\d+):$", line)
        if m:
            tile_num = int(m.group(1))
        elif line == "":
            #print(tile_list)
            tile = Tile(tile_num, tile_lines)
            tiles[tile_num] = tile
            tile_lines = []
        else:
            tile_lines.append(list(line))
    if tile_lines:
        tile = Tile(tile_num, tile_lines)
        tiles[tile_num] = tile


    edge_map = defaultdict(set)
    print(f"Tile count: {len(tiles)}")
    for tile in tiles.values():
        for edge in [tile.north(), tile.south(), tile.east(), tile.west(),
                     tile.north()[::-1], tile.south()[::-1], tile.east()[::-1], tile.west()[::-1]]:
            edge_map[edge].add(tile.num)

    shared_edge_ct = defaultdict(int)
    for edge_set in edge_map.values():
        if len(edge_set) > 1:
            for edge in edge_set:
                shared_edge_ct[edge] += 1
    # print(edge_map)
    # print(shared_edge_ct)
    product1 = 1
    for tile in tiles.values():
        if shared_edge_ct[tile.num] == 4:
            product1 *= tile.num
    print(f"Answer1: {product1}")

    # part 2
    # tile count is 144 --> 12 x 12 grid
    # x x x
    # x x x
    # x x x
    # 3 x 4 = 12 unmatched edges = 8 edge tiles
    # 12 x 4 = 48 unmatched edges = 44 edge tiles

    edge_map = defaultdict(set)
    print(f"Tile count: {len(tiles)}")
    for tile in tiles.values():
        for d in ["n", "e", "s", "w"]:
            edge = tile.get_edge(d)
            edge_reversed = edge[::-1]
            edge_map[edge].add((tile.num, d))
            edge_map[edge_reversed].add((tile.num, d+"r"))
    print(edge_map)
    edge_tiles = set()
    for edge in edge_map:
        if len(edge_map[edge]) == 1:
            for tile, dir in edge_map[edge]:
                edge_tiles.add(tile)
    print("N unmatched_edges = ", len(edge_tiles))

    shared_tile_ct = defaultdict(int)
    shared_edge_ct = defaultdict(int)
    for edge_set in edge_map.values():
        if len(edge_set) > 1:
            for tile_num, d in edge_set:
                shared_tile_ct[tile_num] += 1
                shared_edge_ct[(tile_num, d[0:1])] += 1
    # print(edge_map)
    # print(shared_edge_ct)

    corner_tiles = set()
    for tile in tiles.values():
        if shared_tile_ct[tile.num] == 4:
            corner_tiles.add(tile.num)

    print("corner tiles", corner_tiles)
    for tile_num in corner_tiles:
        for d in ["n", "e", "s", "w"]:
            if shared_edge_ct[(tile_num, d)] == 0:
                print(tile_num, d)
    # test_edge = tiles[1543].get_edge("n")
    # print(test_edge)
    # print(edge_map[edge])
    #exit(-1)

    #test data for part2
    # corner tiles {3079, 1171, 2971, 1951}
    # tile = tiles[2971]
    # tile_grid = np.zeros((3,3), int)
    # tile_grid[0][0] = 2971
    # assigned = set()
    # assigned.add(2971)

    # real data for part 2
    tile = tiles[1291]
    tile_grid = np.zeros((12, 12), int)
    tile_grid[0][0] = 1291
    assigned = set()
    assigned.add(1291)

    for y in range(0,len(tile_grid)):
        for x in range(0, len(tile_grid)):
            if tile_grid[y][x] == 0:
                continue
            #print(x,y)
            #print(tile_grid)
            tile = tiles[tile_grid[y][x]]
            for d in ["n", "e", "s", "w"]:
                edge = tile.get_edge(d)
                for (other_tile_num, other_d) in edge_map[edge]:
                    if other_tile_num not in assigned:
                        if d == "e":
                            newx = x + 1
                            newy = y
                        elif d == "w":
                            newx = x - 1
                            newy = y
                        elif d == "n":
                            newx = x
                            newy = y - 1
                        elif d == "s":
                            newx = x
                            newy = y + 1
                        if 0 <= newx < len(tile_grid) and 0 <= newy < len(tile_grid):
                            other_tile = tiles[other_tile_num]
                            from_dir = other_d[0:1]
                            to_dir = opposite_dir(d)

                            if from_dir[0:1] == "n":
                                if to_dir not in ["e", "n"]:
                                    other_d = reverse_dir(other_d)
                            if from_dir == "e":
                                if to_dir not in ["n", "e"]:
                                    other_d = reverse_dir(other_d)
                            if from_dir == "s":
                                if to_dir not in ["w", "s"]:
                                    other_d = reverse_dir(other_d)
                            if from_dir == "w":
                                if to_dir not in ["w", "s"]:
                                    other_d = reverse_dir(other_d)

                            other_tile.flip_rotate(other_d, to_dir)
                            assert(tile.get_edge(d) == other_tile.get_edge(opposite_dir(d)))
                            tile_grid[newy][newx] = other_tile_num
                            assigned.add(other_tile_num)

    print(tile_grid)
    # check tile grid
    for y in range(0, len(tile_grid)):
        for x in range(0, len(tile_grid)):
            tile = tiles[tile_grid[y,x]]
            for d in DIRS:
                if d == "e":
                    newx = x + 1
                    newy = y
                elif d == "w":
                    newx = x - 1
                    newy = y
                elif d == "n":
                    newx = x
                    newy = y - 1
                elif d == "s":
                    newx = x
                    newy = y + 1
                if 0 <= newx < len(tile_grid) and 0 <= newy < len(tile_grid):
                    other_tile = tiles[tile_grid[newy, newx]]
                    edge1 = tile.get_edge(d)
                    edge2 = other_tile.get_edge(opposite_dir(d))
                    if edge1 != edge2:
                        print(f"Error at y={y} {newy}, x={x} {newx} d={d} {tile.num} {other_tile.num}")
                        print(f"{edge1} {edge2}")


    sea_grid = None
    for y in range(0,len(tile_grid)):
        sea_grid_row = None
        for x in range(0, len(tile_grid)):
            tile = tiles[tile_grid[y][x]]
            if sea_grid_row is None:
                sea_grid_row = tile.data[1:-1,1:-1]
                continue
            sea_grid_row = np.concatenate((sea_grid_row, tile.data[1:-1,1:-1]), axis=1)
        #print("row:", sea_grid_row, "<<<")
        if sea_grid is None:
            sea_grid = sea_grid_row
            continue
        sea_grid = np.concatenate((sea_grid, sea_grid_row), axis=0)

    sea_monster_lines = SEA_MONSTER.split("\n")[:-1]
    sea_monster_coords = []
    for y in range(0, len(sea_monster_lines)):
        sea_monster_line = sea_monster_lines[y]
        for x in range(0, len(sea_monster_line)):
            if sea_monster_line[x] == "#":
                sea_monster_coords += [(y, x)]
    sea_monster_array = np.array(sea_monster_coords)

    for k in range(4):
        for op in [None, np.fliplr, np.flipud]:
            test_grid = np.rot90(sea_grid, k=k)
            if op is not None:
                test_grid = op(test_grid)
            sea_monster_count = 0
            for y in range(0,len(sea_grid)):
                for x in range(0, len(sea_grid)):
                    sea_monster_test_array = sea_monster_array + [y, x]
                    if check_monster(test_grid, sea_monster_test_array):
                        sea_monster_count += 1
            print(k, op, sea_monster_count)

    sea_monster_count = 0
    # We figured out that this is the right rotation in the last block
    test_grid = np.flipud(np.rot90(sea_grid))
    for y in range(0,len(sea_grid)):
        for x in range(0, len(sea_grid)):
            sea_monster_test_array = sea_monster_array + [y, x]
            if check_monster(test_grid, sea_monster_test_array):
                for c in sea_monster_test_array:
                    test_grid[tuple(c)] = "."
                sea_monster_count += 1
    print("Sea monster count:", sea_monster_count)
    unique, counts = np.unique(test_grid, return_counts=True)
    print(unique, counts)


"""
[[1291 1009 2389 3671 1627 3137 1601 2803 1621 1039 3373 1213]
 [2657 1153 2699 3529 2027 1741 1931 3541 3229 1747 1499 1297]
 [3931 3049 1787 1571 3271 3779 2237 3877 3163 2393 2887 1973]
 [2203 2251 1907 3257 3301 2341 3343 1637 3347 1847 2791 1021]
 [3673 1279 2381 2081 3121 3011 2309 1901 1933 2957 1583 2663]
 [2797 2423 2549 1321 3637 1109 1831 2143 3533 1093 2399 3221]
 [2861 1019 3677 1129 1249 3727 1319 1619 1489 1231 1609 2269]
 [1531 1889 3967 2087 1657 2333 2417 2687 2609 1867 1237 2099]
 [3323 3391 2719 2441 2833 3929 2953 1861 3557 3617 3067 2053]
 [2617 2467 2857 1993 2671 2161 1439 3803 3371 1949 3413 3467]
 [1559 1327 1361 3457 3697 1879 1721 3041 2039 2351 2621 2707]
 [1117 2003 3517 1187 3181 2729 3217 3001 1663 1429 1871 1543]]
"""