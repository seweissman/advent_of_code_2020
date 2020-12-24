from collections import deque

DIRS = ["ne", "nw", "se", "sw", "e", "w"]
REVERSE_DIRS = ["sw", "se", "nw", "ne", "w", "e"]


def reverse(dir):
    return REVERSE_DIRS[DIRS.index(dir)]


class HexTile:
    ct = 0
    tile_list = []

    def __init__(self):
        self.nw = None
        self.ne = None
        self.e = None
        self.w = None
        self.se = None
        self.sw = None
        self.color = "white"
        self.id = HexTile.ct
        HexTile.ct += 1
        HexTile.tile_list.append(self)

    def get_tile(self, dir):
        tile = self.__getattribute__(dir)
        return tile

    def set_tile(self, dir, tile):
        self.__setattr__(dir, tile)
        rev_dir = reverse(dir)
        tile.__setattr__(rev_dir, self)

    def flip(self):
        if self.color == "white":
            self.color = "black"
        else:
            self.color = "white"

    def __repr__(self):
        return f"HexTile({self.color})"

    def adj_tiles(self):
        return [self.get_tile(dir) for dir in DIRS]

    @classmethod
    def count_black(cls):
        ct = 0
        for tile in cls.tile_list:
            if tile.color == "black":
                ct += 1
        return ct


def build_grid(start_tile, n):
    """
    Build a grid of n tile starting from start_tile and moving outward in
    a circle
    """
    tiles_to_set = deque([start_tile])
    while True:
        if n == 0:
            return
        ref_tile = tiles_to_set.popleft()

        ne_tile = ref_tile.get_tile("ne")
        if not ne_tile:
            ne_tile = HexTile()
            ref_tile.set_tile("ne", ne_tile)
            tiles_to_set.append(ne_tile)

        e_tile = ref_tile.get_tile("e")
        if not e_tile:
            e_tile = HexTile()
            ref_tile.set_tile("e", e_tile)
            tiles_to_set.append(e_tile)
        ne_tile.set_tile("se", e_tile)

        se_tile = ref_tile.get_tile("se")
        if not se_tile:
            se_tile = HexTile()
            ref_tile.set_tile("se", se_tile)
            tiles_to_set.append(se_tile)
        e_tile.set_tile("sw", se_tile)

        sw_tile = ref_tile.get_tile("sw")
        if not sw_tile:
            sw_tile = HexTile()
            ref_tile.set_tile("sw", sw_tile)
            tiles_to_set.append(sw_tile)
        se_tile.set_tile("w", sw_tile)

        w_tile = ref_tile.get_tile("w")
        if not w_tile:
            w_tile = HexTile()
            ref_tile.set_tile("w", w_tile)
            tiles_to_set.append(w_tile)
        sw_tile.set_tile("nw", w_tile)

        nw_tile = ref_tile.get_tile("nw")
        if not nw_tile:
            nw_tile = HexTile()
            ref_tile.set_tile("nw", nw_tile)
            tiles_to_set.append(nw_tile)

        w_tile.set_tile("ne", nw_tile)
        nw_tile.set_tile("e", ne_tile)
        n -= 1

def change_grid(tile_list):
    # Save the current grid state in a map so we can make our changes
    # in place
    tile_color_map = {}
    for tile in tile_list:
        tile_color_map[tile.id] = tile.color

    # Iterate over tiles and flip according to rules
    for tile in tile_list:
        black_ct = 0
        white_ct = 0
        for adj_tile in tile.adj_tiles():
            if adj_tile is None:
                white_ct +=1
            else:
                if tile_color_map[adj_tile.id] == "white":
                    white_ct += 1
                else:
                    black_ct += 1
        if tile.color == "black" and (black_ct == 0 or black_ct > 2):
            tile.flip()
        if tile.color == "white" and black_ct == 2:
            tile.flip()


def find_tile(ref_tile, dir_str):
    """
    Given a direction string, e.g. wenwwweseeeweswwwnwwe, and a starting tile, return
    tile in the grid we are on after following the directions.
    """
    i = 0
    curr_tile = ref_tile
    while i < len(dir_str):
        if dir_str[i] == "s" or dir_str[i] == "n":
            dir = dir_str[i:i + 2]
            i = i + 2
        else:
            dir = dir_str[i]
            i = i + 1
        #print(dir)
        new_tile = curr_tile.get_tile(dir)
        assert(new_tile is not None)
        curr_tile = new_tile
    return curr_tile


if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    ring = 0
    pos = 0
    ref_tile = HexTile()

    tile_list = deque([ref_tile])
    # After a bit of experimenting we determine that this size grid is big enough
    # to solve the puzzle. For a bigger puzzle we'd have to increase the size of the grid
    build_grid(ref_tile, 15000)

    # Some sanity checks
    tile = find_tile(ref_tile, "nwse")
    assert(tile.id == ref_tile.id)
    tile = find_tile(ref_tile, "nwwswee")
    assert(tile.id == ref_tile.id)

    # Part 1
    for line in lines:
        i = 0
        tile = find_tile(ref_tile, line)
        tile.flip()

    print("Answer: ", HexTile.count_black())

    # part 2

    i = 0
    while i < 100:
        change_grid(HexTile.tile_list)
        i += 1
        if i % 10 == 0:
            print(i)

    print("Day 100: ", HexTile.count_black())

