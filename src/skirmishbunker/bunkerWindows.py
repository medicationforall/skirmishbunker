import cadquery as cq
from cqterrain import window

def init_window_params(self):
    self.render_windows=True
    self.window_width_offset = -2
    self.window_length = 15
    self.window_width = None
    self.window_height = 20
    self.window_length_padding = 0

    self.window_frame_width = 2
    self.window_frame_chamfer = 1.6
    self.window_frame_chamfer_select = "<Z or >Z"
    self.skip_windows = [0]

    self.custom_cut_window=None
    self.custom_cut_window_padding = 0

    self.custom_window=None
    self.custom_window_padding = 0

    self.cut_windows = None
    self.windows = None

def resolve_window_skip(self):
    skip_list = [] + self.skip_windows

    if self.render_doors:
        skip_list = skip_list + self.door_panels

    if self.render_ladders:
        skip_list = skip_list + self.ladder_panels

    return skip_list

def make_cut_windows(self):
    height = self.height
    cut_width = self.inset+self.wall_width
    if self.inset < 0:
        cut_width= -1*self.inset

    if self.custom_cut_window:
        cut_window = self.custom_cut_window(self)
    else:
        cut_window = cq.Workplane("XY").box(self.window_length, cut_width,self.window_height)

    inset = self.inset
    padding = self.panel_padding
    self.cut_windows = self.make_series(
        cut_window,
        length_offset=self.panel_length - self.window_length + (self.panel_padding+self.custom_cut_window_padding)*2,
        x_translate = self.int_length/2+cut_width/2,
        y_translate = self.int_width/2+cut_width/2,
        z_translate=-1*(self.panel_padding), skip_list=resolve_window_skip(self), keep_list=None
    )

def make_windows(self):
    height = self.height
    window_width = self.inset
    if self.inset < 0:
        window_width= -1*self.inset
    elif self.inset == 0:
        window_width = self.wall_width+2

    # inset override
    if self.window_width:
        window_width = self.window_width

    if self.custom_cut_window:
        frame = self.custom_window(self)
    else:
        frame = window.frame(self.window_length, window_width, self.window_height, self.window_frame_width)
        frame = frame.faces("Y").edges(self.window_frame_chamfer_select).chamfer(self.window_frame_chamfer)

    inset = self.inset
    padding = self.panel_padding
    self.windows = self.make_series(
        frame,
        length_offset=self.panel_length - self.window_length + (self.panel_padding+self.custom_window_padding)*2,
        x_translate = self.int_length/2+window_width/2+self.window_width_offset,
        y_translate = self.int_width/2+window_width/2+self.window_width_offset,
        z_translate=-1*(self.panel_padding), skip_list=resolve_window_skip(self), keep_list=None
    )
