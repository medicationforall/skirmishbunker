# Bunker Development

## Inspiration

https://www.reddit.com/r/PrintedMinis/comments/rgb3ln/i_painted_a_classic_warhammer_40k_bunker/
![](https://i.redd.it/sv2qlkwiaj581.jpg)

https://www.pinterest.com/pin/bunker-part-2--483855553698959743/
![](https://i.pinimg.com/originals/03/13/93/031393ff27641fc9b0f084084672d858.jpg)

---

## Making The Outline

[Example 01 - Outline](../example/ex_01_outline.py)

``` python
import cadquery as cq
from cadqueryhelper import shape
from skirmishbunker import Base

class Bunker(Base):
    def __init__(self):
        super().__init__()
        self.length = 100
        self.width = 100
        self.height = 75
        self.inset = 10
        self.wedge = None

    def make(self):
        super().make()
        self.wedge = (
            cq.Workplane("XY" )
            .wedge(self.length,self.height,self.width,self.inset,self.inset,self.length-self.inset,self.width-self.inset)
            .rotate((1,0,0),(0,0,0),-90)
        )

    def build(self):
        super().build()
        return self.wedge

bp = Bunker()
bp.make()
rec = bp.build()

show_object(rec)
```

![](image/01.png)

---
## Determine Wall Angle

[Code Example 02 - Angle Test](../example/ex_02_angle.py)

 ### New \_\_init__ Parameter
``` python
    self.angle = 0
```

### Angle code
``` python
def find_angle(self, length, height):
    '''
    Presumed length and height are part of a right triangle
    '''
    hyp = math.hypot(length, height)
    angle = length/hyp
    angle_radians = math.acos((angle))
    angle_deg = math.degrees(angle_radians)
    return angle_deg
```

### Update make method
``` python
def make(self):
    super().make()
    self.wedge = (
        cq.Workplane("XY" )
        .wedge(self.length,self.height,self.width,self.inset,self.inset,self.length-self.inset,self.width-self.inset)
        .rotate((1,0,0),(0,0,0),-90)
    )

    #determine angle
    self.angle =self.find_angle(self.inset, self.height)

    # Add example box
    box = cq.Workplane("XY").box(10,10,10).rotate((0,1,0),(0,0,0),-1*(self.angle)).translate((self.length/2,0,0))
    self.wedge = self.wedge.add(box)
```

### Generate examples
``` python
bp = Bunker()
bp.inset=40
bp.make()
rec = bp.build()
```

![](image/02.png)

``` python
bp = Bunker()
bp.inset=10
bp.make()
rec = bp.build()
```

![](image/03.png)

---

## Cut Out Interior
 I wanted a square interior as opposed to shelling the wedge outline.

 [Code Example 03 - Interior](../example/ex_02_angle.py)

 ### New \_\_init__ Parameter
 ``` python
 self.inset = 20
 ```

 ### Create interior_rectangle
``` python
interior_rectangle = (
    cq.Workplane("XY")
    .box(self.length-(2*(self.inset+self.wall_width)), self.width-(2*(self.inset+self.wall_width)), self.height-self.wall_width)
    .translate((0,0,self.wall_width/2))
)
```

![](image/04.png)

### Width Test
``` python
bp = Bunker()
bp.inset=20
bp.width=150
bp.make()
rec = bp.build()
```

![](image/05.png)

---
## Create panels
