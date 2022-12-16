import cadquery as cq
from .BlastDoor import BlastDoor

def init_door_params(self):
    self.render_doors=True
    self.door_panels = [0,3]
    self.ladder_panels = [8]
    self.door_length = 23
    self.door_height =35
    self.door_fillet = 4

    self.cut_doors = None
    self.doors = None

def make_cut_doors(self):
    height = self.height
    door_cut_width = self.inset+self.wall_width

    if self.inset<0:
        door_cut_width = -1*(self.inset)+self.wall_width

    cut_door = (
        cq.Workplane("XY")
        .box(self.door_length, door_cut_width, self.door_height)
        .edges("|Y").fillet(self.door_fillet)
        .translate((0,0,-1*(height/2 - self.door_height/2)+self.wall_width))
    )

    self.cut_doors = self.make_series(
        cut_door,
        length_offset=self.panel_length - self.door_length + self.panel_padding*2,
        x_translate = self.int_length/2+door_cut_width/2,
        y_translate = self.int_width/2+door_cut_width/2,
        z_translate=0, skip_list=None, keep_list=self.door_panels
    )

def make_doors(self):
    height = self.height
    bp = BlastDoor()
    bp.length = self.door_length
    bp.height = self.door_height
    bp.make()
    door = bp.build().translate((0,0,-1*(height/2 - self.door_height/2)+self.wall_width))

    x_translate = self.int_length/2+bp.width
    y_translate = self.int_width/2+bp.width
    if self.inset <= 0:
        x_translate = self.int_length/2+(bp.width/4)
        y_translate = self.int_width/2+(bp.width/4)

    self.doors = self.make_series(
        door,
        length_offset=self.panel_length - self.door_length + self.panel_padding*2,
        x_translate = x_translate,
        y_translate = y_translate,
        z_translate=0, skip_list=None, keep_list=self.door_panels
    )
