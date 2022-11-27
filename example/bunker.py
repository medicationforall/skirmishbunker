import cadquery as cq
from skirmishbunker import Bunker

bp = Bunker()
bp.make()
rec = bp.build()

cq.exporters.export(rec,'stl/bunker.stl')
