import cadquery as cq
from .FlatRoof import FlatRoof
from cadqueryhelper import series
from cqterrain import roof
from math import floor as math_floor

class DetailedRoof(FlatRoof):
    def __init__(self):
        super().__init__()

        self.bunker_int_length=None
        self.bunker_int_width=None
        self.angle = 0

        self.wall_details_inset = 3
        self.wall_details_depth = 5
        self.wall_arch_fillet = 2

        self.hatch_cut_inset = 2
        self.hatch_cut_chamfer = 2

        self.roof_overflow = 0

        self.outline = None
        self.roof_body = None
        self.cut_walls = None
        self.wall_details = None
        self.roof_tiles = None
        self.cut_hatches = None
        self.hatches = None
        self.cut_pips = None

    def calc_tile_space_length(self):
        return self.calc_final_int_length()

    def calc_tile_space_width(self):
        return self.calc_final_int_width()

    def calc_tile_z_translate(self):
        return -1 * ((self.height / 2) - self.wall_width - 1)

    def calc_hatch_z_translate(self):
        return -1 * (self.height / 2) + self.hatch_height / 2 + self.wall_width

    def make_roof_body(self):
        self.outline = (cq.Workplane("XY" )
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

        self.roof_body = (cq.Workplane("XY")
            .add(self.outline))
    
        if self.wall_width > 0:
            self.roof_body = (self.roof_body
                .faces("Z")
                .shell(-1 * self.wall_width))

    def make_wall_cuts(self):
        x_size = math_floor((self.length-self.inset*2) / 24)*24
        y_size = math_floor((self.width-self.inset*2) / 24)*24

        x_cut = cq.Workplane("XY").box(
            x_size,
            self.wall_details_depth,
            self.height
        )
        y_cut = cq.Workplane("XY").box(
            self.wall_details_depth,
            y_size,
            self.height
        )
        inset = self.wall_details_inset

        x_plus = (cq.Workplane("XY")
            .add(y_cut)
            .translate(((self.length/2 - 4/2)-inset,0,0)))
        x_minus = (cq.Workplane("XY")
            .add(y_cut)
            .rotate((0,0,1),(0,0,0),180)
            .translate((-1*(self.length/2 - 4/2)+inset,0,0)))

        y_plus = (cq.Workplane("XY")
            .add(x_cut)
            .translate((0,(self.width/2 - 4/2)-inset,0)))
        y_minus = (cq.Workplane("XY")
            .add(x_cut)
            .rotate((0,0,1),(0,0,0),180)
            .translate((0,-1*(self.width/2 - 4/2)+inset,0)))

        self.cut_walls = (x_plus
            .add(x_minus)
            .add(y_plus)
            .add(y_minus))

    def make_wall_details(self):
        detail = (cq.Workplane("XY")
            .box(20, self.wall_details_depth, self.height)
            .faces("X or -X")
            .box(4, self.wall_details_depth + 1, self.height))

        arch = (cq.Workplane("XY")
            .box(20 - self.wall_details_depth, 5, ((self.height+1) /4)*3)
            .faces("Z")
            .edges("Y")
            .fillet(self.wall_arch_fillet))

        wall_detail = detail.cut(arch)

        x_size = math_floor((self.length - self.inset * 2) / 24)
        y_size = math_floor((self.width - self.inset * 2) / 24)

        inset = self.wall_details_inset

        x_series = series(wall_detail, x_size, length_offset = 0)
        y_series = (series(wall_detail, y_size, length_offset = 0)
            .rotate((0,0,1),(0,0,0),90))

        x_plus = (cq.Workplane("XY")
            .add(y_series)
            .translate(((self.length/2 - 4/2)-inset,0,0)))
        x_minus = (cq.Workplane("XY")
            .add(y_series)
            .rotate((0,0,1),(0,0,0),180)
            .translate((-1*(self.length/2 - 4/2)+inset,0,0)))

        y_plus = (cq.Workplane("XY")
            .add(x_series)
            .translate((0,(self.width/2 - 4/2)-inset,0)))
        y_minus = (cq.Workplane("XY")
            .add(x_series)
            .rotate((0,0,1),(0,0,0),180)
            .translate((0,-1*(self.width/2 - 4/2)+inset,0)))

        self.wall_details = (x_plus
            .add(x_minus)
            .add(y_plus)
            .add(y_minus))

    def make(self):
        super().make()

        self.angle = roof.angle(self.inset, self.height)
        self.make_wall_cuts()
        self.make_wall_details()

    def build(self):
        result = super().build()

        result = (result
            .cut(self.cut_walls)
            .union(self.wall_details))
        
        # Re-cut holes as they will have been filled
        if self.cut_holes and self.holes:
            result = result.cut(self.holes)

        return result
