# Bunker Development

## Inspiration

https://www.reddit.com/r/PrintedMinis/comments/rgb3ln/i_painted_a_classic_warhammer_40k_bunker/
![](https://i.redd.it/sv2qlkwiaj581.jpg)

https://www.pinterest.com/pin/bunker-part-2--483855553698959743/
![](https://i.pinimg.com/originals/03/13/93/031393ff27641fc9b0f084084672d858.jpg)

---
## All Your Base
[src code](../src/skirmishbunker/Base.py)

**Base** is the class parent class that the project will inherit from.<br />
There are two lifecycle methods **make** and **build**. For all intents **base** derived classes are factories for making cadquery solids.

* **make** creates the parts off of class parameter values.
* **build** assembles the made parts onto a cadquery workplane.

If you call **build** without calling **make** an exception will be thrown.<br />
You can call **make** multiple times.

``` python
class Base:
    def __init__(self):
        self.width = 75
        self.length = 75
        self.height = 75
        self.make_called = False

    def make(self):
        self.make_called = True

    def build(self):
        if self.make_called == False:
            raise Exception('Make has not been called')

    def dimensions(self):
        return (self.length, self.width, self.height)
```

---

## Making The Outline
* Create the wedge outline, this is part of the blocking process.

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

    def make_wedge(self):
        self.wedge = (
            cq.Workplane("XY" )
            .wedge(self.length,self.height,self.width,self.inset,self.inset,self.length-self.inset,self.width-self.inset)
            .rotate((1,0,0),(0,0,0),-90)
        )

    def make(self):
        super().make()
        self.make_wedge()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.wedge)
        )
        return scene

bp = Bunker()
bp.make()
rec = bp.build()

show_object(rec)
```

![](image/01.png)

---
## Determine Wall Angle

* Calculate arccosine of base to inset angle.
* As a proof of concept I'm aligning a box to the exterior angled wall.

[Code Example 02 - Angle Test](../example/ex_02_angle.py)

### Add import
``` python
from cqterrain import roof
```

### New \_\_init__ Parameter
``` python
    self.angle = 0
```

### Angle Code From cqterrain roof
``` python
def angle(self, length, height):
    '''
    Presumed length and height are part of a right triangle
    '''
    hyp = math.hypot(length, height)
    angle = length/hyp
    angle_radians = math.acos((angle))
    angle_deg = math.degrees(angle_radians)
    return angle_deg
```

### Update make
``` python
def make(self):
    super().make()
    self.angle =roof.angle(self.inset, self.height)

    self.make_wedge()

    # Add example box
    box = cq.Workplane("XY").box(10,10,10).rotate((0,1,0),(0,0,0),-1*(self.angle)).translate((self.length/2,0,0))
    self.wedge = self.wedge.add(box)
```


### Generate examples

#### Inset 40
``` python
bp = Bunker()
bp.inset=40
bp.make()
rec = bp.build()
```

![](image/02.png)

#### Inset 10

``` python
bp = Bunker()
bp.inset=10
bp.make()
rec = bp.build()
```

![](image/03.png)

---

## Cut Out Interior
* I wanted a square interior as opposed to shelling the wedge outline.

[Code Example 03 - Interior](../example/ex_03_interior.py)

### New \_\_init__ Parameter

 ``` python
 self.inset = 20
 self.interior_rectangle = None
 ```

### Create interior_rectangle

``` python
def make_interior_rectangle(self):
    self.interior_rectangle = (
        cq.Workplane("XY")
        .box(self.length-(2*(self.inset+self.wall_width)), self.width-(2*(self.inset+self.wall_width)), self.height-self.wall_width)
        .translate((0,0,self.wall_width/2))
    )
```

### Update make

``` python
def make(self):
    super().make()
    self.angle =roof.angle(self.inset, self.height)

    self.make_wedge()
    self.make_interior_rectangle()

    # Add example box
    box = cq.Workplane("XY").box(10,10,10).rotate((0,1,0),(0,0,0),-1*(self.angle)).translate((self.length/2,0,0))
    self.wedge = self.wedge.add(box)
```

### Update build
``` python
def build(self):
    super().build()
    scene = (
        cq.Workplane("XY")
        .union(self.wedge)
        .cut(self.interior_rectangle)
    )
    return scene
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
## Cut Panels
* Create the outline rectangles where the bunker details will go.

