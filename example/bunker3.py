import cadquery as cq
from skirmishbunker import Bunker

bp = Bunker()
bp.inset=15
bp.width=140
bp.length=110
bp.height=65

bp.render_panel_details=True
bp.panel_length=28
bp.panel_width = 6
bp.panel_padding = 4

bp.render_windows=True
bp.skip_windows = []
bp.window_length = 8
bp.window_height = 24
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"

bp.render_doors=True
bp.door_panels = [0, 5]

bp.render_ladders=True
bp.ladder_panels = [8]

bp.render_floor_tiles=True
bp.render_roof=True


bp.make()
rec = bp.build_plate()

#show_object(rec)


cq.exporters.export(rec,'stl/bunker3.stl')
