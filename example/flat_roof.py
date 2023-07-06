import cadquery as cq
from skirmishbunker import FlatRoof

bp = FlatRoof()
bp.roof_chamfer = 10
bp.roof_operation = "chamfer"
bp.make()

flat_roof = bp.build()

#show_object(flat_roof)

cq.exporters.export(flat_roof,'stl/flat_roof.stl')
