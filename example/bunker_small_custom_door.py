import cadquery as cq
from skirmishbunker import Bunker, SplitDoor
from cqterrain import tile
from cadqueryhelper import shape

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

def custom_cut_door(bunker):
    height = bunker.height
    p_length = bunker.panel_length
    p_width = bunker.panel_width
    padding = bunker.panel_padding
    door_cut_width = bunker.inset+bunker.wall_width

    padding_top = 3.2

    if bunker.inset<0:
        door_cut_width = -1*(bunker.inset)+bunker.wall_width

    cut = (
        shape.arch_pointed(24, door_cut_width, 49, 27.3)
        .translate((0,-0,-3))
    )

    cut = shape.arch_pointed(
        p_length  - bunker.inner_arch_sides,
        door_cut_width,
        height - padding - bunker.inner_arch_top - bunker.wall_width+1 -padding_top,
        ((height - padding)/2) + bunker.arch_inner_height - bunker.inner_arch_sides - bunker.wall_width+1 - padding_top
    ).translate((0,0,-4 + bunker.wall_width /2 - padding_top / 2))

    return cut

def custom_door(bunker):
    height = bunker.height
    p_length = bunker.panel_length
    padding = bunker.panel_padding
    padding_top = 3.2

    bp = SplitDoor()
    bp.length = p_length  - bunker.inner_arch_sides
    bp.height = height - padding - bunker.inner_arch_top - bunker.wall_width+1 -padding_top
    bp.width = 1
    bp.base_height = ((height - padding)/2) + bunker.arch_inner_height - bunker.inner_arch_sides - bunker.wall_width+1 - padding_top
    bp.open = 6
    bp.make()
    door = bp.build()
    #return door.translate((0,0,0))
    return door.translate((0,-1,-4 + bunker.wall_width /2 - padding_top / 2))


bp = Bunker()
bp.inset=0
bp.width=75
bp.length=75
bp.height=65
bp.wall_width =6

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

bp.render_ladders=False
bp.ladder_panels = [0]

bp.render_floor_tiles=True
bp.render_roof=False

bp.floor_padding = -5
bp.floor_tile_padding =.5

bp.render_floor_cuts = False
bp.render_pips = True
bp.render_magnets = True
bp.render_base = True

bp.custom_floor_tile = custom_windmill_tile

bp.custom_cut_door = custom_cut_door
bp.custom_cut_door_padding = -.5

bp.custom_door = custom_door
bp.custom_door_padding = -.5

bp.make()
rec = bp.build_body()

#show_object(rec)

cq.exporters.export(rec,'stl/bunker_small_custom_door.stl')
