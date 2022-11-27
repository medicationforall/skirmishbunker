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

# 150 x 75 x 75 mm

from . import Base
import cadquery as cq
from cadqueryhelper import shape, series
import math

class Bunker(Base):
    def __init__(self):
        super().__init__()
        self.length = 100
        self.width = 100
        self.height = 75
        self.wedge = None
        self.angle = 0
        self.inset = 10
        self.wall_width = 5
        self.panel_length = 28
        self.panel_width = 6
        self.panel_padding = 4

    def find_angle(self, length, height):
        '''
        Presumed length and height are part of a right triangle
        '''
        hyp = math.hypot(length, height)
        angle = length/hyp
        angle_radians = math.acos((angle))
        angle_deg = math.degrees(angle_radians)
        return angle_deg

    def make_cut_panels(self):
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        height = self.height
        inset = self.inset
        p_length = self.panel_length
        p_width = self.panel_width
        padding = self.panel_padding

        cut_panel = cq.Workplane("XY").box(p_length, p_width, height - padding)
        x_panels_size = math.floor(length / (p_length + (padding)))
        y_panels_size = math.floor(width / (p_length + (padding)))

        x_pannels_plus = (
            series(cut_panel, x_panels_size, length_offset= padding*2)
            .rotate((1,0,0),(0,0,0),(self.angle)+90)
            .translate((0,((self.width-inset+(padding/2))/2)-p_width/2,-1*(padding)))
        )

        x_pannels_minus = (
            series(cut_panel, x_panels_size, length_offset= padding*2)
            .rotate((1,0,0),(0,0,0),-1*(self.angle+90))
            .translate((0,-1*(((self.width-inset+(padding/2))/2)-p_width/2),-1*(padding)))
        )

        y_pannels_plus = (
            series(cut_panel, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((0,1,0),(0,0,0),-1*(self.angle)+90)
            .translate((((self.length-inset+(padding/2))/2)-p_width/2,0,-1*(padding)))
        )

        y_pannels_minus = (
            series(cut_panel, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((0,1,0),(0,0,0),(self.angle)+90)
            .translate((-1*(((self.length-inset+(padding/2))/2)-p_width/2),0,-1*(padding)))
        )

        return x_pannels_plus.add(x_pannels_minus).add(y_pannels_plus).add(y_pannels_minus)

    def detail_bunker(self, bunker):
        return bunker

    def make(self):
        super().make()
        interior_rectangle = (
            cq.Workplane("XY")
            .box(self.length-(2*(self.inset+self.wall_width)), self.width-(2*(self.inset+self.wall_width)), self.height-self.wall_width)
            .translate((0,0,self.wall_width/2))
        )

        self.wedge = (
            cq.Workplane("XY" )
            .wedge(self.length,self.height,self.width,self.inset,self.inset,self.length-self.inset,self.width-self.inset)
            .rotate((1,0,0),(0,0,0),-90)
        )

        #determine angle
        self.angle =self.find_angle(self.inset, self.height)

        box = cq.Workplane("XY").box(10,10,10).rotate((0,1,0),(0,0,0),-1*(self.angle)).translate((self.length/2,0,0))
        #self.wedge = self.wedge.add(box)

        self.wedge = self.wedge.cut(interior_rectangle)

        # cut panels
        cut_panels = self.make_cut_panels()
        self.wedge = self.wedge.cut(cut_panels)
        #self.wedge = self.detail_bunker(self.wedge)

    def build(self):
        super().build()
        return self.wedge
