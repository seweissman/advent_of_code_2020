"""Version 2 of day 24 using offset coords instead of tile/grid objects"""

from collections import defaultdict


def change_tile(old_color_map, new_color_map, tile):
    black_ct = 0
    white_ct = 0
    for adj_tile in adj_tiles(tile):
        if old_color_map[adj_tile] == "white":
            white_ct += 1
        else:
            black_ct += 1
    if old_color_map[tile] == "black" and (black_ct == 0 or black_ct > 2):
        new_color_map[tile] = "white"
    if old_color_map[tile] == "white" and black_ct == 2:
        new_color_map[tile] = "black"


def change_grid(color_map):
    new_color_map = color_map.copy()
    for tile in list(color_map.keys()):
        if color_map[tile] == "black":
            for other_tile in adj_tiles(tile):
                change_tile(color_map, new_color_map, other_tile)
            change_tile(color_map, new_color_map, tile)
    return new_color_map


def find_tile(dir_str):
    """
    Given a direction string, e.g. wenwwweseeeweswwwnwwe, and a starting tile, return
    tile in the grid we are on after following the directions.
      nw  ne
    w   x   e
      sw  se

    We use an offset/zigzag coordinate system like follows, positions in the same y column
    are highlighted with parens:
     -1,2  (0,2)   1,2
        (0,1)   1,1
    -1,0   (0,0)   1,0
        (0,-1)  1,-1
    -1,-2  (0,-2)  1,-2

    """
    x = y = 0
    i = 0
    while i < len(dir_str):
        # Get next dir from string
        if dir_str[i] == "s" or dir_str[i] == "n":
            dir = dir_str[i:i + 2]
            i = i + 2
        else:
            dir = dir_str[i]
            i = i + 1
        if dir == "nw":
            if y % 2 == 1:
                x -= 1
            y += 1
        elif dir == "sw":
            if y % 2 == 1:
                x -= 1
            y -= 1
        elif dir == "e":
            x += 1
        elif dir == "w":
            x -= 1
        elif dir == "ne":
            if y % 2 == 0:
                x += 1
            y += 1
        elif dir == "se":
            if y % 2 == 0:
                x += 1
            y -= 1
    return (x, y)


def adj_tiles(tile):
    x, y = tile
    if y % 2 == 1:
        return [(x-1, y+1), (x-1, y-1), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    else:
        return [(x, y+1), (x, y-1), (x+1, y), (x-1, y), (x+1, y+1), (x+1, y-1)]


def count_black(color_map):
    return len([color for color in color_map.values() if color == "black"])


if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    tile = find_tile("nwse")
    assert(tile == (0, 0))
    tile = find_tile("nwwswee")
    assert(tile == (0, 0))

    # Part 1
    color_map = defaultdict(lambda: "white")
    for line in lines:
        tile = find_tile(line)
        if color_map[tile] == "white":
            color_map[tile] = "black"
        else:
            color_map[tile] = "white"

    print("Answer: ", count_black(color_map))

    # part 2

    i = 0
    while i < 100:
        color_map = change_grid(color_map)
        i += 1

    print("Day 100: ", count_black(color_map))

