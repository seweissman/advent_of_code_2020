from collections import deque

DIRS = ["ne", "nw", "se", "sw", "e", "w"]
REVERSE_DIRS = ["sw", "se", "nw", "ne", "w", "e"]


def reverse(dir):
    return REVERSE_DIRS[DIRS.index(dir)]

class HexTile:
    """Represents a single hexagonal tile"""
    def __init__(self, id):
        self.nw = None
        self.ne = None
        self.e = None
        self.w = None
        self.se = None
        self.sw = None
        self.color = "white"
        self.id = id

    def get_tile(self, dir):
        """Get adjacent tile in the given direction"""
        tile = self.__getattribute__(dir)
        return tile

    def set_tile(self, dir, tile):
        """Set tile in the given direction to the given tile"""
        self.__setattr__(dir, tile)
        rev_dir = reverse(dir)
        tile.__setattr__(rev_dir, self)

    def flip(self):
        """File tile color. If black tile while be white, if white tile will be black"""
        if self.color == "white":
            self.color = "black"
        else:
            self.color = "white"

    def __repr__(self):
        return f"HexTile({self.color})"

    def adj_tiles(self):
        """Return list of all adjacent tiles"""
        return [self.get_tile(dir) for dir in DIRS]


class HexGrid:
    """Represents a hexagonal grid"""
    ct = 0
    tile_list = []
    ref_tile = None
    tiles_to_set = None

    @classmethod
    def make_tile(cls):
        tile = HexTile(cls.ct)
        cls.tile_list.append(tile)
        cls.tiles_to_set.append(tile)
        cls.ct += 1
        return tile

    @classmethod
    def init(cls):
        cls.tiles_to_set = deque()
        cls.ref_tile = cls.make_tile()

    @classmethod
    def count_black(cls):
        ct = 0
        for tile in cls.tile_list:
            if tile.color == "black":
                ct += 1
        return ct

    @classmethod
    def change_grid(cls):
        # grow grid if necessary
        while True:
            do_grow = False
            for tile in cls.tile_list:
                if tile.color == "black" and None in tile.adj_tiles():
                    do_grow = True
            if do_grow:
                cls.grow_grid(1000)
            else:
                break

        # Save the current grid state in a map so we can make our changes
        # in place
        tile_color_map = {}
        for tile in cls.tile_list:
            tile_color_map[tile.id] = tile.color

        # Iterate over tiles and flip according to rules
        for tile in cls.tile_list:
            black_ct = 0
            white_ct = 0
            for adj_tile in tile.adj_tiles():
                if adj_tile is None:
                    white_ct += 1
                else:
                    if tile_color_map[adj_tile.id] == "white":
                        white_ct += 1
                    else:
                        black_ct += 1
            if tile.color == "black" and (black_ct == 0 or black_ct > 2):
                tile.flip()
            if tile.color == "white" and black_ct == 2:
                tile.flip()

    @classmethod
    def find_tile(cls, dir_str):
        """
        Given a direction string, e.g. wenwwweseeeweswwwnwwe, and a starting tile, return
        tile in the grid we are on after following the directions.
        """
        i = 0
        curr_tile = cls.ref_tile
        while i < len(dir_str):
            if dir_str[i] == "s" or dir_str[i] == "n":
                dir = dir_str[i:i + 2]
                i = i + 2
            else:
                dir = dir_str[i]
                i = i + 1
            # print(dir)
            new_tile = curr_tile.get_tile(dir)
            while new_tile is None:
                cls.grow_grid(1000)
                new_tile = curr_tile.get_tile(dir)
            assert (new_tile is not None)
            curr_tile = new_tile
        return curr_tile

    @classmethod
    def grow_grid(cls, n):
        while True:
            if n == 0:
                return
            ref_tile = cls.tiles_to_set.popleft()

            ne_tile = ref_tile.get_tile("ne")
            if not ne_tile:
                ne_tile = cls.make_tile()
                ref_tile.set_tile("ne", ne_tile)

            e_tile = ref_tile.get_tile("e")
            if not e_tile:
                e_tile = cls.make_tile()
                ref_tile.set_tile("e", e_tile)
            ne_tile.set_tile("se", e_tile)

            se_tile = ref_tile.get_tile("se")
            if not se_tile:
                se_tile = cls.make_tile()
                ref_tile.set_tile("se", se_tile)
            e_tile.set_tile("sw", se_tile)

            sw_tile = ref_tile.get_tile("sw")
            if not sw_tile:
                sw_tile = cls.make_tile()
                ref_tile.set_tile("sw", sw_tile)
            se_tile.set_tile("w", sw_tile)

            w_tile = ref_tile.get_tile("w")
            if not w_tile:
                w_tile = cls.make_tile()
                ref_tile.set_tile("w", w_tile)
            sw_tile.set_tile("nw", w_tile)

            nw_tile = ref_tile.get_tile("nw")
            if not nw_tile:
                nw_tile = cls.make_tile()
                ref_tile.set_tile("nw", nw_tile)

            w_tile.set_tile("ne", nw_tile)
            nw_tile.set_tile("e", ne_tile)
            n -= 1


if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    # We need to create one time to start. Could probably change the class to make this better.
    HexGrid.init()

    # Some sanity checks
    tile = HexGrid.find_tile("nwse")
    assert(tile == HexGrid.ref_tile)
    tile = HexGrid.find_tile("nwwswee")
    assert(tile == HexGrid.ref_tile)

    # Part 1
    for line in lines:
        i = 0
        tile = HexGrid.find_tile(line)
        tile.flip()

    print("Answer: ", HexGrid.count_black())

    # part 2

    i = 0
    while i < 100:
        HexGrid.change_grid()
        i += 1
        if i % 10 == 0:
            print(i)

    print("Day 100: ", HexGrid.count_black())