[Code Example 04 - Cut Panels](../example/ex_04_cut.py)

### Add import
``` python
from math import floor as math_floor
```

### New \_\_init__ Parameters
``` python
self.wall_width = 5
self.panel_length = 28
self.panel_width = 6
self.panel_padding = 4

self.cut_panels = None
```

### Generate Cut Panels
``` python
def make_cut_panels(self):
      length = self.length-(2*(self.inset+self.wall_width))
      width = self.width-(2*(self.inset+self.wall_width))
      height = self.height
      inset = self.inset
      p_length = self.panel_length
      p_width = self.panel_width
      padding = self.panel_padding

      cut_panel = cq.Workplane("XY").box(p_length, p_width, height - padding)
      x_panels_size = math_floor(length / (p_length + (padding)))
      y_panels_size = math_floor(width / (p_length + (padding)))

      x_panels_plus = (
          series(cut_panel, x_panels_size, length_offset= padding*2)
          .rotate((1,0,0),(0,0,0),(self.angle)+90)
          .translate((0,((self.width-inset+(padding/2))/2)-p_width/2,-1*(padding)))
      )

      x_panels_minus = (
          series(cut_panel, x_panels_size, length_offset= padding*2)
          .rotate((1,0,0),(0,0,0),-1*(self.angle+90))
          .translate((0,-1*(((self.width-inset+(padding/2))/2)-p_width/2),-1*(padding)))
      )

      y_panels_plus = (
          series(cut_panel, y_panels_size, length_offset= padding*2)
          .rotate((0,0,1),(0,0,0),90)
          .rotate((0,1,0),(0,0,0),-1*(self.angle)+90)
          .translate((((self.length-inset+(padding/2))/2)-p_width/2,0,-1*(padding)))
      )

      y_panels_minus = (
          series(cut_panel, y_panels_size, length_offset= padding*2)
          .rotate((0,0,1),(0,0,0),90)
          .rotate((0,1,0),(0,0,0),(self.angle)+90)
          .translate((-1*(((self.length-inset+(padding/2))/2)-p_width/2),0,-1*(padding)))
      )

      self.cut_panels = x_panels_plus.add(y_panels_plus).add(x_panels_minus).add(y_panels_minus)
```

### Update make
``` python
def make(self):
    super().make()
    self.angle =roof.angle(self.inset, self.height)

    self.make_wedge()
    self.make_interior_rectangle()
    self.make_cut_panels()
```

### Update build
``` python
def build(self):
    super().build()
    scene = (
        cq.Workplane("XY")
        .union(self.wedge)
        .cut(self.interior_rectangle)
        .cut(self.cut_panels)
    )
    return scene
```

### Build the bunker
``` python
bp = Bunker()
bp.inset=20
bp.width=150
bp.length=120
bp.make()
rec = bp.build()
```

![](image/06.png)

---

## Create Arch Detail

[Code Example 05 - Arch Detail](../example/ex_05_arch_detail.py)

### New \_\_init__ Parameters
``` python
self.arch_padding_top = 3
self.arch_padding_sides = 3
self.arch_inner_height = 6
self.inner_arch_top = 5
self.inner_arch_sides = 4

self.panels = None
self.cut_panels = None
```

### Arch Details
``` python
def arch_detail(self):
    length = self.length-(2*(self.inset+self.wall_width))
    width = self.width-(2*(self.inset+self.wall_width))
    height = self.height
    inset = self.inset
    p_length = self.panel_length
    p_width = self.panel_width
    padding = self.panel_padding

    panel_outline = cq.Workplane("XY").box(p_length, p_width, height - padding)
    arch = shape.arch_pointed(p_length+self.arch_padding_sides, p_width/2 , height - padding + self.arch_padding_top, ((height - padding)/2) + self.arch_inner_height).translate((0,-1*(p_width/4),0))
    inner_arch = shape.arch_pointed(p_length + self.arch_padding_sides - self.inner_arch_sides, p_width , height - padding + self.arch_padding_top - self.inner_arch_top, ((height - padding)/2) + self.arch_inner_height - self.inner_arch_sides)
    inner_inner_arch = shape.arch_pointed(p_length + self.arch_padding_sides - self.inner_arch_sides-3, p_width/2 , height - padding + self.arch_padding_top - self.inner_arch_top-3, ((height - padding)/2) + self.arch_inner_height - self.inner_arch_sides).translate((0,(p_width/4),-1.5))
    panel_back = cq.Workplane("XY").box(p_length, p_width/2, height - padding).translate((0,(p_width/4),0))
    panel_detail = cq.Workplane("XY").add(panel_back).add(arch)
    inside_arch = panel_back.cut(inner_inner_arch)
    panel = panel_outline.intersect(panel_detail).cut(inner_arch).add(inside_arch)
    return panel
```

