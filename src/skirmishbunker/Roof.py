import cadquery as cq
from . import Base
from .Hatch import Hatch
from cadqueryhelper import series, grid
from cqterrain import roof, tile
from math import floor as math_floor

class Roof(Base):
    def __init__(self):
        super().__init__()
        self.width=150
        self.length=120
        self.height=30
        self.inset=10
        self.bunker_int_length=None
        self.bunker_int_width=None
        self.wall_width = 5
        self.angle = 0

        self.panel_padding = 2
        self.panel_length = 28
        self.panel_width = 6

        self.wall_details_inset = 3
        self.wall_details_depth = 5
        self.wall_arch_fillet = 2

        self.tile_height = 2

        self.hatch_length = 25
        self.hatch_width = 25
        self.hatch_height = 6
        self.hatch_cut_inset = 2
        self.hatch_cut_chamfer = 2
        self.hatch_panels = [0]

        self.render_floor_tiles = False
        self.render_hatches = False

        self.outline =None
        self.roof = None
        self.cut_walls = None
        self.wall_details = None
        self.roof_tiles = None
        self.cut_hatches = None
        self.hatches = None


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

    def make_series(self, shape, length_offset, x_translate=0, y_translate=0, z_translate=0, skip_list=None, keep_list=None):
        length_2 = self.length - (self.wall_width*2)
        width_2 = self.width - (self.wall_width*2)
        p_width = self.panel_width

        if self.bunker_int_length and self.bunker_int_width:
            length_2 = self.bunker_int_length
            width_2 = self.bunker_int_width

        x_panels_size = math_floor(length_2 / (self.panel_length + self.panel_padding))
        y_panels_size = math_floor(width_2 / (self.panel_length + self.panel_padding))

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

    def make_floor_tiles(self):
        tile_size = 21
        tile_padding = 2
        tile_height = self.tile_height

        int_length = self.length-(2*(self.inset+self.wall_width))
        int_width = self.width-(2*(self.inset+self.wall_width))

        tile = cq.Workplane("XY").box(tile_size, tile_size, tile_height)
        slot = cq.Workplane("XY").slot2D(tile_size,2).extrude(tile_height).rotate((0,0,1),(0,0,0),45)
        slot2 = cq.Workplane("XY").slot2D(tile_size-7,2).extrude(tile_height).rotate((0,0,1),(0,0,0),45).translate((-3,-3,0))
        slot3 = cq.Workplane("XY").slot2D(tile_size-7,2).extrude(tile_height).rotate((0,0,1),(0,0,0),45).translate((3,3,0))
        slot4 = cq.Workplane("XY").slot2D(tile_size-7-7,2).extrude(tile_height).rotate((0,0,1),(0,0,0),45).translate((-3-3,-3-3,0))
        slot5 = cq.Workplane("XY").slot2D(tile_size-7-7,2).extrude(tile_height).rotate((0,0,1),(0,0,0),45).translate((3+3,3+3,0))

        tile = tile.cut(slot).cut(slot2).cut(slot3).cut(slot4).cut(slot5)

        columns = math_floor(int_width/(tile_size + tile_padding))
        rows = math_floor(int_length/(tile_size + tile_padding))
        tile_grid = grid.make_grid(part=tile, dim = [tile_size + tile_padding, tile_size + tile_padding], columns = columns, rows = rows)

        self.roof_tiles = tile_grid.translate((0,0,-1*((self.height/2)-self.wall_width-1)))
        #self.roof_tiles = tile_grid

    def make_cut_hatches(self):
        cut_length = self.hatch_length - self.hatch_cut_inset
        cut_width = self.hatch_width - self.hatch_cut_inset
        cut_height = self.wall_width + self.tile_height

        hatch_cut = (
            cq.Workplane("XY")
            .box(cut_length,cut_width,cut_height)
            .edges("|Z").chamfer(self.hatch_cut_chamfer)
            .faces("Z").edges().chamfer(3)
            .translate((0,0,-1*(self.height/2)+cut_height/2 ))
        )

        length_offset= self.panel_length - cut_length + self.panel_padding*2
        hatch_cut_series = self.make_series(
            hatch_cut,
            length_offset,
            x_translate=(self.bunker_int_length/2)-cut_width/2,
            y_translate=(self.bunker_int_width/2)-cut_width/2,
            z_translate=0,
            skip_list=None,
            keep_list=self.hatch_panels
        )
        self.cut_hatches = hatch_cut_series

    def make_hatches(self):
        bp = Hatch()
        bp.length = self.hatch_length
        bp.width = self.hatch_width
        bp.height = self.hatch_height
        bp.make()
        hatch = (
            bp.build()
            .translate((0,0,-1*(self.height/2)+self.hatch_height/2 +self.wall_width))
        )

        length_offset= self.panel_length - bp.length + self.panel_padding*2
        hatch_series = self.make_series(
            hatch,
            length_offset,
            x_translate=(self.bunker_int_length/2)-bp.width/2,
            y_translate=(self.bunker_int_width/2)-bp.width/2,
            z_translate=0,
            skip_list=None,
            keep_list=self.hatch_panels
        )
        self.hatches = hatch_series

    def make(self):
        super().make()
        self.angle =roof.angle(self.inset, self.height)
        self.make_roof()
        self.make_wall_cuts()
        self.make_wall_details()

        if self.render_floor_tiles:
            self.make_floor_tiles()

        if self.render_hatches:
            self.make_cut_hatches()
            self.make_hatches()

    def build(self):
        super().make()
        result = (
            cq.Workplane("XY")
            .union(self.roof)
            .cut(self.cut_walls)
            .union(self.wall_details)
        )

        if self.render_floor_tiles and self.roof_tiles:
            result = result.add(self.roof_tiles)

        if self.render_hatches and self.hatches:
            result = result.cut(self.cut_hatches)
            result = result.add(self.hatches)

        return result
