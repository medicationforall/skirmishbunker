import cadquery as cq
from skirmishbunker import Bunker

bp = Bunker()
bp.inset=20
bp.width=150
bp.length=120
bp.make()
rec = bp.build()

cq.exporters.export(rec,'stl/bunker.stl')
