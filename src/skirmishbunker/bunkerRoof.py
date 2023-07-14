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

from .DetailedRoof import DetailedRoof

def init_roof_params(self):
    self.render_roof = True

    self.roof_height = 18
    self.roof_inset = -3
    self.roof_overflow = 1
    self.roof_wall_details_inset = -0.8

    self.roof_chamfer_faces_selector = "+Z"
    self.roof_chamfer_edges_selector = ""
    self.roof_chamfer_operation = "chamfer"

    self.roof_tile_size = 21
    self.roof_tile_padding = 2
    self.roof_tile_height = 1.5

    self.roof_x_translate = None
    self.roof_z_translate = None

    self.roof_hatch_length = 25
    self.roof_hatch_width = 25
    self.roof_hatch_radius = 11
    self.roof_hatch_height = 6

    # allow growing or shrinking of roof
    # pip/magnet holes by this multiplier
    self.roof_pip_hole_mod = 1.0

    self.roof_object = DetailedRoof()
    self.roof_body = None
    self.roof_bp = None

def make_roof(self):
    length = self.length - (2 * (self.inset - self.roof_overflow))
    width = self.width - (2 * (self.inset - self.roof_overflow))

    bp = self.roof_object
    bp.height = self.roof_height
    bp.length = length
    bp.width = width
    bp.inset = self.roof_inset
    bp.bunker_int_length = self.int_length
    bp.bunker_int_width = self.int_width

    bp.roof_chamfer = self.corner_chamfer
    bp.roof_chamfer_faces_selector = self.roof_chamfer_faces_selector
    bp.roof_chamfer_edges_selector = self.roof_chamfer_edges_selector
    bp.roof_operation = self.roof_chamfer_operation

    bp.wall_width = self.wall_width
    bp.wall_details_inset = self.roof_wall_details_inset

    bp.render_tiles = self.render_floor_tiles
    bp.tile_size = self.roof_tile_size
    bp.tile_padding = self.roof_tile_padding
    bp.tile_height = self.roof_tile_height

    bp.hatch_panels = self.ladder_panels
    bp.hatch_length = self.roof_hatch_length
    bp.hatch_width = self.roof_hatch_width
    bp.hatch_radius = self.roof_hatch_radius
    bp.hatch_height = self.roof_hatch_height

    bp.panel_length = self.panel_length
    bp.panel_padding = self.panel_padding

    if self.render_pips == True or self.render_magnets == True:
        bp.cut_holes = True
    else:
        bp.cut_holes = False

    bp.hole_diameter = (self.pip_radius * 2) * self.roof_pip_hole_mod
    bp.hole_depth = self.pip_height * self.roof_pip_hole_mod
    bp.hole_inset = self.pip_padding

    bp.roof_overflow = self.roof_overflow
    bp.make()
    self.roof_bp = bp
