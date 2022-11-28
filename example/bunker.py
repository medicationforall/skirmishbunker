import cadquery as cq
from skirmishbunker import Bunker

bp = Bunker()
bp.inset=20
bp.width=150
bp.length=120
bp.window_length = 18
bp.window_height = 8
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"
bp.make()
rec = bp.build()

cq.exporters.export(rec,'stl/bunker.stl')
