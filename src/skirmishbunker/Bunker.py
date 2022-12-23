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

from . import Base
import cadquery as cq
from cadqueryhelper import series
from cqterrain import roof, tile, Ladder
from math import floor as math_floor

from .bunkerBody import init_body_params, make_wedge, make_interior_rectangle, make_base
from .bunkerPanels import init_bunker_params, make_cut_panels, arch_detail, make_detail_panels
from .bunkerWindows import init_window_params, make_cut_windows, make_windows
from .bunkerDoors import init_door_params, make_cut_doors, make_doors
from .bunkerRoof import init_roof_params, make_roof
from .bunkerFloor import init_floor_params, make_interior_floor
from .bunkerLadders import init_ladder_params, make_ladders
from .bunkerFloorCuts import init_floor_cut, make_floor_cuts

class Bunker(Base):
    def __init__(self):
        super().__init__()

        init_body_params(self)
        init_bunker_params(self)
        init_window_params(self)
        init_door_params(self)
        init_roof_params(self)
        init_floor_params(self)
        init_ladder_params(self)
        init_floor_cut(self)

    def make_series(self, shape, length_offset, x_translate=0, y_translate=0, z_translate=0, skip_list=None, keep_list=None):
        length = self.int_length
        width = self.int_width
        padding = self.panel_padding
        p_width = self.panel_width

        x_panels_size = math_floor(length / (self.panel_length + self.panel_padding))
        y_panels_size = math_floor(width / (self.panel_length + self.panel_padding))

        x_shapes = series(shape, x_panels_size, length_offset=length_offset)
        y_shapes = series(shape, y_panels_size, length_offset=length_offset)

        x_plus = (
            cq.Workplane("XY").add(x_shapes)
            .translate((0, y_translate, z_translate))
        )

        x_minus = (
            cq.Workplane("XY").add(x_shapes)
            .rotate((0,0,1),(0,0,0),180)
            .translate((0, -1*y_translate, z_translate))
        )

        y_plus = (
            cq.Workplane("XY").add(y_shapes)
            .rotate((0,0,1),(0,0,0),90)
            .translate((x_translate, 0, z_translate))
        )

        y_minus = (
            cq.Workplane("XY").add(y_shapes)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((0,0,1),(0,0,0),180)
            .translate((-1*(x_translate), 0, z_translate))
        )

        scene = x_plus.add(y_plus).add(x_minus).add(y_minus)

        if skip_list and len(skip_list) > 0:
            solids = scene.solids().vals()
            scene = cq.Workplane("XY")

            for  index, solid in enumerate(solids):
                if index not in skip_list:
                    scene.add(solid)
        elif keep_list and len(keep_list) > 0:
            solids = scene.solids().vals()
            scene = cq.Workplane("XY")

            for  index, solid in enumerate(solids):
                if index in keep_list:
                    scene.add(solid)

        return scene

    def make(self):
        super().make()
        self.angle = roof.angle(self.inset, self.height)

        make_wedge(self)
        make_interior_rectangle(self)
        make_base(self)
        make_cut_panels(self)

        if self.render_panel_details:
            make_detail_panels(self)

        if self.render_windows:
            make_cut_windows(self)
            make_windows(self)

        if self.render_doors:
            make_cut_doors(self)
            make_doors(self)

        if self.render_ladders:
            make_ladders(self)

        if self.render_roof:
            make_roof(self)

        if self.render_floor_tiles:
            make_interior_floor(self)

        if self.render_floor_cuts:
            make_floor_cuts(self)

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
            .cut(self.interior_rectangle)
            .cut(self.cut_panels)
            .union(self.base)
        )

        if self.render_windows and self.cut_windows and self.windows:
            scene = scene.cut(self.cut_windows).union(self.windows)

        if self.render_doors and self.cut_doors and self.doors:
            scene = scene.cut(self.cut_doors).union(self.doors)

        if self.render_ladders and self.ladders:
            scene = scene.union(self.ladders)

        if self.render_roof and self.roof_bp:
            self.roof=self.roof_bp.build().translate((0,0, self.height/2+self.roof_bp.height/2))

            if self.roof_x_translate and self.roof_z_translate:
                self.roof = self.roof.translate((self.roof_x_translate,0,self.roof_z_translate))
            scene = scene.add(self.roof)

        if self.render_floor_tiles and self.interior_tiles:
            scene = scene.add(self.interior_tiles)

        if self.render_floor_cuts and self.floor_cuts:
            scene = scene.add(self.floor_cuts)

        if self.render_panel_details and self.panels:
            scene = scene.add(self.panels)

        return scene

    def build_plate(self):
        x_translate = self.length

        if self.inset < 0:
            x_translate = self.length+(-1*(self.inset*2))
        if self.inset == 0:
            x_translate = self.length+15

        if self.render_roof and self.roof_bp:
            self.roof_x_translate = x_translate
            self.roof_z_translate = -1*(self.height+self.base_height)
        return self.build()
