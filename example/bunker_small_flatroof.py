import cadquery as cq
from skirmishbunker import Bunker, FlatRoof

# Renders a small bunker with chamfer
# and flat roof
bp = Bunker()
bp.inset=10
bp.width=75
bp.length=75
bp.height=65
bp.corner_chamfer=3

bp.render_panel_details=True
bp.panel_length=28
bp.panel_width = 5
bp.panel_padding = 4

bp.render_windows=True
bp.skip_windows = []
bp.window_length = 8
bp.window_height = 24
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"

bp.render_doors=True
bp.door_panels = [0]

bp.render_ladders=True
bp.ladder_panels = [2]

bp.render_floor_tiles=True
bp.render_roof=True


roof_obj = FlatRoof()

## ROOF ##
bp.render_roof = True
bp.set_roof_object(roof_obj)
bp.roof_height = 4
bp.roof_inset = -3
bp.roof_overflow = 1

bp.roof_chamfer_faces_selector = ""
bp.roof_chamfer_edges_selector = "(not <Z)"
bp.roof_tile_size = 20
bp.roof_tile_padding = 2
bp.roof_tile_height = 1


bp.make()
rec = bp.build_plate()

#show_object(rec)
cq.exporters.export(rec,'stl/bunker_small_flat_roof.stl')
