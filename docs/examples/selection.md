## Model Selection

### Pick objects

``` py linenums="1"
from pytekla import wrap

model = wrap("Model.Model")

# The returned value is a 'ModelObjectWrapper' Python generator
picked_objects = model.pick_objects(object_type="part", prompt="Select parts from the model")
```

### Get all objects

``` py linenums="1"
from pytekla import wrap

model = wrap("Model.Model")

# The returned value is a 'ModelObjectWrapper' Python generator
all_objects = model.get_all_objects()
```

### Get selected objects

``` py linenums="1"
from pytekla import wrap

model = wrap("Model.Model")

# The returned value is a 'ModelObjectWrapper' Python generator
selected_objects = model.get_selected_objects()
```

### Get objects with types

``` py linenums="1"
from pytekla import wrap

model = wrap("Model.Model")

# The returned value is a 'ModelObjectWrapper' Python generator
objects_with_types = model.get_objects_with_types(["Beam", "Assembly"])
```

### Get objects by filter

``` py linenums="1"
from pytekla import wrap

model = wrap("Model.Model")

# The returned value is a 'ModelObjectWrapper' Python generator
objects_by_filter = model.get_objects_by_filter("Steel_All")
```

### Get objects by bounding box

``` py linenums="1"
from pytekla import wrap

model = wrap("Model.Model")

# The returned value is a 'ModelObjectWrapper' Python generator
objects_by_bounding_box = model.get_objects_by_bounding_box((0, 0, 0), (5000, 5000, 5000))
```

## Drawing Selection

### Get active drawing

``` py linenums="1"
from pytekla import wrap

drawing_handler = wrap("Drawing.DrawingHandler")

# DrawingDbObjectWrapper instance
active_drawing = drawing_handler.get_active_drawing()
```

### Get all drawings

``` py linenums="1"
from pytekla import wrap

drawing_handler = wrap("Drawing.DrawingHandler")

drawings = drawing_handler.get_drawings()
```