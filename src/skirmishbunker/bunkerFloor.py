from cqterrain import tile
from cadqueryhelper import grid
from math import floor as math_floor

def init_floor_params(self):
    self.render_floor_tiles=True
    self.floor_padding = 20
    self.floor_tile_size = 11
    self.floor_tile_height = 1
    self.floor_chamfer_size = 2.4
    self.floor_mid_tile_size = 3.2
    self.floor_tile_padding = 1

    self.interior_tiles = None

def make_interior_floor(self):
    tile_size = self.floor_tile_size
    tile_padding = self.floor_tile_padding
    int_length = self.int_length-self.floor_padding
    int_width = self.int_width-self.floor_padding

    floor_tile = tile.octagon_with_dots(tile_size, self.floor_chamfer_size, self.floor_mid_tile_size, tile_padding, self.floor_tile_height)

    columns = math_floor(int_width/(tile_size + tile_padding))
    rows = math_floor(int_length/(tile_size + tile_padding))
    tile_grid = grid.make_grid(part=floor_tile, dim = [tile_size + tile_padding, tile_size + tile_padding], columns = columns, rows = rows)
    self.interior_tiles = tile_grid.translate((0,0,-1*((self.height/2)-self.wall_width-(tile_padding/2))))
    #self.interior_tiles = tile_grid