### Stub make_detail_panels
``` python
def make_detail_panels(self):
    detail_panel = self.arch_detail()
    self.panels = detail_panel
```

### Update make
``` python
def make(self):
    super().make()
    self.angle =roof.angle(self.inset, self.height)

    self.make_wedge()
    self.make_interior_rectangle()
    self.make_cut_panels()
    self.make_detail_panels()
```

### Update build
``` python
def build(self):
    super().build()
    scene = (
        cq.Workplane("XY")
        .union(self.wedge)
        .cut(self.interior_rectangle)
        .cut(self.cut_panels)
        .union(self.panels)
    )
    return scene
```

![](image/07.png)

---

## Add Detail Panels to bunker

* Stamp the arch details onto the building.
* Build out the stub method make_detail_panels from the previous example.

[Code Example 06 - Detail Panels](../example/ex_06_detail_panels.py)

### Build Out make_detail_panels Method
``` python
def make_detail_panels(self):
      length = self.length-(2*(self.inset+self.wall_width))
      width = self.width-(2*(self.inset+self.wall_width))
      height = self.height
      inset = self.inset
      p_length = self.panel_length
      p_width = self.panel_width
      padding = self.panel_padding

      detail_panel = self.arch_detail()

      x_panels_size = math_floor(length / (p_length + (padding)))
      y_panels_size = math_floor(width / (p_length + (padding)))

      x_panels_plus = (
          series(detail_panel, x_panels_size, length_offset= padding*2)
          .rotate((0,0,1),(0,0,0),180)
          .rotate((1,0,0),(0,0,0),(self.angle)-90)
          .translate((0,((self.width-inset+(padding/2))/2)-p_width/2,-1*(padding)))
      )

      x_panels_minus = (
          series(detail_panel, x_panels_size, length_offset= padding*2)
          .rotate((1,0,0),(0,0,0),-1*(self.angle-90))
          .translate((0,-1*(((self.width-inset+(padding/2))/2)-p_width/2),-1*(padding)))
      )

      y_panels_plus = (
          series(detail_panel, y_panels_size, length_offset= padding*2)
          .rotate((0,0,1),(0,0,0),-90)
          .rotate((0,1,0),(0,0,0),-1*(self.angle)+90)
          .translate((((self.length-inset+(padding/2))/2)-p_width/2,0,-1*(padding)))
      )

      y_panels_minus = (
          series(detail_panel, y_panels_size, length_offset= padding*2)
          .rotate((0,0,1),(0,0,0),90)
          .rotate((0,1,0),(0,0,0),(self.angle)-90)
          .translate((-1*(((self.length-inset+(padding/2))/2)-p_width/2),0,-1*(padding)))
      )

      self.panels = x_panels_plus.add(y_panels_plus).add(x_panels_minus).add(y_panels_minus)
```

![](image/08.png)

---

## Add a Base

* Add a base to resolve overhang on the bottom of the building.

[Code Example 07 - Base](../example/ex_07_base.py)

### New \_\_init__ Parameters

``` python
self.base_height = 3
self.base = None
```

### Make the base
``` python
def make_base(self):
    self.base = (
        cq.Workplane("XY")
        .box(self.length, self.width, self.base_height)
        .translate((0,0,-1*((self.height/2)+(self.base_height/2))))
    )
```

### Update make
``` python
def make(self):
    super().make()
    self.angle =roof.angle(self.inset, self.height)

    self.make_wedge()
    self.make_interior_rectangle()
    self.make_cut_panels()
    self.make_detail_panels()
    self.make_base()
```

### Update build
``` python
def build(self):
    super().build()
    scene = (
        cq.Workplane("XY")
        .union(self.wedge)
        .cut(self.interior_rectangle)
        .cut(self.cut_panels)
        .union(self.panels)
        .union(self.base)
    )
    return scene
```

![](image/09.png)

---

## Make Window Cut

* Create the outline of the windows and remove the spaces where they will reside.

