### Display prompt

``` py linenums="1"
import sys
from pytekla import wrap


model = wrap("Model.Model")

operation = wrap("Model.Operations.Operation")

if not model.get_connection_status():
    print("Cannot connect with Tekla model")
    sys.exit()


operation.display_prompt("Some message")
```