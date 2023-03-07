### Check if two beams are parallel

``` py linenums="1"
import sys
from pytekla import wrap


model = wrap("Model.Model")

operation = wrap("Model.Operations.Operation")

if not model.get_connection_status():
    print("Cannot connect with Tekla model")
    sys.exit()


while True:

    beams = tuple(model.pick_objects(object_type="part", prompt="Pick two beams"))

    if len(beams) != 2 or not all(("Beam" in str(b) for b in beams)):
        continue

    lines = tuple(wrap("Geometry3d.Line", b.start_point, b.end_point) for b in beams)

    parallel = wrap("Geometry3d.Parallel")

    if parallel.line_to_line(*lines):
        operation.display_prompt("Beams are parallel")
    else:
        operation.display_prompt("Beams are not parallel")
    break
```