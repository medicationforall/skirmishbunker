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

### Install a development version

If you want to work on this library locally you will need the following instaled globally on you computer:

* Python 3
* setuptools
* pip
* virtualenv (venv)

Next you will need to clone this repo (or, ideally, your own fork):

	git clone https://github.com/medicationforall/skirmishbunker

Now, step into the cloned folder and build a Python virtual environment:

	cd /path/to/skirmishbunker
	python -m venv ./venv

Once this is done, activate the virtual environment and install dependencies:

	source ./venv/bin/activate
	pip install ./

This will take a little while to run, once finished, you might need to link `skirmishbunker` as an editable library (or your changes will not be seen). Do this as follows:

	pip install -e ./

Now edit away! 