[Code Example 08 - Window Cut](../example/ex_08_window_cut.py)

### New \_\_init__ Parameters
``` python
self.window_cut_width_padding = 1
self.window_length = 15
self.window_height = 20
self.cut_windows = None
```

### Make the cut windows

``` python
def make_cut_windows(self):
      length = self.length-(2*(self.inset+self.wall_width))
      width = self.width-(2*(self.inset+self.wall_width))
      height = self.height
      inset = self.inset
      p_length = self.panel_length
      p_width = self.panel_width
      padding = self.panel_padding
      cut_width = self.wall_width + inset/2 + self.window_cut_width_padding
      length_offset = p_length - self.window_length + padding*2

      cut_window = cq.Workplane("XY").box(self.window_length, cut_width,self.window_height)
      x_panels_size = math_floor(length / (p_length + (padding)))
      y_panels_size = math_floor(width / (p_length + (padding)))

      x_win_plus = (
          series(cut_window, x_panels_size, length_offset=length_offset)
          .translate((0,((self.width-inset+(padding/2))/2)-cut_width/2, -1*(padding)))
      )

      x_win_minus = (
          series(cut_window, x_panels_size, length_offset=length_offset)
          .translate((0,-1*(((self.width-inset+(padding/2))/2)-cut_width/2), -1*(padding)))
      )

      y_win_plus = (
          series(cut_window, y_panels_size, length_offset=length_offset)
          .rotate((0,0,1),(0,0,0),90)
          .translate((((self.length-inset+(padding/2))/2)-cut_width/2,0,-1*(padding)))
      )

      y_win_minus = (
          series(cut_window, y_panels_size, length_offset=length_offset)
          .rotate((0,0,1),(0,0,0),90)
          .translate((-1*(((self.length-inset+(padding/2))/2)-cut_width/2),0,-1*(padding)))
      )

      self.cut_windows = x_win_plus.add(y_win_plus).add(x_win_minus).add(y_win_minus)
```

### Update make
``` python
def make(self):
    super().make()
    self.angle =roof.angle(self.inset, self.height)

    self.make_wedge()
    self.make_interior_rectangle()
    self.make_cut_panels()
    self.make_detail_panels()
    self.make_base()
    self.make_cut_windows()
```

### Update build
``` python
def build(self):
    super().build()
    scene = (
        cq.Workplane("XY")
        .union(self.wedge)
        .cut(self.interior_rectangle)
        .cut(self.cut_panels)
        .union(self.panels)
        .union(self.base)
        .cut(self.cut_windows)
    )
    return scene
```

![](image/10.png)

---

## Add Window Details

* Create the window frames detail

[Code Example 09 - Window Detail](../example/ex_09_window_detail.py)

### Update Import

``` python
from cqterrain import roof, window
```

The code we care about looks like this.
``` python
def frame(length=20, width = 4, height = 40, frame_width=3):
    outline = cq.Workplane("XY").box(length, width, height)
    inline =  cq.Workplane("XY").box(length-(frame_width*2), width, height-(frame_width*2))
    return outline.cut(inline)
```

### New \_\_init__ Parameters

``` python
self.window_frame_width = 2
self.window_frame_chamfer = 1.6
self.window_frame_chamfer_select = "<Z or >Z"
self.windows = None
```

### Create The Frame Example Implementation


``` python
frame = window.frame(self.window_length, cut_width, self.window_height, self.window_frame_width)
frame = frame.faces("Y").edges(self.window_frame_chamfer_select).chamfer(self.window_frame_chamfer)
```

![](image/11.png)

