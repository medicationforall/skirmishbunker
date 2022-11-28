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

 [Code Example 03 - Interior](../example/ex_03_interior.py)

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
## Cut Panels

[Code Example 04 - Cut Panels](../example/ex_04_cut.py)

### New \_\_init__ Parameters
``` python
self.wall_width = 5
self.panel_length = 28
self.panel_width = 6
self.panel_padding = 4
```

### Generate cut panels
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
    x_panels_size = math.floor(length / (p_length + (padding)))
    y_panels_size = math.floor(width / (p_length + (padding)))

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

    return x_panels_plus.add(x_panels_minus).add(y_panels_plus).add(y_panels_minus)
```

### Remove Cut Panels From Bunker
``` python
  # cut panels
  cut_panels = self.make_cut_panels()
  self.wedge = self.wedge.cut(cut_panels)
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

### Details
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

### Update Build
``` python
def build(self):
    super().build()
    scene = (
        cq.Workplane("XY")
        #.add(self.wedge)
        .add(self.panels)
    )
    return scene
```

![](image/07.png)

---

## Add Detail Panels to bunker

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

      x_panels_size = math.floor(length / (p_length + (padding)))
      y_panels_size = math.floor(width / (p_length + (padding)))

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

      self.panels = x_panels_plus.add(x_panels_minus).add(y_panels_plus).add(y_panels_minus)
```

![](image/08.png)

---

## Add a Base

[Code Example 07 - Base](../example/ex_07_base.py)

### New \_\_init__ Parameters

``` python
self.base_height = 2
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

### Update Build
``` python
def build(self):
    super().build()

    scene = (
        cq.Workplane("XY")
        .add(self.wedge)
        .add(self.panels)
        .add(self.base)
    )
    return scene
```

![](image/09.png)

---

## Make Window Cut

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
    x_panels_size = math.floor(length / (p_length + (padding)))
    y_panels_size = math.floor(width / (p_length + (padding)))

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

    self.cut_windows = x_win_plus.add(x_win_minus).add(y_win_plus).add(y_win_minus)
```

### Update Build
``` python
def build(self):
    super().build()

    scene = (
        cq.Workplane("XY")
        .add(self.wedge)
        .add(self.panels)
        .add(self.base)
        .cut(self.cut_windows)
    )
    return scene
```

![](image/10.png)

---

## Add Window Details

[Code Example 09 - Window Detail](../example/ex_09_window_detail.py)

### New Import

``` python
from cqterrain import window
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

### Create The Frame


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
    frame = frame.faces("Y").edges("<Z or >Z").chamfer(self.window_frame_chamfer)
    x_panels_size = math.floor(length / (p_length + (padding)))
    y_panels_size = math.floor(width / (p_length + (padding)))

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
    self.windows = x_win_plus.add(x_win_minus).add(y_win_plus).add(y_win_minus)
```


### Update Build

``` python
def build(self):
    super().build()

    scene = (
        cq.Workplane("XY")
        .add(self.wedge)
        .add(self.panels)
        .cut(self.cut_windows)
        .add(self.base)
        .add(self.windows)
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
