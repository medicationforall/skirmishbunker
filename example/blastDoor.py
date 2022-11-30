import cadquery as cq
from skirmishbunker import BlastDoor

bp = BlastDoor()
bp.make()
blast_door = bp.build()

cq.exporters.export(blast_door,'stl/blastDoor.stl')
