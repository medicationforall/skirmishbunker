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
from cadqueryhelper import Base, series
from cqterrain import roof, tile, Ladder
from .FlatRoof import FlatRoof
from .SeriesHelper import SeriesHelper
from math import floor as math_floor

from .bunkerBody import init_body_params, make_wedge, make_interior_rectangle, make_base
from .bunkerPanels import init_bunker_params, make_cut_panels, arch_detail, make_detail_panels
from .bunkerWindows import init_window_params, make_cut_windows, make_windows
from .bunkerDoors import init_door_params, make_cut_doors, make_doors
from .bunkerRoof import init_roof_params, make_roof
from .bunkerFloor import init_floor_params, make_interior_floor
from .bunkerLadders import init_ladder_params, make_ladders
from .bunkerFloorCuts import init_floor_cut, make_floor_cuts
from .bunkerPips import init_pip_params, make_pips, make_cut_pips

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
        init_pip_params(self)

    def make_series(self, shape, length_offset, x_translate = 0, y_translate = 0, z_translate = 0, skip_list = None, keep_list = None):
        series = SeriesHelper()
        series.shape = shape
        series.outer_length = self.int_length
        series.outer_width = self.int_width
        series.length_offset = length_offset
        series.comp_length = self.panel_length
        series.comp_padding = self.panel_padding
        series.x_translate = x_translate
        series.y_translate = y_translate
        series.z_translate = z_translate
        series.skip_list = skip_list
        series.keep_list = keep_list
        series.make()

        return series.get_scene()

    def set_roof_object(self, roof):
        if not isinstance(roof, FlatRoof):
            raise Exception("Invalid roof type")

        self.roof_object = roof

    def make(self):
        super().make()
        self.angle = roof.angle(self.inset, self.height)

        # order matters
        make_wedge(self)
        make_interior_rectangle(self)

        if self.render_base:
            make_base(self)

        if self.render_cut_panels:
            # depends on make_interior_rectangle
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

        if self.render_pips:
            make_pips(self)
            make_cut_pips(self)

    def build_body(self):
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
        )

        if self.render_interior:
            scene = scene.cut(self.interior_rectangle)

        if self.render_base and self.base:
            scene = scene.union(self.base)

        if self.render_cut_panels and self.cut_panels:
            scene = scene.cut(self.cut_panels)

        if self.render_pips and self.pips:
            if self.render_magnets:
                scene = scene.cut(self.pips)
            else:
                scene = scene.union(self.pips)
            scene = scene.cut(self.cut_pips)

        if self.render_windows and self.cut_windows and self.windows:
            scene = scene.cut(self.cut_windows).union(self.windows)

        if self.render_doors and self.cut_doors and self.doors:
            scene = scene.cut(self.cut_doors).union(self.doors)

        if self.render_floor_tiles and self.interior_tiles:
            scene = scene.union(self.interior_tiles)

        if self.render_floor_cuts and self.floor_cuts:
            scene = scene.cut(self.floor_cuts)

        if self.render_ladders and self.ladders:
            scene = scene.union(self.ladders)

        if self.render_panel_details and self.panels:
            scene = scene.add(self.panels)

        return scene

    def build_roof(self, z_translate=0):
        self.roof = self.roof_bp.build().translate((0, 0, z_translate))

        if self.roof_x_translate != None and self.roof_z_translate:
            self.roof = self.roof.translate((
                self.roof_x_translate,
                0,
                self.roof_z_translate
            ))

        return self.roof

    def build(self):
        super().build()

        scene = self.build_body()

        if self.render_roof and self.roof_bp:
            scene.add(self.build_roof(z_translate = self.height/2+self.roof_bp.height/2))

        return scene

    def build_plate(self):
        x_translate = self.length

        if self.inset < 0:
            x_translate = self.length + (-1 * (self.inset * 2))
        if self.inset == 0:
            x_translate = self.length + 15

        if self.render_roof and self.roof_bp:
            self.roof_x_translate = x_translate
            self.roof_z_translate = -1 * (self.height + self.base_height)

        return self.build()