## Create the windows
``` python
def make_windows(self):
      length = self.length-(2*(self.inset+self.wall_width))
      width = self.width-(2*(self.inset+self.wall_width))
      height = self.height
      inset = self.inset
      p_length = self.panel_length
      p_width = self.panel_width
      padding = self.panel_padding
      cut_width = self.wall_width + inset/2 + self.window_cut_width_padding
      length_offset = p_length - self.window_length + padding*2

      frame = window.frame(self.window_length, cut_width, self.window_height, self.window_frame_width)
      frame = frame.faces("Y").edges(self.window_frame_chamfer_select).chamfer(self.window_frame_chamfer)
      x_panels_size = math_floor(length / (p_length + (padding)))
      y_panels_size = math_floor(width / (p_length + (padding)))

      x_win_plus = (
          series(frame, x_panels_size, length_offset=length_offset)
          .translate((0,((self.width-inset+(padding/2))/2)-cut_width/2, -1*(padding)))
      )

      x_win_minus = (
          series(frame, x_panels_size, length_offset=length_offset)
          .rotate((0,0,1),(0,0,0),180)
          .translate((0,-1*(((self.width-inset+(padding/2))/2)-cut_width/2), -1*(padding)))
      )

      y_win_plus = (
          series(frame, y_panels_size, length_offset=length_offset)
          .rotate((0,0,1),(0,0,0),90)
          .translate((((self.length-inset+(padding/2))/2)-cut_width/2,0,-1*(padding)))
      )

      y_win_minus = (
          series(frame, y_panels_size, length_offset=length_offset)
          .rotate((0,0,1),(0,0,0),90)
          .rotate((0,0,1),(0,0,0),180)
          .translate((-1*(((self.length-inset+(padding/2))/2)-cut_width/2),0,-1*(padding)))
      )
      self.windows = x_win_plus.add(y_win_plus).add(x_win_minus).add(y_win_minus)
```

### Update make

``` python
def make(self):
    super().make()
    self.angle =roof.angle(self.inset, self.height)

    self.make_wedge()
    self.make_interior_rectangle()
    self.make_cut_panels()
    self.make_detail_panels()
    self.make_base()
    self.make_cut_windows()
    self.make_windows()
```


### Update build

``` python
def build(self):
    super().build()
    scene = (
        cq.Workplane("XY")
        .union(self.wedge)
        .cut(self.interior_rectangle)
        .cut(self.cut_panels)
        .union(self.panels)
        .union(self.base)
        .cut(self.cut_windows)
        .union(self.windows)
    )
    return scene
```


![](image/12.png)

---

## Testing Window Alternates

``` python
bp = Bunker()
bp.inset=20
bp.width=300
bp.length=120
bp.window_length = 7
bp.window_height = 30
bp.make()
rec = bp.build()
```

![](image/13.png)

``` python
bp = Bunker()
bp.inset=20
bp.width=150
bp.length=120
bp.window_length = 18
bp.window_height = 8
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"
bp.make()
rec = bp.build()
```

![](image/14.png)

---

## Skip Window POC

[Code Example 10 - Skip Windows](../example/ex_10_skip_windows.py)

In order to add doors I need to be able to skip adding the windows at certain indexes. I'd like to be able to set an array of windows to skip [0, 2, 4] and consistently not render those details.

### New \_\_init__ Parameters
``` python
self.skip_windows = [0, 2, 4]
```

### Modify make_cut_windows and make_windows
To enforce for the skip_windows array.

``` python
scene = x_win_plus.add(y_win_plus).add(x_win_minus).add(y_win_minus)

if self.skip_windows and len(self.skip_windows) > 0:
    solids = scene.solids().vals()
    scene = cq.Workplane("XY")

    for  index, solid in enumerate(solids):
        if index not in self.skip_windows:
            scene.add(solid)

self.windows = scene
```

![](image/15.png)

I'm making this look easy, but the ordering in how the solids are added to the workplane and how the solids are rotated matter to have consistent indexes.

![](image/16.png)

Changing the overall dimensions should keep the same relative indexes.

![](image/17.png)

---

## Cut Out The Door

[Code Example 11 - Cut Door](../example/ex_11_cut_door.py)

Follows the same indexing rules as the windows but in this case you are specifying which panels will have doors as opposed to which ones will not.

### New \_\_init__ Parameters
``` python
self.door_panels = [0]
self.door_length = 23
self.door_height =35
self.door_fillet = 4
self.cut_doors = None
```

