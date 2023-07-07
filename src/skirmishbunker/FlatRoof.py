import cadquery as cq
from skirmishbunker import Base
from cadqueryhelper import series, grid
from math import floor as math_floor

class FlatRoof(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.length = 160
        self.width = 150
        self.height = 25

        self.inset = 0
        self.wall_width = 0

        # select all edges on the positive z face
        self.roof_chamfer_faces_selector = "+Z"
        self.roof_chamfer_edges_selector = ""
        self.roof_chamfer = 10
        self.roof_operation = "chamfer" # chamfer, fillet

        # roof tiles
        self.render_tiles = False
        self.tile_size = 18
        self.tile_padding = 1
        self.tile_height = 1
        # less then -1 results in a cut
        self.tile_z_offset = -1

        #shapes
        self.roof_body = None
        self.roof_tiles = None

    def should_cut_tiles(self):
        if self.tile_z_offset < -1:
            return True
        
        return False

    def calc_final_length(self):
        return self.length - (self.inset * 2)

    def calc_final_width(self):
        return self.width - (self.inset * 2)

    def calc_final_int_length(self):
        return self.length - (2 * (self.inset + self.wall_width))

    def calc_final_int_width(self):
        return self.width - (2 * (self.inset + self.wall_width))

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

        # Not entirely sure why -1 works here...
        if cut_tiles == True:
            z_translate = self.tile_z_offset + self.height
        else:
            z_translate = self.height + self.tile_z_offset

        self.roof_tiles = tile_grid.translate((0, 0, z_translate))

    def make(self):
        super().make()

        self.inner_length = self.length - self.roof_chamfer * 2
        self.inner_width = self.width - self.roof_chamfer * 2

        self.__make_roof_body()

        if self.render_tiles:
            self.make_tiles()

    def build(self):
        super().build()
        tiles = self.render_tiles
        cut_tiles = self.should_cut_tiles()

        result = (
            cq.Workplane("XY")
            .union(self.roof_body)
        )

        if tiles and self.roof_tiles and cut_tiles == True:
            result = result.cut(self.roof_tiles)
        elif tiles and self.roof_tiles:
            result = result.add(self.roof_tiles)

        return result
