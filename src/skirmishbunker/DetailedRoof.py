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

import cadquery as cq
from .FlatRoof import FlatRoof
from cadqueryhelper import series
from cqterrain import roof
from math import floor as math_floor

class DetailedRoof(FlatRoof):
    def __init__(self):
        super().__init__()

        self.bunker_int_length = None
        self.bunker_int_width = None
        self.angle = 0

        self.wall_details_inset = 3
        self.wall_details_depth = 5
        self.wall_arch_fillet = 2

        self.hatch_cut_inset = 2
        self.hatch_cut_chamfer = 2

        self.roof_overflow = 0

        self.outline = None
        self.cut_walls = None
        self.wall_details = None

    def calc_tile_z_translate(self):
        return -1 * ((self.height / 2) - self.wall_width - 1)

    def calc_hatch_space_length(self):
        length = self.length
        length -= 2 * (self.inset + self.wall_width)
        length -= 2 * self.roof_chamfer
        return length

    def calc_hatch_space_width(self):
        width = self.width
        width -= 2 * (self.inset + self.wall_width)
        width -= 2 * self.roof_chamfer
        return width

    def calc_hatch_z_translate(self):
        return -1 * (self.height / 2) + self.hatch_height / 2 + self.wall_width

    def calc_hole_x_translate(self):
        if self.inset <= 0:
            translate = (self.length / 2)
        else:
            translate = ((self.length - (self.inset * 2)) / 2)

        translate -= (self.hole_diameter / 2)
        translate -= self.hole_inset
        return translate

    def calc_hole_y_translate(self):
        if self.inset <= 0:
            translate = (self.width / 2)
        else:
            translate = ((self.width - (self.inset * 2)) / 2)

        translate -= (self.hole_diameter / 2)
        translate -= self.hole_inset
        return translate

    def make_roof_body(self):
        self.outline = (cq.Workplane("XY" )
            .wedge(
                self.length,
                self.height,
                self.width,
                self.inset,
                self.inset,
                self.length - self.inset,
                self.width - self.inset
            ).rotate((1,0,0),(0,0,0),-90)
        )

        self.roof_body = (cq.Workplane("XY")
            .add(self.outline))

        if self.wall_width > 0:
            self.roof_body = (self.roof_body
                .faces("Z")
                .shell(-1 * self.wall_width))

    def make_wall_cuts(self):
        x_size = math_floor((self.length-self.inset*2) / 24)*24
        y_size = math_floor((self.width-self.inset*2) / 24)*24

        x_cut = cq.Workplane("XY").box(
            x_size,
            self.wall_details_depth,
            self.height
        )
        y_cut = cq.Workplane("XY").box(
            self.wall_details_depth,
            y_size,
            self.height
        )
        inset = self.wall_details_inset

        x_plus = (cq.Workplane("XY")
            .add(y_cut)
            .translate(((self.length/2 - 4/2)-inset,0,0)))
        x_minus = (cq.Workplane("XY")
            .add(y_cut)
            .rotate((0,0,1),(0,0,0),180)
            .translate((-1*(self.length/2 - 4/2)+inset,0,0)))

        y_plus = (cq.Workplane("XY")
            .add(x_cut)
            .translate((0,(self.width/2 - 4/2)-inset,0)))
        y_minus = (cq.Workplane("XY")
            .add(x_cut)
            .rotate((0,0,1),(0,0,0),180)
            .translate((0,-1*(self.width/2 - 4/2)+inset,0)))

        self.cut_walls = (x_plus
            .add(x_minus)
            .add(y_plus)
            .add(y_minus))

    def make_wall_details(self):
        detail = (cq.Workplane("XY")
            .box(20, self.wall_details_depth, self.height)
            .faces("X or -X")
            .box(4, self.wall_details_depth + 1, self.height))

        arch = (cq.Workplane("XY")
            .box(20 - self.wall_details_depth, 5, ((self.height+1) /4)*3)
            .faces("Z")
            .edges("Y")
            .fillet(self.wall_arch_fillet))

        wall_detail = detail.cut(arch)

        x_size = math_floor((self.length - self.inset * 2) / 24)
        y_size = math_floor((self.width - self.inset * 2) / 24)

        inset = self.wall_details_inset

        x_series = series(wall_detail, x_size, length_offset = 0)
        y_series = (series(wall_detail, y_size, length_offset = 0)
            .rotate((0,0,1),(0,0,0),90))

        x_plus = (cq.Workplane("XY")
            .add(y_series)
            .translate(((self.length/2 - 4/2)-inset,0,0)))
        x_minus = (cq.Workplane("XY")
            .add(y_series)
            .rotate((0,0,1),(0,0,0),180)
            .translate((-1*(self.length/2 - 4/2)+inset,0,0)))

        y_plus = (cq.Workplane("XY")
            .add(x_series)
            .translate((0,(self.width/2 - 4/2)-inset,0)))
        y_minus = (cq.Workplane("XY")
            .add(x_series)
            .rotate((0,0,1),(0,0,0),180)
            .translate((0,-1*(self.width/2 - 4/2)+inset,0)))

        self.wall_details = (x_plus
            .add(x_minus)
            .add(y_plus)
            .add(y_minus))

    def make(self):
        super().make()

        self.angle = roof.angle(self.inset, self.height)
        self.make_wall_cuts()
        self.make_wall_details()

    def build(self):
        result = super().build()

        result = (result
            .cut(self.cut_walls)
            .union(self.wall_details))

        # Re-cut holes as they will have been filled
        if self.cut_holes and self.holes:
            result = result.cut(self.holes)

        return result
