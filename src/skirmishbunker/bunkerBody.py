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

def init_body_params(self):
    self.length = 100
    self.width = 100
    self.height = 75
    self.int_length = None
    self.int_width = None
    self.base_height = 3
    self.floor_thickness = None
    self.corner_chamfer = 0

    self.angle = 0
    self.inset = 10
    self.wall_width = 5
    self.render_interior=True
    self.render_base=True

    self.wedge = None
    self.interior_rectangle = None
    self.base = None

def make_wedge(self):
    self.wedge = (
        cq.Workplane("XY" )
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

    if self.corner_chamfer > 0:
        self.wedge = self.wedge.edges("(not >Z) and (not <Z)").chamfer(self.corner_chamfer)

def make_interior_rectangle(self):
    self.int_length = self.length - (2*(self.inset+self.wall_width))
    self.int_width = self.width - (2*(self.inset+self.wall_width))

    if self.floor_thickness:
        floor_thickness = self.floor_thickness
    else:
        floor_thickness = self.wall_width

    if self.inset < 0:
        self.int_length = self.length - (2*(self.wall_width))
        self.int_width = self.width - (2*(self.wall_width))

    self.interior_rectangle = (
        cq.Workplane("XY")
        .box(self.int_length, self.int_width, self.height - floor_thickness)
        .translate((0, 0, floor_thickness / 2))
    )

def make_base(self):
    self.base = (
        cq.Workplane("XY")
        .box(self.length, self.width, self.base_height)
        .translate((
            0,
            0,
            -1 * ((self.height / 2) + (self.base_height / 2))
        ))
    )

    if self.corner_chamfer > 0:
        self.base = self.base.edges("(not >Z) and (not <Z)").chamfer(self.corner_chamfer)
