## Model

### Change part names

``` py linenums="1"
import sys
from pytekla import wrap


model = wrap("Model.Model")

if not model.get_connection_status():
    print("Cannot connect with Tekla model")
    sys.exit()

parts = model.pick_objects(object_type="part", prompt="Pick some parts")

for part in parts:
    part.name = "NEW COOL NAME"
    part._class = "42"
    part.modify()


model.commit_changes("Modify parts")
```