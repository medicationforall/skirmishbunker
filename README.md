# skirmishbunker
python Library for making a skirmish wargame bunker

![](./documentation/image/cover.png)

## Documentation
[Thorough writeup of the development of the bunker](./documentation/README.md)

### Example Usage

``` python
import cadquery as cq
from skirmishbunker import Bunker

bp = Bunker()
bp.inset=15
bp.width=140
bp.length=110
bp.height=65

bp.render_windows=True
bp.skip_windows = []
bp.window_length = 18
bp.window_height = 8
bp.window_frame_chamfer = 1.6
bp.window_frame_chamfer_select = "<Z"

bp.render_doors=True
bp.door_panels = [0, 3]

bp.render_ladders=True
bp.ladder_panels = [8]

bp.render_floor_tiles=True
bp.render_roof=False

bp.make()
rec = bp.build()

cq.exporters.export(rec,'bunker.stl')
```

## Dependencies
* [CadQuery 2.1](https://github.com/CadQuery/cadquery)
* [cqMore](https://github.com/JustinSDK/cqMore)
* [cadqueryhelper](https://github.com/medicationforall/cadqueryhelper)
* [cqterrain](https://github.com/medicationforall/cqterrain)


### Installation
To install skirmishbunker directly from GitHub, run the following `pip` command:

	pip install git+https://github.com/medicationforall/skirmishbunker

**OR**

### Local Installation
From the cloned skirmishbunker directory run.

	pip install ./
