import cadquery as cq
from skirmishbunker import Bunker

bp = Bunker()
bp.inset=15
bp.width=140
bp.length=110
bp.height=65
bp.window_length = 18
bp.window_height = 8
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"

bp.render_windows=True
bp.skip_windows = []

bp.render_doors=False
bp.door_panels = [0,3]

bp.render_ladders=False
bp.ladder_panels = [8]

bp.render_floor_tiles=False
bp.render_roof=False

bp.make()
rec = bp.build()

cq.exporters.export(rec,'stl/bunker.stl')
