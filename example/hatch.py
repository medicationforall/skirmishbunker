import cadquery as cq
from skirmishbunker import Hatch

bp = Hatch()
bp.make()
roof_ex = bp.build()

cq.exporters.export(roof_ex,'stl/hatch.stl')
