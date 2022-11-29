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

        self.inset = 10
        self.angle = 0

        self.wedge = None

    def make_wedge(self):
        self.wedge = (
            cq.Workplane("XY" )
            .wedge(self.length,self.height,self.width,self.inset,self.inset,self.length-self.inset,self.width-self.inset)
            .rotate((1,0,0),(0,0,0),-90)
        )

    def make(self):
        super().make()
        self.angle =roof.angle(self.inset, self.height)

        self.make_wedge()

        # Add example box
        box = cq.Workplane("XY").box(10,10,10).rotate((0,1,0),(0,0,0),-1*(self.angle)).translate((self.length/2,0,0))
        self.wedge = self.wedge.add(box)

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
        )
        return scene

bp = Bunker()
bp.inset=40
bp.make()
rec = bp.build()

log(bp.angle)

show_object(rec)
