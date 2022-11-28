import cadquery as cq
from cadqueryhelper import shape, series
from skirmishbunker import Base
import math

class Bunker(Base):
    def __init__(self):
        super().__init__()
        self.length = 100
        self.width = 100
        self.height = 75

        self.angle = 0
        self.inset = 10
        self.wall_width = 5
        self.panel_length = 28
        self.panel_width = 6
        self.panel_padding = 4

        self.arch_padding_top = 3
        self.arch_padding_sides = 3
        self.arch_inner_height = 6
        self.inner_arch_top = 5
        self.inner_arch_sides = 4

        self.wedge = None
        self.panels = None
        self.cut_panels = None

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

        x_panels_plus = (
            series(cut_panel, x_panels_size, length_offset= padding*2)
            .rotate((1,0,0),(0,0,0),(self.angle)+90)
            .translate((0,((self.width-inset+(padding/2))/2)-p_width/2,-1*(padding)))
        )

        x_panels_minus = (
            series(cut_panel, x_panels_size, length_offset= padding*2)
            .rotate((1,0,0),(0,0,0),-1*(self.angle+90))
            .translate((0,-1*(((self.width-inset+(padding/2))/2)-p_width/2),-1*(padding)))
        )

        y_panels_plus = (
            series(cut_panel, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((0,1,0),(0,0,0),-1*(self.angle)+90)
            .translate((((self.length-inset+(padding/2))/2)-p_width/2,0,-1*(padding)))
        )

        y_panels_minus = (
            series(cut_panel, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((0,1,0),(0,0,0),(self.angle)+90)
            .translate((-1*(((self.length-inset+(padding/2))/2)-p_width/2),0,-1*(padding)))
        )

        return x_panels_plus.add(y_panels_plus).add(x_panels_minus).add(y_panels_minus)

    def arch_detail(self):
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        height = self.height
        inset = self.inset
        p_length = self.panel_length
        p_width = self.panel_width
        padding = self.panel_padding

        panel_outline = cq.Workplane("XY").box(p_length, p_width, height - padding)
        arch = shape.arch_pointed(p_length+self.arch_padding_sides, p_width/2 , height - padding + self.arch_padding_top, ((height - padding)/2) + self.arch_inner_height).translate((0,-1*(p_width/4),0))
        inner_arch = shape.arch_pointed(p_length + self.arch_padding_sides - self.inner_arch_sides, p_width , height - padding + self.arch_padding_top - self.inner_arch_top, ((height - padding)/2) + self.arch_inner_height - self.inner_arch_sides)
        inner_inner_arch = shape.arch_pointed(p_length + self.arch_padding_sides - self.inner_arch_sides-3, p_width/2 , height - padding + self.arch_padding_top - self.inner_arch_top-3, ((height - padding)/2) + self.arch_inner_height - self.inner_arch_sides).translate((0,(p_width/4),-1.5))
        panel_back = cq.Workplane("XY").box(p_length, p_width/2, height - padding).translate((0,(p_width/4),0))
        panel_detail = cq.Workplane("XY").add(panel_back).add(arch)
        inside_arch = panel_back.cut(inner_inner_arch)
        panel = panel_outline.intersect(panel_detail).cut(inner_arch).add(inside_arch)
        return panel

    def make_detail_panels(self):
        detail_panel = self.arch_detail()
        self.panels = detail_panel

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
        log('angle' + str(self.angle))

        box = cq.Workplane("XY").box(10,10,10).rotate((0,1,0),(0,0,0),-1*(self.angle)).translate((self.length/2,0,0))
        #self.wedge = self.wedge.add(box)

        self.wedge = self.wedge.cut(interior_rectangle)

        # cut panels
        cut_panels = self.make_cut_panels()
        self.cut_panels = cut_panels

        self.wedge = self.wedge.cut(cut_panels)

        self.make_detail_panels()

    def build(self):
        super().build()

        scene = (
            cq.Workplane("XY")
            #.add(self.wedge)
            .add(self.panels)
        )
        return scene

bp = Bunker()
bp.inset=20
bp.width=150
bp.length=120
bp.make()
rec = bp.build()

show_object(rec)
