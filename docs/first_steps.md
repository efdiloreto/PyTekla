## Setting the Path to the Tekla Structures bin Folder

When using PyTekla for the first time, it is necessary to set the directory path to the Tekla Structures bin folder. To do that, you need to import a function called `set_tekla_path`. 

```python
>>> from pytekla.config import set_tekla_path
>>> set_tekla_path("C:\\TeklaStructures\\2022.0\\bin")
```

You need to do this just once or when you want to work with another Tekla Structures version.

After this you are all set to start coding in PyTekla!


## Using PyTekla

After importing PyTekla you will have access to all the [Tekla Open API](https://developer.tekla.com/tekla-structures/api/22/8180) library:

``` py linenums="1"
import pytekla
from Tekla.Structures.Model import Model, Beam
```

There are two ways to use the Tekla Open API library with PyTekla. The first option is to use the library directly, while the second option is to use the wrappers provided by PyTekla.


### Examples

Let's take a look at how each of these options works using an example to get some objects from the model and read properties from one of them.

=== "Without PyTekla wrappers"

    ``` py linenums="1"
    import clr
    import pytekla
    from System.Collections import Hashtable, ArrayList
    from Tekla.Structures.Model import Model, Part, Weld

    model = Model()

    # Check model connection status
    if not model.GetConnectionStatus():
        print("Cannot connect with Tekla model")
        sys.exit()

    # Get all Assembly and Part objects
    model_object_selector = model.GetModelObjectSelector()

    # We need to get the .NET types to use in this method
    types = [clr.GetClrType(t) for t in (Assembly, Part)]
    objects_enumerator = model_object_selector.GetAllObjectsWithType(types)

    # objects is a ModelObjectEnumerator [https://developer.tekla.com/tekla-structures/api/22/14457]
    # We may want to have a Python list with all these objects for other purposes
    objects_list = [o for o in objects_enumerator]

    # Grab first object to get some information
    # obj is instance of a ModelObject subclass [https://developer.tekla.com/tekla-structures/api/22/14416]
    obj = objects_list[0]

    # Get all user properties
    user_hash_table = Hashtable()
    obj.GetAllUserProperties(hash_table)

    # We have a .NET Hashtable [https://learn.microsoft.com/en-us/dotnet/api/system.collections.hashtable?view=net-7.0]
    # For future use, we may want to convert it to a Python dictionary
    user_properties_dict = {k: v for k, v in zip(user_hash_table.Keys, user_hash_table.Values)}

    # Get some report properties
    report_hash_table = Hashtable()

    str_names = ArrayList()
    str_names.Add("MATERIAL")
    str_names.Add("FINISH")

    double_names = ArrayList()
    double_names.Add("WEIGHT")

    int_names = ArrayList()
    int_names.Add("GROUP_ID")

    # The name of the method is confusing, it only gets the specified properties
    obj.GetAllReportProperties(str_names, double_names, int_names, report_hash_table)

    # Convert to Python Dict for future use
    report_properties_dict = {k: v for k, v in zip(report_hash_table.Keys, report_hash_table.Values)}
    ```

=== "With PyTekla wrappers"

    ``` py linenums="1"
    from pytekla import wrapper


    model = wrapper("Model.Model")

    # Check model connection status
    if not model.get_connection_status():
        print("Cannot connect with Tekla model")
        sys.exit()

    # Get all Assembly and Part objects
    # PyTekla will find the type names in the Tekla.Structures.Model namespace [https://developer.tekla.com/tekla-structures/api/22/13460]
    objects_generator = model.get_objects_with_types(("Assembly", "Part"))

    # objects is a native Python generator 
    objects_list = list(objects_generator)

    # Grab first object to get some information
    # obj is instance of a PyTekla ModelObjectWrapper 
    obj = objects_list[0]

    # Get all user properties
    user_properties_dict = obj.get_all_user_properties()

    # Get some report properties
    report_properties_dict = obj.get_multiple_report_properties(
        string_names=["MATERIAL", "FINISH"],
        float_names=["WEIGHT"],
        int_names=["GROUP_ID"]
    )
    ```

!!! note

    As per the [Tekla Open API documentation](https://developer.tekla.com/tekla-structures/api/22/14389), if the connection to Tekla Structures is lost it cannot be re-established. To get the model connected you can try to run Tekla Structures as Admisnitrator.

## How the wrappers work

A wrapper is an object that encapsulates and contains another object. It allows the wrapped object to be accessed and used through the wrapper. The wrapper can provide additional functionality and services.

PyTekla provides five types of wrappers:

- [`BaseWrapper`][pytekla.wrappers.BaseWrapper]
- [`ModelObjectWrapper`][pytekla.wrappers.ModelObjectWrapper]
- [`ModelWrapper`][pytekla.wrappers.ModelWrapper]
- [`DrawingDbObjectWrapper`][pytekla.wrappers.DrawingDbObjectWrapper]
- [`DrawingHandlerWrapper`][pytekla.wrappers.DrawingHandlerWrapper]

Those wrappers provide a more 'pythonic' experience when working with the Tekla Open API. You can check their documentation in the [API Reference section](api_reference.md).

You can use directly those wrappers or use the handy `wrap` function. This function will wrap any Tekla Structures object. Let see an example:

```python
from pytekla import wrap
from Tekla.Structures.Model import Material, Beam

# This will return a 'BaseWrapper' object.
material = wrap(Material())

# This will return a 'ModelObjectWrapper' object.
beam = wrap(Beam())
```

Alternatively, you can use strings to instanciate the objects:

```python
from tekla import wrap

# This will find, instanciate and wrap the type Tekla.Structures.Model.Material
material = wrap("Model.Material")

# This will find, instanciate and wrap the type Tekla.Structures.Model.Beam
beam = wrap("Model.Beam")
```

For more examples check this [section](examples/selection.md).