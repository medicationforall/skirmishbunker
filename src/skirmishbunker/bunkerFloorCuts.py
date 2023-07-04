import cadquery as cq

def init_floor_cut(self):
    self.render_floor_cuts=False
    self.floor_cut_length = 28
    self.floor_cut_width = 28
    self.floor_cut_chamfer = 3

    self.floor_cut_panels = [0]

    self.floor_cuts = None

def make_floor_cuts(self):

    if self.floor_thickness:
        floor_thickness = self.floor_thickness
    else:
        floor_thickness = self.wall_width

    height = floor_thickness + self.base_height + self.floor_tile_height
    z_translate = (-1*(self.height/2)) - self.base_height + (height/2) #+ (self.floor_tile_height/2)

    floor_cut = (
        cq.Workplane("XY")
        .box(self.floor_cut_length, self.floor_cut_width, height)
        .edges("|Z")
        .chamfer(self.floor_cut_chamfer)
        .translate((0, 0, z_translate))
    )

    floor_cuts = self.make_series(
        floor_cut,
        length_offset= self.panel_length - self.floor_cut_length + self.panel_padding*2,
        x_translate = self.int_length/2 - self.floor_cut_width/2,
        y_translate = self.int_width/2 - self.floor_cut_width/2,
        z_translate=0,
        skip_list=None,
        keep_list=self.floor_cut_panels
    )

    self.floor_cuts = floor_cuts
