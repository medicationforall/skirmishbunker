import cadquery as cq
from skirmishbunker import Base
from cadqueryhelper import series
from cqterrain import roof
from math import floor as math_floor

class Roof(Base):
    def __init__(self):
        super().__init__()
        self.width=150
        self.length=120
        self.height=30
        self.inset=10
        self.wall_width = 5
        self.angle = 0

        self.wall_details_inset = 3
        self.wall_details_depth = 5
        self.wall_arch_fillet = 2

        self.outline =None
        self.roof = None
        self.cut_walls = None
        self.wall_details = None


    def make_roof(self):
        self.outline = (
            cq.Workplane("XY" )
            .wedge(self.length,self.height,self.width,self.inset,self.inset,self.length-self.inset,self.width-self.inset)
            .rotate((1,0,0),(0,0,0),-90)
        )

        self.roof = (
            cq.Workplane("XY")
            .add(self.outline)
            .faces("Z").shell(-1*self.wall_width)
        )

    def make_wall_cuts(self):
        x_size = math_floor((self.length-self.inset*2) / 24)*24
        y_size = math_floor((self.width-self.inset*2) / 24)*24

        x_cut = cq.Workplane("XY").box(x_size,self.wall_details_depth,self.height)
        y_cut = cq.Workplane("XY").box(self.wall_details_depth, y_size,self.height)
        inset = self.wall_details_inset

        x_plus = cq.Workplane("XY").add(y_cut).translate(((self.length/2 - 4/2)-inset,0,0))
        x_minus = cq.Workplane("XY").add(y_cut).rotate((0,0,1),(0,0,0),180).translate((-1*(self.length/2 - 4/2)+inset,0,0))

        y_plus = cq.Workplane("XY").add(x_cut).translate((0,(self.width/2 - 4/2)-inset,0))
        y_minus = cq.Workplane("XY").add(x_cut).rotate((0,0,1),(0,0,0),180).translate((0,-1*(self.width/2 - 4/2)+inset,0))

        self.cut_walls = x_plus.add(x_minus).add(y_plus).add(y_minus)

    def make_wall_details(self):
        detail = cq.Workplane("XY").box(20,self.wall_details_depth,self.height).faces("X or -X").box(4, self.wall_details_depth+1, self.height)
        arch = cq.Workplane("XY").box(20-self.wall_details_depth,5,((self.height+1) /4)*3).faces("Z").edges("Y").fillet(self.wall_arch_fillet)
        wall_detail = detail.cut(arch)#.rotate((1,0,0),(0,0,0),self.angle-90)
        x_size = math_floor((self.length-self.inset*2) / 24)
        y_size = math_floor((self.width-self.inset*2) / 24)

        inset = self.wall_details_inset

        x_series = series(wall_detail, x_size, length_offset=0)
        y_series = series(wall_detail, y_size, length_offset=0).rotate((0,0,1),(0,0,0),90)

        x_plus = cq.Workplane("XY").add(y_series).translate(((self.length/2 - 4/2)-inset,0,0))
        x_minus = cq.Workplane("XY").add(y_series).rotate((0,0,1),(0,0,0),180).translate((-1*(self.length/2 - 4/2)+inset,0,0))

        y_plus = cq.Workplane("XY").add(x_series).translate((0,(self.width/2 - 4/2)-inset,0))
        y_minus = cq.Workplane("XY").add(x_series).rotate((0,0,1),(0,0,0),180).translate((0,-1*(self.width/2 - 4/2)+inset,0))

        #self.wall_details = wall_detail
        self.wall_details = x_plus.add(x_minus).add(y_plus).add(y_minus)

    def make(self):
        super().make()
        self.angle =roof.angle(self.inset, self.height)
        self.make_roof()
        self.make_wall_cuts()
        self.make_wall_details()

    def build(self):
        super().make()
        result = (
            cq.Workplane("XY")
            .union(self.roof)
            .cut(self.cut_walls)
            .union(self.wall_details)
        )
        return result

bp = Roof()
bp.height = 20
bp.inset = 2
bp.wall_details_inset = 1.5
bp.make()
roof = bp.build()

show_object(roof)
