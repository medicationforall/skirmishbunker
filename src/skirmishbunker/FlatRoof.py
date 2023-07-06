import cadquery as cq
from skirmishbunker import Base

class FlatRoof(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length = 160
        self.width = 150
        self.height = 25

        # select all edges on the positive z face
        self.roof_chamfer_faces_selector = "+Z"
        self.roof_chamfer_edges_selector = ""
        self.roof_chamfer = 10
        self.roof_operation = "chamfer" # chamfer, fillet

        #shapes
        self.roof_body = None

    def __make_roof_body(self):
        roof_body = (
            cq.Workplane("XY")
            .box(self.length,self.width,self.height)
        )

        if self.roof_chamfer and self.roof_chamfer < self.height:
            if self.roof_operation.lower() == "chamfer":
                roof_body = (
                    roof_body
                    .faces(self.roof_chamfer_faces_selector)
                    .edges(self.roof_chamfer_edges_selector)
                    .chamfer(self.roof_chamfer)
                )
            elif self.roof_operation.lower() == "fillet":
                roof_body = (
                    roof_body
                    .faces(self.roof_chamfer_faces_selector)
                    .edges(self.roof_chamfer_edges_selector)
                    .fillet(self.roof_chamfer)
                )
            else:
                raise Exception("Unrecognied roof operation")
        else:
            # better to kill if this condition is met otherwise it fails silently.
            raise Exception(f"roof_chamfer {self.roof_chamfer} >= roof height {self.height}")

        self.roof_body = roof_body

    def make(self):
        super().make()
        self.inner_length = self.length - self.roof_chamfer*2
        self.inner_width = self.width - self.roof_chamfer*2

        self.__make_roof_body()

    def build(self):
        super().build()
        return self.roof_body
