import cadquery as cq
from skirmishbunker import Roof

bp = Roof()
bp.height = 20
bp.inset = 2
bp.wall_details_inset = 1.5
bp.make()
roof_ex = bp.build()

cq.exporters.export(roof_ex,'stl/roof.stl')
