import cadquery as cq
from cadqueryhelper import shape, series
from cqterrain import roof
from skirmishbunker import Base
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

        self.wedge = None
        self.interior_rectangle = None
        self.cut_panels = None

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

    def make_cut_panels(self):
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        height = self.height
        inset = self.inset
        p_length = self.panel_length
        p_width = self.panel_width
        padding = self.panel_padding
        p_height = height - padding

        cut_panel = (
            cq.Workplane("XY")
            .box(p_length, p_width, p_height)
            .translate((0,-1*(p_width/2),1*(p_height/2)))
            .rotate((1,0,0),(0,0,0),self.angle-90)
            .translate((0,0,-1*(height/2)))
        )
        x_panels_size = math_floor(length / (p_length + (padding)))
        y_panels_size = math_floor(width / (p_length + (padding)))

        x_panels_plus = (
            series(cut_panel, x_panels_size, length_offset= padding*2)
            .translate((0,self.width/2,0))
        )

        x_panels_minus = (
            series(cut_panel, x_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),180)
            .translate((0,-1*(self.width/2),0))
        )

        y_panels_plus = (
            series(cut_panel, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),90)
            .translate((self.length/2,0,0))
        )

        y_panels_minus = (
            series(cut_panel, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),-90)
            .translate((-1*(self.length/2),0,0))
        )

        self.cut_panels = x_panels_plus.add(y_panels_plus).add(x_panels_minus).add(y_panels_minus)

    def make(self):
        super().make()
        self.angle =roof.angle(self.inset, self.height)

        self.make_wedge()
        self.make_interior_rectangle()
        self.make_cut_panels()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
            .cut(self.interior_rectangle)
            .cut(self.cut_panels)
        )
        return scene

bp = Bunker()
bp.inset=20
bp.width=150
bp.length=120
bp.panel_width = 6
bp.panel_padding = 4
bp.make()
rec = bp.build()

show_object(rec)
