import cadquery as cq
from cadqueryhelper import shape, series
from cqterrain import window, roof
from skirmishbunker import Base, BlastDoor
from math import floor as math_floor

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
        self.base_height = 3

        self.window_cut_width_padding = 2
        self.window_length = 15
        self.window_height = 20
        self.window_length_padding = 0

        self.window_frame_width = 2
        self.window_frame_chamfer = 1.6
        self.window_frame_chamfer_select = "<Z or >Z"
        self.skip_windows = [0]

        self.door_panels = [0,3]
        self.door_length = 23
        self.door_height =35
        self.door_fillet = 4

        self.wedge = None
        self.interior_rectangle = None
        self.panels = None
        self.cut_panels = None
        self.cut_windows = None
        self.cut_doors = None
        self.windows = None
        self.doors = None
        self.base = None

    def make_wedge(self):
        self.wedge = (
            cq.Workplane("XY" )
            .wedge(self.length,self.height,self.width,self.inset,self.inset,self.length-self.inset,self.width-self.inset)
            .rotate((1,0,0),(0,0,0),-90)
        )

    def make_interior_rectangle(self):
        self.interior_rectangle = (
            cq.Workplane("XY")
            .box(self.length-(2*(self.inset+self.wall_width)), self.width-(2*(self.inset+self.wall_width)), self.height-self.wall_width)
            .translate((0,0,self.wall_width/2))
        )

    def make_base(self):
        self.base = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.base_height)
            .translate((0,0,-1*((self.height/2)+(self.base_height/2))))
        )

    def make_series(self, shape, length_offset, x_translate=0, y_translate=0, z_translate=0, skip_list=None, keep_list=None):
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        padding = self.panel_padding
        inset = self.inset
        p_width = self.panel_width

        x_panels_size = math_floor(length / (self.panel_length + self.panel_padding))
        y_panels_size = math_floor(width / (self.panel_length + self.panel_padding))

        x_shapes = series(shape, x_panels_size, length_offset=length_offset)
        y_shapes = series(shape, y_panels_size, length_offset=length_offset)

        x_plus = (
            cq.Workplane("XY").add(x_shapes)
            .translate((0, y_translate, z_translate))
        )

        x_minus = (
            cq.Workplane("XY").add(x_shapes)
            .rotate((0,0,1),(0,0,0),180)
            .translate((0, -1*y_translate, z_translate))
        )

        y_plus = (
            cq.Workplane("XY").add(y_shapes)
            .rotate((0,0,1),(0,0,0),90)
            .translate((x_translate, 0, z_translate))
        )

        y_minus = (
            cq.Workplane("XY").add(y_shapes)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((0,0,1),(0,0,0),180)
            .translate((-1*(x_translate), 0, z_translate))
        )

        scene = x_plus.add(y_plus).add(x_minus).add(y_minus)

        if skip_list and len(skip_list) > 0:
            solids = scene.solids().vals()
            scene = cq.Workplane("XY")

            for  index, solid in enumerate(solids):
                if index not in skip_list:
                    scene.add(solid)
        elif keep_list and len(keep_list) > 0:
            solids = scene.solids().vals()
            scene = cq.Workplane("XY")

            for  index, solid in enumerate(solids):
                if index in keep_list:
                    scene.add(solid)

        return scene

    def make_cut_panels(self):
        cut_panel = cq.Workplane("XY").box(
            self.panel_length,
            self.panel_width, self.height - self.panel_padding
        )
        cut_panel = (
            cq.Workplane("XY").box(self.panel_length,self.panel_width, self.height - self.panel_padding)
            .rotate((1,0,0),(0,0,0),(self.angle)+90)
            )

        x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-self.panel_width/2
        y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-self.panel_width/2
        self.cut_panels = self.make_series(cut_panel, length_offset=self.panel_padding*2, x_translate=x_translate,y_translate=y_translate, z_translate=-1*(self.panel_padding))

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
        detail_panel = (
            self.arch_detail()
            .rotate((0,1,0),(0,0,0),180)
            .rotate((1,0,0),(0,0,0),(self.angle)+90)
        )
        x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-self.panel_width/2
        y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-self.panel_width/2

        self.panels = self.make_series(detail_panel, length_offset=self.panel_padding*2, x_translate=x_translate, y_translate=y_translate, z_translate=-1*(self.panel_padding))

    def make_cut_windows(self):
        height = self.height
        cut_width = self.wall_width + self.inset/2 + self.window_cut_width_padding
        cut_window = (cq.Workplane("XY").box(self.window_length, cut_width,self.window_height))
        inset = self.inset
        padding = self.panel_padding
        self.cut_windows = self.make_series(
            cut_window,
            length_offset=self.panel_length - self.window_length + self.panel_padding*2,
            x_translate = ((self.length-inset+(padding/2))/2)-cut_width/2,
            y_translate = ((self.width-inset+(padding/2))/2)-cut_width/2,
            z_translate=-1*(self.panel_padding), skip_list=self.skip_windows + self.door_panels, keep_list=None
        )

    def make_windows(self):
        height = self.height
        cut_width = self.wall_width + self.inset/2 + self.window_cut_width_padding
        frame = window.frame(self.window_length, cut_width, self.window_height, self.window_frame_width)
        frame = frame.faces("Y").edges(self.window_frame_chamfer_select).chamfer(self.window_frame_chamfer)

        inset = self.inset
        padding = self.panel_padding
        self.windows = self.make_series(
            frame,
            length_offset=self.panel_length - self.window_length + self.panel_padding*2,
            x_translate = ((self.length-inset+(padding/2))/2)-cut_width/2,
            y_translate = ((self.width-inset+(padding/2))/2)-cut_width/2,
            z_translate=-1*(self.panel_padding), skip_list=self.skip_windows + self.door_panels, keep_list=None
        )

    def make_cut_doors(self):
        height = self.height
        cut_door = (
            cq.Workplane("XY")
            .box(self.door_length, 20, self.door_height)
            .edges("|Y").fillet(self.door_fillet)
            .translate((0,0,-1*(height/2 - self.door_height/2)+self.wall_width))
        )

        cut_width = self.wall_width + self.inset/2 + self.window_cut_width_padding
        self.cut_doors = self.make_series(
            cut_door,
            length_offset=self.panel_length - self.door_length + self.panel_padding*2,
            x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-cut_width/2,
            y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-cut_width/2,
            z_translate=0, skip_list=None, keep_list=self.door_panels
        )

    def make_doors(self):
        height = self.height
        bp = BlastDoor()
        bp.length = self.door_length
        bp.height = self.door_height
        bp.make()
        door = bp.build().translate((0,0,-1*(height/2 - self.door_height/2)+self.wall_width))

        cut_width = self.wall_width + self.inset/2 + self.window_cut_width_padding
        self.doors = self.make_series(
            door,
            length_offset=self.panel_length - self.door_length + self.panel_padding*2,
            x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-cut_width/2,
            y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-cut_width/2,
            z_translate=0, skip_list=None, keep_list=self.door_panels
        )

    def make(self):
        super().make()
        self.angle =roof.angle(self.inset, self.height)

        self.make_wedge()
        self.make_interior_rectangle()
        self.make_cut_panels()
        self.make_detail_panels()
        self.make_base()
        self.make_cut_windows()
        self.make_windows()
        self.make_cut_doors()
        self.make_doors()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
            .cut(self.interior_rectangle)
            .cut(self.cut_panels)
            .union(self.panels)
            .cut(self.cut_doors)
            .union(self.doors)
            .cut(self.cut_windows)
            .union(self.windows)
            .union(self.base)
        )
        return scene

bp = Bunker()
bp.inset=20
bp.width=150
bp.length=120
bp.height=72
bp.window_length = 18
bp.window_height = 8
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"
bp.make()
rec = bp.build()

show_object(rec)

#mini = cq.Workplane("XY").cylinder(32, 12.5).translate((0,89,-1*((75/2))+(32/2)-1.5))
#show_object(mini)