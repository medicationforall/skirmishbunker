import cadquery as cq

def init_pip_params(self):
    self.render_pips = False
    self.render_magnets = False
    self.pip_radius = 1.55
    self.pip_height = 2.1
    self.pip_padding = 1.5
    self.pips = None
    self.cut_pips = None

def make_pips(self):
    pip = cq.Workplane("XY").cylinder(self.pip_height, self.pip_radius)
    if self.render_magnets:
        pip = cq.Workplane("XY").cylinder(self.pip_height, self.pip_radius)

    x_translate = self.length/2-self.inset-self.pip_radius-self.pip_padding
    y_translate = self.width/2-self.inset-self.pip_radius-self.pip_padding
    z_translate = self.height/2+self.pip_height/2

    if self.render_magnets:
        z_translate = self.height/2-self.pip_height/2

    pips = (
        cq.Workplane("XY")
        .union(pip.translate((x_translate, y_translate, z_translate)))
        .union(pip.translate((-1*x_translate, y_translate, z_translate)))
        .union(pip.translate((-1*x_translate, -1*y_translate, z_translate)))
        .union(pip.translate((x_translate, -1*y_translate, z_translate)))

    )
    self.pips = pips

def make_cut_pips(self):
    pip = cq.Workplane("XY").cylinder(self.pip_height, self.pip_radius)

    x_translate = self.length/2-self.pip_radius-self.pip_padding
    y_translate = self.width/2-self.pip_radius-self.pip_padding
    z_translate = -1*(self.height/2 + self.base_height - self.pip_height/2)

    pips = (
        cq.Workplane("XY")
        .union(pip.translate((x_translate, y_translate, z_translate)))
        .union(pip.translate((-1*x_translate, y_translate, z_translate)))
        .union(pip.translate((-1*x_translate, -1*y_translate, z_translate)))
        .union(pip.translate((x_translate, -1*y_translate, z_translate)))
    )
    self.cut_pips = pips
