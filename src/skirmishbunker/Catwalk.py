import cadquery as cq
from skirmishbunker import Base

class Catwalk(Base):
    def __init__(self):
        super().__init__()
        self.length = 185
        self.width = 185
        self.height = 4

        self.interior_length = 130
        self.interior_width = 130
        self.interior_height = 2
        self.interior_overlap = 5

        self.render_magnets = False
        self.magnet_radius = 1.5
        self.magnet_height = 2
        self.magnet_padding = 1.5

        self.platform = None
        self.cut_magnets = None

    def __make_platform(self):
        platform = cq.Workplane("XY").box(self.length, self.width, self.height)
        center_cut = cq.Workplane("XY").box(self.interior_length, self.interior_width, self.height)
        overlap = cq.Workplane("XY").box(self.interior_length , self.interior_width, self.interior_height)
        overlap_cut = cq.Workplane("XY").box(self.interior_length - self.interior_overlap*2, self.interior_width - self.interior_overlap*2, self.interior_height)

        self.platform = (
            platform
            .cut(center_cut)
            .union(overlap.translate((0,0,-1*(self.height/2 - self.interior_height/2))))
            .cut(overlap_cut.translate((0,0,-1*(self.height/2 - self.interior_height/2))))
        )

    def __make_magnet_cuts(self):
        magnet = cq.Workplane("XY").cylinder(self.magnet_height, self.magnet_radius+.1)

        x_translate = self.interior_length/2-self.magnet_radius-self.magnet_padding
        y_translate = self.interior_width/2-self.magnet_radius-self.magnet_padding
        z_translate = -1*(self.height/2 - self.magnet_height/2)

        pips = (
            cq.Workplane("XY")
            .union(magnet.translate((x_translate, y_translate, z_translate)))
            .union(magnet.translate((-1*x_translate, y_translate, z_translate)))
            .union(magnet.translate((-1*x_translate, -1*y_translate, z_translate)))
            .union(magnet.translate((x_translate, -1*y_translate, z_translate)))
        )
        self.cut_magnets = pips

    def make(self):
        super().make()
        self.__make_platform()
        self.__make_magnet_cuts()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.platform)
            .cut(self.cut_magnets)
        )
        return scene


#bp = Catwalk()
#bp.make()
#result = bp.build()

#show_object(result)
