from cqterrain import Ladder

def init_ladder_params(self):
    self.render_ladders = True
    self.ladder_panels = [0]
    self.ladder_length = 20
    self.ladder_z_translate = 0
    self.ladders = None
    self.custom_ladder = None

def make_ladders(self):
    bp = Ladder()
    bp.length = self.ladder_length
    bp.height = self.height

    if self.custom_ladder:
        self.custom_ladder(self, bp)

    bp.make()
    ladder = bp.build()

    self.ladders = self.make_series(
        ladder,
        length_offset= self.panel_length - bp.length + self.panel_padding*2,
        x_translate = self.int_length/2 - bp.width/2,
        y_translate = self.int_width/2 - bp.width/2,
        z_translate = self.ladder_z_translate,
        skip_list = None,
        keep_list = self.ladder_panels
    )
