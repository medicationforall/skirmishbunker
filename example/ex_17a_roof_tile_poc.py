import cadquery as cq

tile_size = 21
tile_padding = 2

tile = cq.Workplane("XY").box(tile_size, tile_size, 2)
slot = cq.Workplane("XY").slot2D(tile_size,2).extrude(2).rotate((0,0,1),(0,0,0),45)
slot2 = cq.Workplane("XY").slot2D(tile_size-7,2).extrude(2).rotate((0,0,1),(0,0,0),45).translate((-3,-3,0))
slot3 = cq.Workplane("XY").slot2D(tile_size-7,2).extrude(2).rotate((0,0,1),(0,0,0),45).translate((3,3,0))
slot4 = cq.Workplane("XY").slot2D(tile_size-7-7,2).extrude(2).rotate((0,0,1),(0,0,0),45).translate((-3-3,-3-3,0))
slot5 = cq.Workplane("XY").slot2D(tile_size-7-7,2).extrude(2).rotate((0,0,1),(0,0,0),45).translate((3+3,3+3,0))

tile = tile.cut(slot).cut(slot2).cut(slot3).cut(slot4).cut(slot5)

show_object(tile)
