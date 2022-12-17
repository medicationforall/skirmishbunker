from cqterrain import Ladder

def init_ladder_params(self):
    self.render_ladders=True
    self.ladder_panels = [8]
    self.ladders = None

def make_ladders(self):
    bp = Ladder()
    bp.length = 20
    bp.height = self.height
    bp.make()
    ladder = bp.build()

    self.ladders = self.make_series(
        ladder,
        length_offset= self.panel_length - bp.length + self.panel_padding*2,
        x_translate = self.int_length/2 - bp.width/2,
        y_translate = self.int_width/2 - bp.width/2,
        z_translate=0,
        skip_list=None,
        keep_list=self.ladder_panels
    )
