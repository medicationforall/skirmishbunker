import cadquery as cq
from skirmishbunker import Bunker
from cqterrain import tile

def custom_star_tile(bunker):
    star_tile = tile.star(
        length = bunker.floor_tile_size,
        width = bunker.floor_tile_size,
        height = bunker.floor_tile_height,
        points = 4,
        outer_radius = bunker.floor_tile_size/2,
        inner_radius = 2,
        padding = .5
    )
    return star_tile

def custom_windmill_tile(bunker):
    windmill_tile = tile.windmill(
        tile_size = bunker.floor_tile_size,
        height = bunker.floor_tile_height,
        padding = .5
    )
    return windmill_tile

bp = Bunker()
bp.inset=15
bp.width=140
bp.length=110
bp.height=65

bp.render_panel_details=True
bp.panel_length=28
bp.panel_width = 5
bp.panel_padding = 4

bp.render_windows=True
bp.skip_windows = []
bp.window_length = 18
bp.window_height = 8
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"

bp.render_doors=True
bp.door_panels = [0]

bp.render_ladders=True
bp.ladder_panels = [8]

bp.render_floor_tiles=True
bp.render_roof=True

bp.floor_padding = -5
bp.floor_tile_padding=.5

bp.render_floor_cuts = False
bp.render_pips=True
bp.render_magnets=True

#bp.custom_floor_tile = custom_windmill_tile

bp.make()

body_complete = bp.build()
cq.exporters.export(body_complete,'stl/bunker_med_both.stl')

body = bp.build_body()
cq.exporters.export(body,'stl/bunker_med_body.stl')

roof = bp.build_roof()
cq.exporters.export(roof,'stl/bunker_med_roof.stl')
