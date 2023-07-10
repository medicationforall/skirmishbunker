import cadquery as cq
from cadqueryhelper import series
from math import floor

class SeriesHelper:
    def __init__(self):
        # basic shape info
        self.shape = None
        self.outer_length = 0
        self.outer_width = 0
        self.length_offset = 0

        # "component" (panel) size
        self.comp_length = 0
        self.comp_padding = 0

        # additional translation
        self.x_translate = 0
        self.y_translate = 0
        self.z_translate = 0

        self.skip_list = []
        self.keep_list = []

        self.scene = None

    def __validate(self):
        if (self.shape == None):
            raise Exception('No shape set')

        if (self.outer_length <= 0 or self.outer_width <= 0):
            raise Exception('Outer width and length need to be set')

        if (self.comp_padding + self.comp_length <= 0):
            raise Exception('Component sizes need to be set')

    def get_scene(self):
        if (self.scene == None):
            raise Exception('You must ')
        
        return self.scene

    def make(self):
        self.__validate()

        shape = self.shape
        length = self.outer_length
        width = self.outer_width
        length2 = self.comp_length
        length_offset = self.length_offset
        padding = self.comp_padding
        x_trans = self.x_translate
        y_trans = self.y_translate
        z_trans = self.z_translate

        x_comp_size = floor(length / (length2 + padding))
        y_comp_size = floor(width / (length2 + padding))

        x_shapes = series(
            shape,
            x_comp_size,
            length_offset = length_offset
        )
        y_shapes = series(
            shape,
            y_comp_size,
            length_offset = length_offset
        )

        x_plus = (cq.Workplane("XY")
            .add(x_shapes)
            .translate((0, y_trans, z_trans)))

        x_minus = (cq.Workplane("XY")
            .add(x_shapes)
            .rotate((0,0,1), (0,0,0), 180)
            .translate((0, -1 * y_trans, z_trans)))

        y_plus = (cq.Workplane("XY")
            .add(y_shapes)
            .rotate((0,0,1), (0,0,0), 90)
            .translate((x_trans, 0, z_trans)))

        y_minus = (cq.Workplane("XY")
            .add(y_shapes)
            .rotate((0,0,1), (0,0,0), 90)
            .rotate((0,0,1), (0,0,0), 180)
            .translate((-1 * (x_trans), 0, z_trans)))

        scene = (x_plus
            .add(y_plus)
            .add(x_minus)
            .add(y_minus))

        if self.skip_list and len(self.skip_list) > 0:
            solids = scene.solids().vals()
            scene = cq.Workplane("XY")

            for  index, solid in enumerate(solids):
                if index not in self.skip_list:
                    scene.add(solid)
        elif self.keep_list and len(self.keep_list) > 0:
            solids = scene.solids().vals()
            scene = cq.Workplane("XY")

            for  index, solid in enumerate(solids):
                if index in self.keep_list:
                    scene.add(solid)

        self.scene = scene