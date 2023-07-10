import cadquery as cq
from . import Base
from .Hatch import Hatch
from .SeriesHelper import SeriesHelper
from cadqueryhelper import series, grid
from math import floor as math_floor

class FlatRoof(Base):
    def __init__(self):
        super().__init__()

        # base parameters
        self.length = 160
        self.width = 150
        self.height = 25

        self.inset = 0
        self.wall_width = 0

        self.panel_length = 0
        self.panel_padding = 0

        # select all edges on the positive z face
        self.roof_chamfer_faces_selector = "+Z"
        self.roof_chamfer_edges_selector = ""
        self.roof_chamfer = 0
        self.roof_operation = "chamfer" # chamfer, fillet

        # roof tiles
        self.render_tiles = False
        self.tile_size = 21
        self.tile_padding = 2
        self.tile_height = 1.5
        # less then -1 results in a cut
        self.tile_z_offset = -1

        # Hatches
        self.hatch_panels = []
        self.hatch_length = 25
        self.hatch_width = 25
        self.hatch_radius = 10.5
        self.hatch_height = 6
        self.hatch_z_translate = 0

        # Pip/Magnet holes
        self.cut_holes = False
        self.hole_inset = 1.5
        self.hole_depth = 1
        self.hole_diameter = 2

        #shapes
        self.roof_body = None
        self.tiles = None
        self.hatches = None
        self.holes = None

    def should_cut_tiles(self):
        if self.tile_z_offset < -1:
            return True

        return False

    def calc_final_length(self):
        return self.length - (self.inset * 2)

    def calc_final_width(self):
        return self.width - (self.inset * 2)

    def calc_final_int_length(self):
        length = self.length
        length -= 2 * (self.inset + self.wall_width)
        length -= 2 * self.roof_chamfer
        return length

    def calc_final_int_width(self):
        width = self.width
        width -= 2 * (self.inset + self.wall_width)
        width -= 2* self.roof_chamfer
        return width

    def calc_tile_space(self):
        return self.tile_size + self.tile_padding
    
    # Calculate how far the default
    # slot translation will be (This is ~85% of
    # the tile size)
    def calc_slot_translation(self):
        return self.tile_size * 0.143
    
    # Calculate the slot radius/thickness.
    # This is ~90.5% of the tile size
    def calc_slot_radius(self):
        return self.tile_size * 0.095
    
    # Calculate the length of mid size slots.
    # This is ~66.666% of the tile size
    def calc_slot_length_md(self):
        return self.tile_size - (self.tile_size * 0.333)
    
    # Calculate the length of short size slots.
    # This is ~33.333% of the tile size
    def calc_slot_length_sm(self):
        return self.tile_size - (self.tile_size * 0.666)

    def __make_roof_body(self):
        roof_body = cq.Workplane("XY").box(
            self.calc_final_length(),
            self.calc_final_width(),
            self.height
        )

        # if no chamfer/fillet, just return the new body
        if self.roof_chamfer == 0:
            self.roof_body = roof_body
            return

        # better to kill if this condition is met otherwise it fails silently.
        if self.roof_chamfer >= self.height:
            raise Exception(f"roof_chamfer {self.roof_chamfer} >= roof height {self.height}")

        if self.roof_operation.lower() == "chamfer":
            roof_body = (
                roof_body
                .faces(self.roof_chamfer_faces_selector)
                .edges(self.roof_chamfer_edges_selector)
                .chamfer(self.roof_chamfer)
            )
        elif self.roof_operation.lower() == "fillet":
            roof_body = (
                roof_body
                .faces(self.roof_chamfer_faces_selector)
                .edges(self.roof_chamfer_edges_selector)
                .fillet(self.roof_chamfer)
            )
        else:
            raise Exception("Unrecognied roof operation")

        self.roof_body = roof_body

    def make_tiles(self):
        int_length = self.calc_final_int_length()
        int_width = self.calc_final_int_width()
        tile_space = self.calc_tile_space()
        cut_tiles = self.should_cut_tiles()
        slot_translate = self.calc_slot_translation()
        slot_radius = self.calc_slot_radius()
        slot_length_md = self.calc_slot_length_md()
        slot_length_sm = self.calc_slot_length_sm()

        tile = cq.Workplane("XY").box(
            self.tile_size,
            self.tile_size,
            self.tile_height
        )

        slot = (cq.Workplane("XY")
            .slot2D(self.tile_size, slot_radius)
            .extrude(self.tile_height * 2)
            .rotate((0, 0, 1), (0, 0, 0), 45)
            .translate((0, 0, 0 - (self.tile_height / 2))))

        slot2 = (cq.Workplane("XY")
            .slot2D(slot_length_md, slot_radius)
            .extrude(self.tile_height * 2)
            .rotate((0, 0, 1), (0, 0, 0), 45)
            .translate((0 - slot_translate, 0 - slot_translate, 0 - (self.tile_height / 2))))

        slot3 = (cq.Workplane("XY")
            .slot2D(slot_length_md, slot_radius)
            .extrude(self.tile_height * 2)
            .rotate((0, 0, 1), (0, 0, 0), 45)
            .translate((slot_translate, slot_translate, 0 - (self.tile_height / 2))))

        slot4 = (cq.Workplane("XY")
            .slot2D(slot_length_sm, slot_radius)
            .extrude(self.tile_height * 2)
            .rotate((0, 0, 1), (0, 0, 0), 45)
            .translate((0 - (slot_translate *2), 0 - (slot_translate * 2), 0 - (self.tile_height / 2))))

        slot5 = (cq.Workplane("XY")
            .slot2D(slot_length_sm, slot_radius)
            .extrude(self.tile_height * 2)
            .rotate((0, 0, 1), (0, 0, 0), 45)
            .translate((slot_translate * 2, slot_translate * 2, 0 - (self.tile_height / 2))))

        tile = (tile
                .cut(slot)
                .cut(slot2)
                .cut(slot3)
                .cut(slot4)
                .cut(slot5))

        columns = math_floor(int_width / (tile_space))
        rows = math_floor(int_length / (tile_space))
        tile_grid = grid.make_grid(
            part = tile,
            dim = [tile_space, tile_space],
            columns = columns,
            rows = rows
        )

        base_z_translate = (self.height / 2 + self.tile_height / 2)

        if cut_tiles == True:
            z_translate = self.height - base_z_translate
        else:
            z_translate = base_z_translate

        self.tiles = tile_grid.translate((0, 0, z_translate))

    def make_hatches(self):
        int_length = self.calc_final_int_length() 
        int_width = self.calc_final_int_width()
        z_translate = (self.height / 2 + self.hatch_height / 2)

        bp = Hatch()
        bp.length = self.hatch_length
        bp.width = self.hatch_width
        bp.height = self.hatch_height
        bp.hatch_radius = self.hatch_radius
        bp.make()

        hatch = bp.build()
        length_offset = self.panel_length - bp.length + self.panel_padding * 2

        series = SeriesHelper()
        series.shape = hatch
        series.outer_length = int_length
        series.outer_width = int_width
        series.length_offset = length_offset
        series.comp_length = self.panel_length
        series.comp_padding = self.panel_padding
        series.x_translate = (int_length / 2) - (bp.width / 2)
        series.y_translate = (int_width / 2) - (bp.width / 2)
        series.z_translate = z_translate
        series.keep_list = self.hatch_panels
        series.make()

        self.hatches = series.get_scene()

    def make_hole_cuts(self):
        length = self.calc_final_length()
        width = self.calc_final_width()
        radius = self.hole_diameter / 2
        height = self.hole_depth
        inset = self.hole_inset

        hole = cq.Workplane("XY").cylinder(height, radius)

        x_translate = (length / 2) - radius - inset
        y_translate = (width / 2) - radius - inset
        z_translate = -1 * (self.height / 2 - height / 2)

        holes = (
            cq.Workplane("XY")
            .union(hole.translate((x_translate, y_translate, z_translate)))
            .union(hole.translate((-1 * x_translate, y_translate, z_translate)))
            .union(hole.translate((-1 * x_translate, -1 * y_translate, z_translate)))
            .union(hole.translate((x_translate, -1 * y_translate, z_translate)))
        )
        self.holes = holes

    def make(self):
        super().make()

        self.__make_roof_body()

        if self.render_tiles:
            self.make_tiles()

        if len(self.hatch_panels) > 0:
            self.make_hatches()

        if self.cut_holes:
            self.make_hole_cuts()

    def build(self):
        super().build()

        tiles = self.render_tiles
        cut_tiles = self.should_cut_tiles()

        result = (
            cq.Workplane("XY")
            .union(self.roof_body)
        )

        if self.cut_holes and self.holes:
            result = result.cut(self.holes)
        
        if self.hatches:
            result = result.add(self.hatches)

        if tiles and self.tiles and cut_tiles == True:
            result = result.cut(self.tiles)
        elif tiles and self.tiles:
            result = result.add(self.tiles)

        return result
