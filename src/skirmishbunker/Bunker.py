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
from .BlastDoor import BlastDoor
from .Roof import Roof
import cadquery as cq
from cadqueryhelper import shape, series, grid
from cqterrain import window, roof, tile, Ladder
from math import floor as math_floor

class Bunker(Base):
    def __init__(self):
        super().__init__()
        self.length = 100
        self.width = 100
        self.height = 75
        self.int_length = None
        self.int_width = None

        self.angle = 0
        self.inset = 10
        self.wall_width = 5
        self.panel_length = 28
        self.panel_width = 6
        self.panel_padding = 4

        self.arch_padding_top = 3
        self.arch_padding_sides = 3
        self.arch_inner_height = 6
        self.inner_arch_top = 5
        self.inner_arch_sides = 4
        self.base_height = 3

        self.window_cut_width_padding = 2
        self.window_length = 15
        self.window_height = 20
        self.window_length_padding = 0

        self.window_frame_width = 2
        self.window_frame_chamfer = 1.6
        self.window_frame_chamfer_select = "<Z or >Z"
        self.skip_windows = [0]

        self.door_panels = [0,3]
        self.ladder_panels = [8]
        self.door_length = 23
        self.door_height =35
        self.door_fillet = 4

        self.roof_height = 18
        self.roof_inset = -3
        self.roof_overflow = 1
        self.roof_wall_details_inset = -0.8

        self.render_floor_tiles=True
        self.render_roof=True
        self.render_doors=True
        self.render_windows=True
        self.render_ladders=True

        self.wedge = None
        self.interior_rectangle = None
        self.panels = None
        self.cut_panels = None
        self.cut_windows = None
        self.cut_doors = None
        self.windows = None
        self.doors = None
        self.base = None
        self.roof = None
        self.interior_tiles = None
        self.ladders = None

    def make_wedge(self):
        self.wedge = (
            cq.Workplane("XY" )
            .wedge(self.length,self.height,self.width,self.inset,self.inset,self.length-self.inset,self.width-self.inset)
            .rotate((1,0,0),(0,0,0),-90)
        )

    def make_interior_rectangle(self):
        self.int_length = self.length - (2*(self.inset+self.wall_width))
        self.int_width = self.width - (2*(self.inset+self.wall_width))

        if self.inset < 0:
            self.int_length = self.length - (2*(self.wall_width))
            self.int_width = self.width - (2*(self.wall_width))

        self.interior_rectangle = (
            cq.Workplane("XY")
            .box(self.int_length, self.int_width, self.height-self.wall_width)
            .translate((0,0,self.wall_width/2))
        )

    def make_base(self):
        self.base = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.base_height)
            .translate((0,0,-1*((self.height/2)+(self.base_height/2))))
        )

    def make_series(self, shape, length_offset, x_translate=0, y_translate=0, z_translate=0, skip_list=None, keep_list=None):
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        padding = self.panel_padding
        inset = self.inset
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

    def make_cut_panels(self):
        cut_panel = cq.Workplane("XY").box(
            self.panel_length,
            self.panel_width, self.height - self.panel_padding
        )
        cut_panel = (
            cq.Workplane("XY").box(self.panel_length,self.panel_width, self.height - self.panel_padding)
            .rotate((1,0,0),(0,0,0),(self.angle)+90)
            )

        x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-self.panel_width/2
        y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-self.panel_width/2
        self.cut_panels = self.make_series(cut_panel, length_offset=self.panel_padding*2, x_translate=x_translate,y_translate=y_translate, z_translate=-1*(self.panel_padding))

    def arch_detail(self):
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        height = self.height
        inset = self.inset
        p_length = self.panel_length
        p_width = self.panel_width
        padding = self.panel_padding

        panel_outline = cq.Workplane("XY").box(p_length, p_width, height - padding)
        arch = shape.arch_pointed(p_length+self.arch_padding_sides, p_width/2 , height - padding + self.arch_padding_top, ((height - padding)/2) + self.arch_inner_height).translate((0,-1*(p_width/4),0))
        inner_arch = shape.arch_pointed(p_length + self.arch_padding_sides - self.inner_arch_sides, p_width , height - padding + self.arch_padding_top - self.inner_arch_top, ((height - padding)/2) + self.arch_inner_height - self.inner_arch_sides)
        inner_inner_arch = shape.arch_pointed(p_length + self.arch_padding_sides - self.inner_arch_sides-3, p_width/2 , height - padding + self.arch_padding_top - self.inner_arch_top-3, ((height - padding)/2) + self.arch_inner_height - self.inner_arch_sides).translate((0,(p_width/4),-1.5))
        panel_back = cq.Workplane("XY").box(p_length, p_width/2, height - padding).translate((0,(p_width/4),0))
        panel_detail = cq.Workplane("XY").add(panel_back).add(arch)
        inside_arch = panel_back.cut(inner_inner_arch)
        panel = panel_outline.intersect(panel_detail).cut(inner_arch).add(inside_arch)
        return panel

    def make_detail_panels(self):
        detail_panel = (
            self.arch_detail()
            .rotate((0,1,0),(0,0,0),180)
            .rotate((1,0,0),(0,0,0),(self.angle)+90)
        )
        x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-self.panel_width/2
        y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-self.panel_width/2

        self.panels = self.make_series(detail_panel, length_offset=self.panel_padding*2, x_translate=x_translate, y_translate=y_translate, z_translate=-1*(self.panel_padding))

    def resolve_window_skip(self):
        skip_list = [] + self.skip_windows

        if self.render_doors:
            skip_list = skip_list + self.door_panels

        if self.render_ladders:
            skip_list = skip_list + self.ladder_panels

        return skip_list

    def make_cut_windows(self):
        height = self.height
        cut_width = self.wall_width + self.inset/2 + self.window_cut_width_padding
        cut_window = (cq.Workplane("XY").box(self.window_length, cut_width,self.window_height))
        inset = self.inset
        padding = self.panel_padding
        self.cut_windows = self.make_series(
            cut_window,
            length_offset=self.panel_length - self.window_length + self.panel_padding*2,
            x_translate = ((self.length-inset+(padding/2))/2)-cut_width/2,
            y_translate = ((self.width-inset+(padding/2))/2)-cut_width/2,
            z_translate=-1*(self.panel_padding), skip_list=self.resolve_window_skip(), keep_list=None
        )

    def make_windows(self):
        height = self.height
        cut_width = self.wall_width + self.inset/2 + self.window_cut_width_padding
        frame = window.frame(self.window_length, cut_width, self.window_height, self.window_frame_width)
        frame = frame.faces("Y").edges(self.window_frame_chamfer_select).chamfer(self.window_frame_chamfer)

        inset = self.inset
        padding = self.panel_padding
        self.windows = self.make_series(
            frame,
            length_offset=self.panel_length - self.window_length + self.panel_padding*2,
            x_translate = ((self.length-inset+(padding/2))/2)-cut_width/2,
            y_translate = ((self.width-inset+(padding/2))/2)-cut_width/2,
            z_translate=-1*(self.panel_padding), skip_list=self.resolve_window_skip(), keep_list=None
        )

    def make_cut_doors(self):
        height = self.height
        cut_door = (
            cq.Workplane("XY")
            .box(self.door_length, 20, self.door_height)
            .edges("|Y").fillet(self.door_fillet)
            .translate((0,0,-1*(height/2 - self.door_height/2)+self.wall_width))
        )

        cut_width = self.wall_width + self.inset/2 + self.window_cut_width_padding
        self.cut_doors = self.make_series(
            cut_door,
            length_offset=self.panel_length - self.door_length + self.panel_padding*2,
            x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-cut_width/2,
            y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-cut_width/2,
            z_translate=0, skip_list=None, keep_list=self.door_panels
        )

    def make_doors(self):
        height = self.height
        bp = BlastDoor()
        bp.length = self.door_length
        bp.height = self.door_height
        bp.make()
        door = bp.build().translate((0,0,-1*(height/2 - self.door_height/2)+self.wall_width))

        cut_width = self.wall_width + self.inset/2 + self.window_cut_width_padding
        self.doors = self.make_series(
            door,
            length_offset=self.panel_length - self.door_length + self.panel_padding*2,
            x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-cut_width/2,
            y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-cut_width/2,
            z_translate=0, skip_list=None, keep_list=self.door_panels
        )

    def make_ladders(self):
        bp = Ladder()
        bp.length = 20
        bp.height = self.height
        bp.make()
        ladder = bp.build()

        self.ladders = self.make_series(
            ladder,
            length_offset= self.panel_length - bp.length + self.panel_padding*2,
            x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-self.inset,
            y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-self.inset,
            z_translate=0,
            skip_list=None,
            keep_list=self.ladder_panels
        )
        #self.ladders = ladder


    def make_roof(self):
        length = self.length-(2*(self.inset-self.roof_overflow))
        width = self.width-(2*(self.inset-self.roof_overflow))

        print('roof length', length)
        print ('roof width', width)
        bp = Roof()
        bp.height = self.roof_height
        bp.length = length
        bp.width = width
        bp.inset = self.roof_inset
        bp.wall_details_inset = self.roof_wall_details_inset
        bp.render_floor_tiles = self.render_floor_tiles
        bp.make()
        self.roof=bp.build().translate((0,0, self.height/2+bp.height/2))

    def make_interior_floor(self):
        tile_size = 11
        tile_padding = 1
        int_length = self.length-(2*(self.inset+self.wall_width))-20
        int_width = self.width-(2*(self.inset+self.wall_width))-20

        floor_tile = tile.octagon_with_dots(tile_size, 2.4, 3.2, 1)

        #t_height = bounds.zlen
        columns = math_floor(int_width/(tile_size + tile_padding))
        rows = math_floor(int_length/(tile_size + tile_padding))
        tile_grid = grid.make_grid(part=floor_tile, dim = [tile_size + tile_padding, tile_size + tile_padding], columns = columns, rows = rows)
        self.interior_tiles = tile_grid.translate((0,0,-1*((self.height/2)-self.wall_width-.5)))
        #self.interior_tiles = tile_grid

    def make(self):
        super().make()
        self.angle =roof.angle(self.inset, self.height)

        self.make_wedge()
        self.make_interior_rectangle()
        self.make_cut_panels()
        self.make_detail_panels()
        self.make_base()

        if self.render_windows:
            self.make_cut_windows()
            self.make_windows()

        if self.render_doors:
            self.make_cut_doors()
            self.make_doors()

        if self.render_ladders:
            self.make_ladders()

        if self.render_roof:
            self.make_roof()

        if self.render_floor_tiles:
            self.make_interior_floor()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
            .cut(self.interior_rectangle)
            .cut(self.cut_panels)
            .union(self.panels)
            .union(self.base)
        )

        if self.render_windows and self.cut_windows and self.windows:
            scene = scene.cut(self.cut_windows).union(self.windows)

        if self.render_doors and self.cut_doors and self.doors:
            scene = scene.cut(self.cut_doors).union(self.doors)

        if self.render_ladders and self.ladders:
            scene = scene.union(self.ladders)

        if self.render_roof and self.roof:
            scene = scene.add(self.roof)

        if self.render_floor_tiles and self.interior_tiles:
            scene = scene.add(self.interior_tiles)

        return scene

    def build_plate(self):
        if self.roof:
            self.roof = self.roof.translate((self.length,0,-1*(self.height+self.base_height)))
        return self.build()