### Create The Cut Doors
``` python
def make_cut_doors(self):
      length = self.length-(2*(self.inset+self.wall_width))
      width = self.width-(2*(self.inset+self.wall_width))
      height = self.height
      inset = self.inset
      p_length = self.panel_length
      p_width = self.panel_width
      padding = self.panel_padding
      cut_width = self.wall_width + inset/2 + self.window_cut_width_padding
      length_offset = p_length - self.door_length + padding*2

      #cut_window = cq.Workplane("XY").box(self.window_length, cut_width,self.window_height)
      cut_door = (
          cq.Workplane("XY")
          .box(self.door_length, 20, self.door_height)
          .edges("|Y").fillet(self.door_fillet)
          .translate((0,0,-1*(height/2 - self.door_height/2)+self.wall_width))
      )
      x_panels_size = math_floor(length / (p_length + (padding)))
      y_panels_size = math_floor(width / (p_length + (padding)))

      x_plus = (
          series(cut_door, x_panels_size, length_offset=length_offset)
          .translate((0,((self.width-inset+(padding/2))/2)-cut_width/2, 0))
      )

      x_minus = (
          series(cut_door, x_panels_size, length_offset= length_offset)
          .rotate((0,0,1),(0,0,0),180)
          .translate((0,-1*(((self.width-inset+(padding/2))/2)-cut_width/2),0))
      )

      y_plus = (
          series(cut_door, y_panels_size, length_offset=length_offset)
          .rotate((0,0,1),(0,0,0),90)
          .translate((((self.length-inset+(padding/2))/2)-cut_width/2,0,0))
      )

      y_minus = (
          series(cut_door, y_panels_size, length_offset=length_offset)
          .rotate((0,0,1),(0,0,0),90)
          .rotate((0,0,1),(0,0,0),180)
          .translate((-1*(((self.length-inset+(padding/2))/2)-cut_width/2),0,0))
      )

      scene = x_plus.add(y_plus).add(x_minus).add(y_minus)

      if self.door_panels and len(self.door_panels) > 0:
          solids = scene.solids().vals()
          scene = cq.Workplane("XY")

          for  index, solid in enumerate(solids):
              if index in self.door_panels:
                  scene.add(solid)

      self.cut_doors = scene
```

### Update Build

``` python
def build(self):
    super().build()

    scene = (
        cq.Workplane("XY")
        .union(self.wedge)
        .union(self.panels)
        .cut(self.cut_doors)
        .cut(self.cut_windows)
        .add(self.base)
        .union(self.windows)
    )
    return scene
```

![](image/18.png)

---

## Refactoring
I have some problems with this code base.<br >
Chiefly the repeated code all over the place for series management.

``` python
x_plus = (
    series(cut_door, x_panels_size, length_offset=length_offset)
    .translate((0,((self.width-inset+(padding/2))/2)-cut_width/2, 0))
)

x_minus = (
    series(cut_door, x_panels_size, length_offset= length_offset)
    .rotate((0,0,1),(0,0,0),180)
    .translate((0,-1*(((self.width-inset+(padding/2))/2)-cut_width/2),0))
)

y_plus = (
    series(cut_door, y_panels_size, length_offset=length_offset)
    .rotate((0,0,1),(0,0,0),90)
    .translate((((self.length-inset+(padding/2))/2)-cut_width/2,0,0))
)

y_minus = (
    series(cut_door, y_panels_size, length_offset=length_offset)
    .rotate((0,0,1),(0,0,0),90)
    .rotate((0,0,1),(0,0,0),180)
    .translate((-1*(((self.length-inset+(padding/2))/2)-cut_width/2),0,0))
)

scene = x_plus.add(y_plus).add(x_minus).add(y_minus)
```

* Ideally I'd like to place any arbitrary shape in the correct panel locations
* I'd like to be able to skip creating a solid at a given index
* I'd like to be able to keep a solid at a given index

### POC Example
Run the example in a different cqeditor instance.<br />
[Code Example 12 - Refactoring Series](../example/ex_12_refactoring_series.py)

### Minimal make method
``` python
def make_cut_panels(self):
    cut_panel = (
        self.make_cut_panel()
        .rotate((1,0,0),(0,0,0),(self.angle)+90)
        )
    self.cut_panels = self.make_series(cut_panel, [0], [0,2, 4, 5, 6, 7, 8])
```

Does two things
* Generate the shape
* Make the series of the given shape

### Make the shape
``` python
def make_cut_panel(self):
    cut_panel = cq.Workplane("XY").box(
        self.panel_length,
        self.panel_width, self.height - self.panel_padding
    )
    return cut_panel
```

### Make the series

