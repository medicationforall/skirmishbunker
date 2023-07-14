# Copyright 2022 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cqterrain import tile
from cadqueryhelper import grid
from math import floor as math_floor

def init_floor_params(self):
    self.render_floor_tiles=True
    self.floor_padding = 0
    self.floor_tile_size = 11
    self.floor_tile_height = 1
    self.floor_chamfer_size = 2.4
    self.floor_mid_tile_size = 3.2
    self.floor_tile_padding = 1

    self.custom_floor_tile = None

    self.interior_tiles = None

def make_interior_floor(self):
    tile_size = self.floor_tile_size
    tile_padding = self.floor_tile_padding
    int_length = self.int_length-self.floor_padding
    int_width = self.int_width-self.floor_padding

    if self.floor_thickness:
        floor_thickness = self.floor_thickness
    else:
        floor_thickness = self.wall_width

    if self.custom_floor_tile:
        floor_tile = self.custom_floor_tile(self)
    else:
        floor_tile = tile.octagon_with_dots_2(tile_size, self.floor_chamfer_size, self.floor_mid_tile_size, tile_padding, self.floor_tile_height)

    columns = math_floor(int_width/(tile_size + tile_padding))
    rows = math_floor(int_length/(tile_size + tile_padding))
    tile_grid = grid.make_grid(part=floor_tile, dim = [tile_size + tile_padding, tile_size + tile_padding], columns = columns, rows = rows)
    z_tile_translate = -1 * (self.height / 2 - self.floor_tile_height / 2 - floor_thickness)

    #print('z_tile_translate',z_tile_translate)
    self.interior_tiles = tile_grid.translate((0,0,z_tile_translate))
    #self.interior_tiles = tile_grid
