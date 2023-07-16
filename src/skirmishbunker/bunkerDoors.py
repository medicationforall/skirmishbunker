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
from .BlastDoor import BlastDoor

def init_door_params(self):
    self.render_doors=True
    self.door_panels = [0,3]
    self.door_length = 23
    self.door_width = 5
    self.door_height =35
    self.door_fillet = 4

    self.custom_cut_door=None
    self.custom_cut_door_padding = 0

    self.custom_door=None
    self.custom_door_padding = 0

    self.cut_doors = None
    self.doors = None

def make_cut_doors(self):
    height = self.height
    door_cut_width = self.inset+self.wall_width

    if self.floor_thickness:
        floor_thickness = self.floor_thickness
    else:
        floor_thickness = self.wall_width

    if self.inset < 0:
        door_cut_width = -1*(self.inset)+self.wall_width

    if self.custom_cut_door:
        cut_door = self.custom_cut_door(self)
    else:
        cut_door = (
            cq.Workplane("XY")
            .box(self.door_length, door_cut_width, self.door_height)
            .edges("|Y").fillet(self.door_fillet)
            .translate((
                0,
                0,
                -1 * (height / 2 - self.door_height / 2) + floor_thickness
            ))
        )


    self.cut_doors = self.make_series(
        cut_door,
        length_offset=self.panel_length - self.door_length + (self.panel_padding + self.custom_cut_door_padding)*2,
        x_translate = self.int_length/2+door_cut_width/2,
        y_translate = self.int_width/2+door_cut_width/2,
        z_translate=0, skip_list=None, keep_list=self.door_panels
    )

def make_doors(self):
    height = self.height

    if self.floor_thickness:
        floor_thickness = self.floor_thickness
    else:
        floor_thickness = self.wall_width

    if self.custom_door:
        door = self.custom_door(self)
    else:
        bp = BlastDoor()
        bp.length = self.door_length
        bp.width = self.door_width
        bp.height = self.door_height
        bp.fillet = self.door_fillet
        bp.make()
        door = bp.build().translate((
            0,
            0,
            -1 * (height / 2 - self.door_height / 2) + floor_thickness
        ))

    x_translate = self.int_length/2+self.door_width
    y_translate = self.int_width/2+self.door_width
    if self.inset <= 0:
        x_translate = self.int_length/2+(self.door_width/4)
        y_translate = self.int_width/2+(self.door_width/4)

    self.doors = self.make_series(
        door,
        length_offset=self.panel_length - self.door_length + (self.panel_padding + self.custom_door_padding) *2,
        x_translate = x_translate,
        y_translate = y_translate,
        z_translate=0, skip_list=None, keep_list=self.door_panels
    )
