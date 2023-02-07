import cadquery as cq
from skirmishbunker import SplitDoor

bp = SplitDoor()
bp.width = 24
bp.width = 2
bp.chamfer_minus = 0.1
bp.height = 56
bp.base_height = 32.5
bp.open=5
bp.make()
door = bp.build()

cq.exporters.export(door,'stl/splitDoor.stl')
