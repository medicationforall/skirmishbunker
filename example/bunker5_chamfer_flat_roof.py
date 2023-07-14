import cadquery as cq
from skirmishbunker import Bunker, FlatRoof

bp = Bunker()
bp.length = 150
bp.width = 150
bp.floor_thickness = 5
bp.ladder_panels = [2]
bp.render_magnets = True
bp.set_roof_object(FlatRoof())
bp.corner_chamfer = 10
bp.wall_width = 15
bp.roof_overflow = -3
bp.pip_padding = 8
bp.render_pips = True
bp.render_magnets = True
bp.make()
#bunker = bp.build_plate()
bunker = bp.build()

show_object(bunker)

cq.exporters.export(bunker,'stl/bunker5_chamfer_flat_roof.stl')
