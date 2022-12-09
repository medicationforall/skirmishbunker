import cadquery as cq
from skirmishbunker import Roof

bp = Roof()
bp.length = 82
bp.width = 112
bp.height = 18
bp.inset = -3
bp.wall_details_inset = -0.8
bp.render_floor_tiles = True
bp.make()
roof_ex = bp.build()

cq.exporters.export(roof_ex,'stl/roof.stl')
