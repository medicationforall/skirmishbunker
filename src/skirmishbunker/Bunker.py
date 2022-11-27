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

class Bunker(Base):
    def __init__(self):
        super().__init__()
        self.length = 100
        self.width = 100
        self.height = 75
        self.rectangle = None
        self.wedge = None
        self.inset = 10

    def make(self):
        super().make()
        self.rectangle = cq.Workplane("XY").box(self.length, self.width, self.height)
        self.wedge = cq.Workplane("XY" ).wedge(self.length,self.height,self.width,self.inset,self.inset,self.width-self.inset,self.length-self.inset).rotate((1,0,0),(0,0,0),-90)

    def build(self):
        super().build()
        return self.wedge
