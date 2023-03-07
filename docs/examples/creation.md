## Model Creation

### Single beam

``` py linenums="1"
import sys
from pytekla import wrap


model = wrap("Model.Model")

if not model.get_connection_status():
    print("Cannot connect with Tekla model")
    sys.exit()

material = wrap("Model.Material")
material.material_string = "A36"

beam_profile = wrap("Model.Profile")
beam_profile.profile_string = "W310X107"

beam_position = wrap("Model.Position")
beam_position.rotation_offset = 90
beam_position.depth = wrap("Model.Position.DepthEnum").BEHIND

beam = wrap("Model.Beam")
beam.start_point = wrap("Geometry3d.Point", 0.0, 0.0, 0.0)
beam.end_point = wrap("Geometry3d.Point", 5000.0, 0.0, 0.0)
beam.name = "PYTEKLA BEAM"
beam._class = "42"  # Cannot use "class" in lowercase
beam.profile = beam_profile
beam.material = material
beam.position = beam_position
beam.deforming_data.cambering = 100
beam.insert()

model.commit_changes("Beam creation")
```

### Rectangular grid
``` py linenums="1"
import itertools
from string import ascii_uppercase

import numpy as np
from pytekla import wrap


def letters():
    n = 1
    while True:
        yield from (
            "".join(group) for group in itertools.product(ascii_uppercase, repeat=n)
        )
        n += 1


model = wrap("Model.Model")

x_y_step = 5000
z_step = 3000

x_axis = np.arange(0, 20000 + x_y_step, x_y_step)
y_axis = np.arange(0, 50000 + x_y_step, x_y_step)
z_levels = np.arange(0, 9000 + z_step, z_step)

grid = wrap("Model.Grid")
grid.coordinate_x = " ".join(str(x) for x in np.diff(x_axis, prepend=0))
grid.coordinate_y = " ".join(str(y) for y in np.diff(y_axis, prepend=0))
grid.coordinate_z = " ".join(str(z) for z in np.diff(z_levels, prepend=0))

grid.label_x = " ".join(str(x + 1) for x in range(len(x_axis)))
grid.label_y = " ".join(itertools.islice(letters(), len(y_axis)))
grid.label_z = " ".join(f"+{z}" for z in z_levels)

grid.insert()

model.commit_changes("Add Rectangular Grid")
```

### Radial grid
``` py linenums="1"
import itertools
from math import degrees
from string import ascii_uppercase

import numpy as np
from pytekla import wrap


def letters():
    n = 1
    while True:
        yield from (
            "".join(group) for group in itertools.product(ascii_uppercase, repeat=n)
        )
        n += 1


model = wrap("Model.Model")


n_points = 25
radius = np.arange(5000, 25000, 5000)

angles = np.linspace(0, 2 * np.pi, n_points)

degrees_angles = np.array([degrees(x) for x in angles])

n_floors = 5
floor_height = 5000

z_levels = np.arange(
    0, floor_height * n_floors + floor_height, floor_height, dtype=float
)

radial_grid = wrap("Model.RadialGrid")

radial_grid.angular_coordinates = " ".join(
    str(angle) for angle in np.diff(degrees_angles, prepend=0)
)
radial_grid.coordinate_z = " ".join(str(z) for z in z_levels)
radial_grid.radial_coordinates = " ".join(str(x) for x in radius)
radial_grid.angular_labels = " ".join(itertools.islice(letters(), len(degrees_angles)))
radial_grid.label_z = " ".join(f"+{str(z)}" for z in z_levels)
radial_grid.radial_labels = " ".join(str(i) for i, _ in enumerate(radius, start=1))

radial_grid.insert()

model.commit_changes("Add Radial Grid")
```


## Drawing Creation

### Single drawing
``` py linenums="1"
from pytekla import wrap

a3_size = wrap("Drawing.Size", 410.0, 287.0)

layout_attributes = wrap("Drawing.LayoutAttributes")
layout_attributes.sheet_size = a3_size

ga_drawing = wrap("Drawing.GADrawing")
ga_drawing.name = "PyTekla Drawing"
ga_drawing.layout = layout_attributes
ga_drawing.title1 = "Awesome drawing"

ga_drawing.insert()
```