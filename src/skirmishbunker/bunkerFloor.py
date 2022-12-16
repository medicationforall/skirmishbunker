from cqterrain import tile
from cadqueryhelper import grid
from math import floor as math_floor

def init_floor_params(self):
    self.render_floor_tiles=True

    self.interior_tiles = None

def make_interior_floor(self):
    tile_size = 11
    tile_padding = 1
    int_length = self.int_length-20
    int_width = self.int_width-20

    floor_tile = tile.octagon_with_dots(tile_size, 2.4, 3.2, 1)

    columns = math_floor(int_width/(tile_size + tile_padding))
    rows = math_floor(int_length/(tile_size + tile_padding))
    tile_grid = grid.make_grid(part=floor_tile, dim = [tile_size + tile_padding, tile_size + tile_padding], columns = columns, rows = rows)
    self.interior_tiles = tile_grid.translate((0,0,-1*((self.height/2)-self.wall_width-.5)))
    #self.interior_tiles = tile_grid
