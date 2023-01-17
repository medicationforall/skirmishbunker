import cadquery as cq

def init_body_params(self):
    self.length = 100
    self.width = 100
    self.height = 75
    self.int_length = None
    self.int_width = None
    self.base_height = 3

    self.angle = 0
    self.inset = 10
    self.wall_width = 5
    self.render_interior=True
    self.render_base=True

    self.wedge = None
    self.interior_rectangle = None
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

def make_base(self):
    self.base = (
        cq.Workplane("XY")
        .box(self.length, self.width, self.base_height)
        .translate((0,0,-1*((self.height/2)+(self.base_height/2))))
    )
