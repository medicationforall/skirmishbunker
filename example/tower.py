import cadquery as cq
from skirmishbunker import Bunker, Roof

bp = Bunker()
bp.inset=15
bp.width=140
bp.length=140
bp.height=85
bp.base_height=5
bp.window_length = 18
bp.window_height = 8
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"
bp.door_panels = [4, 10]
bp.render_floor_tiles=True
bp.render_roof=False
bp.make()
floor_1 = bp.build()

bp2 = Bunker()
bp2.inset=17
bp2.width=112
bp2.length=112
bp2.height=65
bp2.base_height=5
bp2.window_length = 8
bp2.window_height = 25
bp2.window_frame_chamfer = 1.6
bp2.window_frame_chamfer_select = "<Z"
bp2.door_panels = [0]
bp2.render_floor_tiles=True
bp2.render_roof=False
bp2.make()
floor_2  = bp2.build()

bp = Roof()
bp.length = 80
bp.width = 80
bp.height = 18
bp.inset = -3
bp.wall_details_inset = -0.8
bp.render_floor_tiles = True
bp.make()
roof_ex = bp.build()

scene = cq.Workplane("XY").add(floor_1).add(floor_2.translate((0,0,80)))

#show_object(scene)

cq.exporters.export(floor_1,'stl/tower_1.stl')
cq.exporters.export(floor_2,'stl/tower_2.stl')
cq.exporters.export(roof_ex,'stl/tower_roof.stl')
