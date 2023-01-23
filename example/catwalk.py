import cadquery as cq
from skirmishbunker import Catwalk

bp = Catwalk()
bp.height = 4
bp.make()
result = bp.build()

#show_object(result)
cq.exporters.export(result, 'stl/catwalk.stl')