``` python
def make_series(self, shape, skip_list=None, keep_list=None):
        length = self.length-(2*(self.inset+self.wall_width))
        width = self.width-(2*(self.inset+self.wall_width))
        padding = self.panel_padding
        inset = self.inset
        p_width = self.panel_width

        x_panels_size = math_floor(length / (self.panel_length + self.panel_padding))
        y_panels_size = math_floor(width / (self.panel_length + self.panel_padding))

        x_plus = (
            series(shape, x_panels_size, length_offset= padding*2)
            .translate((0,((self.width-inset+(padding/2))/2)-p_width/2,-1*(padding)))
        )

        x_minus = (
            series(shape, x_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),180)
            .translate((0,-1*(((self.width-inset+(padding/2))/2)-p_width/2),-1*(padding)))
        )

        y_plus = (
            series(shape, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),90)
            .translate((((self.length-inset+(padding/2))/2)-p_width/2,0,-1*(padding)))
        )

        y_minus = (
            series(shape, y_panels_size, length_offset= padding*2)
            .rotate((0,0,1),(0,0,0),90)
            .rotate((0,0,1),(0,0,0),180)
            .translate((-1*(((self.length-inset+(padding/2))/2)-p_width/2),0,-1*(padding)))
        )

        scene = x_plus.add(y_plus).add(x_minus).add(y_minus)

        if skip_list and len(skip_list) > 0:
            solids = scene.solids().vals()
            scene = cq.Workplane("XY")

            for  index, solid in enumerate(solids):
                if index not in skip_list:
                    scene.add(solid)            
        elif keep_list and len(keep_list) > 0:
            solids = scene.solids().vals()
            scene = cq.Workplane("XY")

            for  index, solid in enumerate(solids):
                if index in keep_list:
                    scene.add(solid)

        return scene
```

This code doesn't seem any shorter but...
* It's no longer opinionated about the shape.
* It doesn't care about the angle of the shape.
* If given a skip list it follows it.
* If given a keep list it follow it.
* A skip list beats a keep list

---

## Apply the make_series method
What was 375 lines got refactored to 257 or a **30%** decrease of the Bunker class.<br /><br />
Refer to the example to see the full list of changes.<br />
[Code Example 13 - Series changes Applied](../example/ex_13_series_applied.py)

### Old make_detail_panels
``` python
def make_detail_panels(self):
      length = self.length-(2*(self.inset+self.wall_width))
      width = self.width-(2*(self.inset+self.wall_width))
      height = self.height
      inset = self.inset
      p_length = self.panel_length
      p_width = self.panel_width
      padding = self.panel_padding

      detail_panel = self.arch_detail()

      x_panels_size = math_floor(length / (p_length + (padding)))
      y_panels_size = math_floor(width / (p_length + (padding)))

      x_panels_plus = (
          series(detail_panel, x_panels_size, length_offset= padding*2)
          .rotate((0,0,1),(0,0,0),180)
          .rotate((1,0,0),(0,0,0),(self.angle)-90)
          .translate((0,((self.width-inset+(padding/2))/2)-p_width/2,-1*(padding)))
      )

      x_panels_minus = (
          series(detail_panel, x_panels_size, length_offset= padding*2)
          .rotate((1,0,0),(0,0,0),-1*(self.angle-90))
          .translate((0,-1*(((self.width-inset+(padding/2))/2)-p_width/2),-1*(padding)))
      )

      y_panels_plus = (
          series(detail_panel, y_panels_size, length_offset= padding*2)
          .rotate((0,0,1),(0,0,0),-90)
          .rotate((0,1,0),(0,0,0),-1*(self.angle)+90)
          .translate((((self.length-inset+(padding/2))/2)-p_width/2,0,-1*(padding)))
      )

      y_panels_minus = (
          series(detail_panel, y_panels_size, length_offset= padding*2)
          .rotate((0,0,1),(0,0,0),90)
          .rotate((0,1,0),(0,0,0),(self.angle)-90)
          .translate((-1*(((self.length-inset+(padding/2))/2)-p_width/2),0,-1*(padding)))
      )

      self.panels = x_panels_plus.add(y_panels_plus).add(x_panels_minus).add(y_panels_minus)

```

### New make_detail_panels
``` python
def make_detail_panels(self):
    detail_panel = (
        self.arch_detail()
        .rotate((0,1,0),(0,0,0),180)
        .rotate((1,0,0),(0,0,0),(self.angle)+90)
    )
    x_translate = ((self.length-self.inset+(self.panel_padding/2))/2)-self.panel_width/2
    y_translate = ((self.width-self.inset+(self.panel_padding/2))/2)-self.panel_width/2

    self.panels = self.make_series(detail_panel, length_offset=self.panel_padding*2, x_translate=x_translate, y_translate=y_translate, z_translate=-1*(self.panel_padding))
```
