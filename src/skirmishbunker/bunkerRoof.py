from .Roof import Roof

def init_roof_params(self):
    self.render_roof=True
    self.roof_height = 18
    self.roof_inset = -3
    self.roof_overflow = 1
    self.roof_wall_details_inset = -0.8

    #self.render_hatches = False
    #self.hatch_panels = [8]

    self.roof_x_translate = None
    self.roof_z_translate = None

    self.roof = None
    self.roof_bp = None

def make_roof(self):
    length = self.length-(2*(self.inset-self.roof_overflow))
    width = self.width-(2*(self.inset-self.roof_overflow))

    print('roof length', length)
    print ('roof width', width)
    bp = Roof()
    bp.height = self.roof_height
    bp.length = length
    bp.width = width
    bp.inset = self.roof_inset
    bp.bunker_int_length = self.int_length
    bp.bunker_int_width = self.int_width

    bp.wall_details_inset = self.roof_wall_details_inset
    bp.render_floor_tiles = self.render_floor_tiles
    bp.render_hatches = self.render_ladders
    bp.hatch_panels = self.ladder_panels

    bp.panel_length = self.panel_length
    bp.panel_width = self.panel_width
    bp.panel_padding = self.panel_padding
    bp.make()
    self.roof_bp = bp
