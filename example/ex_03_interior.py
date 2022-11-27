import cadquery as cq
from cadqueryhelper import shape
from skirmishbunker import Base
import math

class Bunker(Base):
    def __init__(self):
        super().__init__()
        self.length = 100
        self.width = 100
        self.height = 75
        self.inset = 10
        self.angle = 0
        self.wall_width = 2
        self.wedge = None

    def find_angle(self, length, height):
        '''
        Presumed length and height are part of a right triangle
        '''
        hyp = math.hypot(length, height)
        angle = length/hyp
        angle_radians = math.acos((angle))
        angle_deg = math.degrees(angle_radians)
        return angle_deg

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

        # Add example box
        box = cq.Workplane("XY").box(10,10,10).rotate((0,1,0),(0,0,0),-1*(self.angle)).translate((self.length/2,0,0))

        self.wedge = self.wedge.cut(interior_rectangle).add(box)

    def build(self):
        super().build()
        return self.wedge

bp = Bunker()
bp.inset=20
bp.make()
rec = bp.build()

show_object(rec)
