import cadquery as cq
from skirmishbunker import Bunker

bp = Bunker()
bp.inset=15
bp.width=220
bp.length=140
bp.height=95

bp.render_windows=True
bp.skip_windows = [0]
bp.window_length = 9
bp.window_height = 38
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"

bp.render_doors=True
bp.door_panels = [0, 3, 7]

bp.render_ladders=True
bp.ladder_panels = [8, 14]

bp.render_floor_tiles=True
bp.render_roof=True

bp.make()
rec = bp.build()

cq.exporters.export(rec,'stl/bunker2.stl')
