
import numpy as np
import re
from collections import defaultdict

class Tile:
    def __init__(self, num, tile_list):
        self.num = num
        self.data = np.array(tile_list)

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

edge_map = defaultdict(set)

if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    tile = None
    tile_lines = []
    tiles = []
    for line in lines:
        m = re.match(r"^Tile (\d+):$", line)
        if m:
            tile_num = int(m.group(1))
        elif line == "":
            #print(tile_list)
            tile = Tile(tile_num, tile_lines)
            tiles.append(tile)
            tile_lines = []
        else:
            tile_lines.append(list(line))
    if tile_lines:
        tile = Tile(tile_num, tile_lines)
        tiles.append(tile)

    print(f"Tile count: {len(tiles)}")
    for tile in tiles:
        for edge in [tile.north(), tile.south(), tile.east(), tile.west(),
                     tile.north()[::-1], tile.south()[::-1], tile.east()[::-1], tile.west()[::-1]]:
            edge_map[edge].add(tile.num)

    shared_edge_ct = defaultdict(int)
    for edge_set in edge_map.values():
        if len(edge_set) > 1:
            for edge in edge_set:
                shared_edge_ct[edge] += 1
    print(edge_map)
    print(shared_edge_ct)
    product1 = 1
    for tile in tiles:
        if shared_edge_ct[tile.num] == 4:
            product1 *= tile.num
    print(f"Answer1: {product1}")
