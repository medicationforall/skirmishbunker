from . import Base
import cadquery as cq
from cadqueryhelper import shape, wave

class SplitDoor(Base):
    def __init__(self):
        super().__init__()
        self.length = 25
        self.width = 3.5
        self.height = 40
        self.base_height = 20
        self.open = 0
        self.bar_height=1

        self.cut_door = None
        self.split_door = None

    def __make_cut_door(self):
        cut_door = shape.arch_pointed(
            self.length,
            self.width,
            self.height,
            self.base_height
        )
        self.cut_door = cut_door

    def __make_door(self):
        divide = .8
        left_wave = wave.square(self.height, self.length/2+divide, self.width, 5, self.length/2-divide)

        # for making the clean cut
        door_left = (
            left_wave
            .rotate((1,0,0),(0,0,0),-90)
            .rotate((0,1,0),(0,0,0),90)
            .translate((self.length/4-divide/2,0,0))

        )

        door_left_chamfer = (
            left_wave
            .rotate((1,0,0),(0,0,0),-90)
            .rotate((0,1,0),(0,0,0),90)
            .faces("<X").edges("Z")
            .chamfer(self.width/2-.01)
            .translate((self.length/4-divide/2,0,0))

        )


        left = (
            cq.Workplane("XY")
            .add(self.cut_door)
            .intersect(door_left_chamfer)

        )

        right = (
            cq.Workplane("XY")
            .add(self.cut_door)
            .cut(door_left)
            .faces(">X").edges("Z")
            .chamfer(self.width/2-.01)

        )
        bar = (
            cq.Workplane("XY").box(self.length, self.width, self.bar_height)
            .translate((0,0,-1*(self.height/2-self.bar_height/2)))
        )

        scene = (
            cq.Workplane("XY")
            .union(left.translate((self.open,0,0)))
            .union(right.translate((-self.open,0,0)))
            .union(bar)
        )
        scene_cut = self.cut_door.intersect(scene)

        self.split_door = scene_cut


    def make(self):
        super().make()
        self.__make_cut_door()
        self.__make_door()

    def build(self):
        super().build()
        return self.split_door
