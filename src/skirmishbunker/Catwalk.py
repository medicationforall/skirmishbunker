# Copyright 2023 James Adams
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
from skirmishbunker import Base
from cadqueryhelper import shape, grid, series
import math

class Catwalk(Base):
    def __init__(self):
        super().__init__()
        self.length = 187
        self.width = 187
        self.height = 4
        self.chamfer_distance = 1

        self.interior_length = 130
        self.interior_width = 130
        self.interior_height = 2
        self.interior_overlap = 5

        self.render_magnets = True
        self.magnet_radius = 1.5
        self.magnet_height = 2
        self.magnet_padding = 1.5
        self.fit_padding = .4

        self.render_corner_walls =  True
        self.wall_height = 25
        self.wall_length = 55
        self.wall_width = 3

        self.render_floor = True
        self.floor_height = 1
        self.floor_tile_size = 12
        self.floor_tile_padding = 2

        self.platform = None
        self.cut_magnets = None
        self.corner_walls = None
        self.floor_tiles = None

    def __make_platform(self):
        platform = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.height)
            .faces("-Z").chamfer(self.height-.1)
        )
        center_cut = (
            cq.Workplane("XY")
            .box(
                self.interior_length + self.fit_padding,
                self.interior_width + self.fit_padding,
                self.height
            )
        )
        overlap = (
            cq.Workplane("XY")
            .box(
                self.interior_length + self.fit_padding ,
                self.interior_width + self.fit_padding,
                self.interior_height
            )
        )
        overlap_cut = (
            cq.Workplane("XY")
            .box(
                self.interior_length - self.interior_overlap*2,
                self.interior_width - self.interior_overlap*2,
                self.interior_height
            )
        )

        self.platform = (
            platform
            .cut(center_cut)
            .union(overlap.translate((0,0,-1*(self.height/2 - self.interior_height/2))))
            .cut(overlap_cut.translate((0,0,-1*(self.height/2 - self.interior_height/2))))
        )

    def __make_magnet_cuts(self):
        magnet = cq.Workplane("XY").cylinder(self.magnet_height, self.magnet_radius+.1)

        x_translate = self.interior_length/2-self.magnet_radius-self.magnet_padding
        y_translate = self.interior_width/2-self.magnet_radius-self.magnet_padding
        z_translate = -1*(self.height/2 - self.magnet_height/2)

        pips = (
            cq.Workplane("XY")
            .union(magnet.translate((x_translate, y_translate, z_translate)))
            .union(magnet.translate((-1*x_translate, y_translate, z_translate)))
            .union(magnet.translate((-1*x_translate, -1*y_translate, z_translate)))
            .union(magnet.translate((x_translate, -1*y_translate, z_translate)))
        )
        self.cut_magnets = pips

    def __make_corner_walls(self):
        wall = (
            cq.Workplane("XY")
            .box(
                self.wall_length,
                self.wall_width,
                self.wall_height
            )
            .faces("Z").edges("<X").chamfer(self.wall_height/2)
        )

        arch_cut = shape.arch_round(4,self.wall_width, self.wall_height-4).translate((0,0,-2))
        cut_size = math.floor(self.wall_length / (4+2))

        def arch_cut_operation(series_shape, size, i, bounding_box):

            if i ==0:
                arch_cut = shape.arch_round(4,self.wall_width, self.wall_height-12).translate((0,0,-6))
                return arch_cut
            elif i ==1:
                arch_cut = shape.arch_round(4,self.wall_width, self.wall_height-8).translate((0,0,-4))
                return arch_cut
            return series_shape

        arch_cuts = series(arch_cut, length_offset=2.7, size=cut_size, operation=arch_cut_operation)
        wall = wall.cut(arch_cuts)

        corner = (
            cq.Workplane("XY")
            .union(wall.translate((-1*(self.wall_length/2-self.wall_width/2),0,0)))
            .union(
                wall
                .translate((-1*(self.wall_length/2-self.wall_width/2),0,0))
                .rotate((0,0,1),(0,0,0),90)
            )
            .translate((
                0,#s,
                0,#-1*(self.width/2-self.wall_width/2),
                self.wall_height/2+self.height/2
            ))
        )

        x_translate = self.length/2-self.wall_width/2
        y_translate = -1*(self.width/2-self.wall_width/2)

        corners = (
            cq.Workplane("XY")
            .union(corner).translate((x_translate,y_translate,0))
            .union(corner.rotate((0,0,1),(0,0,0), 90).translate((-1*x_translate,y_translate,0)))
            .union(corner.rotate((0,0,1),(0,0,0), 180).translate((-1*x_translate,-1*y_translate,0)))
            .union(corner.rotate((0,0,1),(0,0,0), -90).translate((x_translate,-1*y_translate,0)))
        )
        self.corner_walls = corners
        #self.corner_walls = arch_cut

    def __make_floor_tiles(self):
        diamond = shape.diamond(
            self.floor_tile_size,
            self.floor_tile_size,
            self.floor_height
        ).faces("-Z").chamfer(.4)

        rows = math.floor((self.length-self.height) / (self.floor_tile_size+self.floor_tile_padding))
        colums = math.floor((self.width-self.height) / ((self.floor_tile_size+self.floor_tile_padding)/2))

        diamonds = grid.make_grid(
            diamond,
            [self.floor_tile_size+self.floor_tile_padding, (self.floor_tile_size+self.floor_tile_padding)/2],
            rows = rows+2,
            columns = colums,
            odd_col_push = [(self.floor_tile_size+self.floor_tile_padding)/2,0]
        )

        outline = (
            cq.Workplane("XY")
            .box(
                self.length-self.height,
                self.width-self.height,
                self.height/2
            )
            .translate((0,0,self.height/2))
        )

        walkway_length = self.interior_length + self.fit_padding
        walkway_width = self.interior_width + self.fit_padding
        walkway_cut = (
            cq.Workplane("XY")
            .box(
                walkway_length,
                walkway_width,
                self.height/2
            )
            .translate((0,0,self.height/2))
        )

        walway = outline.cut(walkway_cut)
        floor_tiles = diamonds.translate((
            0,
            0,
            self.floor_height/2+self.height/2
        ))

        self.floor_tiles = walway.intersect(floor_tiles).translate((0,0,-1))

        #self.floor_tiles = floor_tiles


    def make(self):
        super().make()
        self.__make_platform()

        if self.render_magnets:
            self.__make_magnet_cuts()

        if self.render_corner_walls:
            self.__make_corner_walls()

        if self.render_floor:
            self.__make_floor_tiles()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.platform)
        )

        if self.render_magnets and self.cut_magnets:
            scene = scene.cut(self.cut_magnets)

        if self.render_corner_walls and self.corner_walls:
            scene = scene.union(self.corner_walls)

        if self.render_floor and self.floor_tiles:
            scene = scene.cut(self.floor_tiles)

        return scene


#bp = Catwalk()
#bp.make()
#result = bp.build()

#show_object(result)
