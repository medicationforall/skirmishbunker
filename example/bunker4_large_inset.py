import cadquery as cq
from skirmishbunker import Bunker

bp = Bunker()
bp.inset=50
bp.width=150
bp.length=150
bp.height=65

bp.render_panel_details=True
bp.panel_length=28
bp.panel_width = 6
bp.panel_padding = 4

bp.render_windows=True
bp.skip_windows = []
bp.window_length = 15
bp.window_width = 32
bp.window_width_offset = -1
bp.window_translate = 3
bp.window_height = 8
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"

bp.render_doors=False
bp.door_panels = [0, 5]

bp.render_ladders=False
bp.ladder_panels = [8]

bp.render_floor_tiles=False
bp.render_roof=False


bp.make()
rec = bp.build_body()

#show_object(rec)

cq.exporters.export(rec,'stl/bunker4_large_inset.stl')
