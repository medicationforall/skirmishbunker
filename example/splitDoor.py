import cadquery as cq
from skirmishbunker import SplitDoor

bp = SplitDoor()
bp.open=3
bp.make()
blast_door = bp.build()

cq.exporters.export(blast_door,'stl/splitDoor.stl')
