from .Roof import Roof

def init_roof_params(self):
    self.render_roof=True
    self.roof_height = 18
    self.roof_inset = -3
    self.roof_overflow = 1
    self.roof_wall_details_inset = -0.8

    self.roof = None

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
    bp.wall_details_inset = self.roof_wall_details_inset
    bp.render_floor_tiles = self.render_floor_tiles
    bp.make()
    self.roof=bp.build().translate((0,0, self.height/2+bp.height/2))
