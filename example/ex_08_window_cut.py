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

        self.arch_padding_top = 3
        self.arch_padding_sides = 3
        self.arch_inner_height = 6
        self.inner_arch_top = 5
        self.inner_arch_sides = 4
        self.base_height = 3

        self.window_cut_width_padding = 2
        self.window_length = 15
        self.window_height = 20

        self.wedge = None
        self.interior_rectangle = None
        self.panels = None
        self.cut_panels = None
        self.cut_windows = None
        self.base = None

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

        cut_panel = cq.Workplane("XY").box(p_length, p_width, height - padding)
        x_panels_size = math_floor(length / (p_length + (padding)))
        y_panels_size = math_floor(width / (p_length + (padding)))

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

        self.cut_panels = x_panels_plus.add(y_panels_plus).add(x_panels_minus).add(y_panels_minus)

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
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        height = self.height
        inset = self.inset
        p_length = self.panel_length
        p_width = self.panel_width
        padding = self.panel_padding

        detail_panel = self.arch_detail()

        x_panels_size = math_floor(length / (p_length + (padding)))
        y_panels_size = math_floor(width / (p_length + (padding)))

        x_panels_plus = (
            series(detail_panel, x_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),180)
            .rotate((1,0,0),(0,0,0),(self.angle)-90)
            .translate((0,((self.width-inset+(padding/2))/2)-p_width/2,-1*(padding)))
        )

        x_panels_minus = (
            series(detail_panel, x_panels_size, length_offset= padding*2)
            .rotate((1,0,0),(0,0,0),-1*(self.angle-90))
            .translate((0,-1*(((self.width-inset+(padding/2))/2)-p_width/2),-1*(padding)))
        )

        y_panels_plus = (
            series(detail_panel, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),-90)
            .rotate((0,1,0),(0,0,0),-1*(self.angle)+90)
            .translate((((self.length-inset+(padding/2))/2)-p_width/2,0,-1*(padding)))
        )

        y_panels_minus = (
            series(detail_panel, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((0,1,0),(0,0,0),(self.angle)-90)
            .translate((-1*(((self.length-inset+(padding/2))/2)-p_width/2),0,-1*(padding)))
        )

        self.panels = x_panels_plus.add(y_panels_plus).add(x_panels_minus).add(y_panels_minus)

    def make_base(self):
        self.base = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.base_height)
            .translate((0,0,-1*((self.height/2)+(self.base_height/2))))
        )

    def make_cut_windows(self):
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        height = self.height
        inset = self.inset
        p_length = self.panel_length
        p_width = self.panel_width
        padding = self.panel_padding
        cut_width = self.wall_width + inset/2 + self.window_cut_width_padding
        length_offset = p_length - self.window_length + padding*2

        cut_window = cq.Workplane("XY").box(self.window_length, cut_width,self.window_height)
        x_panels_size = math_floor(length / (p_length + (padding)))
        y_panels_size = math_floor(width / (p_length + (padding)))

        x_win_plus = (
            series(cut_window, x_panels_size, length_offset=length_offset)
            .translate((0,((self.width-inset+(padding/2))/2)-cut_width/2, -1*(padding)))
        )

        x_win_minus = (
            series(cut_window, x_panels_size, length_offset=length_offset)
            .translate((0,-1*(((self.width-inset+(padding/2))/2)-cut_width/2), -1*(padding)))
        )

        y_win_plus = (
            series(cut_window, y_panels_size, length_offset=length_offset)
            .rotate((0,0,1),(0,0,0),90)
            .translate((((self.length-inset+(padding/2))/2)-cut_width/2,0,-1*(padding)))
        )

        y_win_minus = (
            series(cut_window, y_panels_size, length_offset=length_offset)
            .rotate((0,0,1),(0,0,0),90)
            .translate((-1*(((self.length-inset+(padding/2))/2)-cut_width/2),0,-1*(padding)))
        )

        self.cut_windows = x_win_plus.add(y_win_plus).add(x_win_minus).add(y_win_minus)

    def make(self):
        super().make()
        self.angle =roof.angle(self.inset, self.height)

        self.make_wedge()
        self.make_interior_rectangle()
        self.make_cut_panels()
        self.make_detail_panels()
        self.make_base()
        self.make_cut_windows()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
            .cut(self.interior_rectangle)
            .cut(self.cut_panels)
            .union(self.panels)
            .union(self.base)
            .cut(self.cut_windows)
        )
        return scene

bp = Bunker()
bp.inset=20
bp.width=150
bp.length=120
bp.make()
rec = bp.build()

show_object(rec)
