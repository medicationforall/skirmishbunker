import cadquery as cq
from cadqueryhelper import shape
from cqterrain import roof
from skirmishbunker import Base

class Bunker(Base):
    def __init__(self):
        super().__init__()
        self.length = 100
        self.width = 100
        self.height = 75
        self.int_length = None
        self.int_width = None

        self.inset = 10
        self.angle = 0
        self.wall_width = 2

        self.wedge = None
        self.interior_rectangle = None

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

    def make(self):
        super().make()
        self.angle =roof.angle(self.inset, self.height)

        self.make_wedge()
        self.make_interior_rectangle()

        # Add example box
        box = cq.Workplane("XY").box(10,10,10).rotate((0,1,0),(0,0,0),-1*(self.angle)).translate((self.length/2,0,0))
        self.wedge = self.wedge.add(box)

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
            .cut(self.interior_rectangle)
        )
        return scene

bp = Bunker()
bp.inset=20
bp.wall_width = 2
bp.make()
rec = bp.build()

show_object(rec)
