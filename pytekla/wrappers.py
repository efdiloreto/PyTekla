import inspect
from types import GeneratorType

import clr
import Tekla.Structures
from System import Double, Int32, String
from System.Collections import Hashtable, IDictionary, IEnumerable, IEnumerator
from System.Collections.Generic import Dictionary, List
from Tekla.Structures.Drawing import DatabaseObject, DrawingHandler
from Tekla.Structures.Geometry3d import Point
from Tekla.Structures.Model import UI, Model, ModelObject

from .coreutils.collections import iterable_to_net_array_list, net_idictionary_to_dict
from .coreutils.names import to_pascal_case
from .coreutils.properties import check_property_type


PICKER_OBJECT_TYPES = {
    "object": UI.Picker.PickObjectsEnum.PICK_N_OBJECTS,
    "part": UI.Picker.PickObjectsEnum.PICK_N_PARTS,
    "weld": UI.Picker.PickObjectsEnum.PICK_N_WELDS,
    "bolt group": UI.Picker.PickObjectsEnum.PICK_N_BOLTGROUPS,
    "reinforcement": UI.Picker.PickObjectsEnum.PICK_N_REINFORCEMENTS,
}


_TEKLA_OBJECT_ATTR_NAME = "_tekla_object"


def _process_attr(_object):
    if isinstance(_object, GeneratorType):
        return _object
    if isinstance(_object, IDictionary):
        return {
            k: wrap(v, detect_types=False) for k, v in zip(_object.Keys, _object.Values)
        }
    elif isinstance(_object, (IEnumerator, IEnumerable)):
        return (wrap(elem, detect_types=False) for elem in _object)
    else:
        return wrap(_object, detect_types=False)


def _attrs_wrapper(func):
    def wrapper(*args, **kwargs):
        args = [a.unwrap() if isinstance(a, BaseWrapper) else a for a in args]
        kwargs = {
            k: (v.unwrap() if isinstance(v, BaseWrapper) else v)
            for k, v in kwargs.items()
        }
        result = func(*args, **kwargs)
        new_result = _process_attr(result)
        return new_result

    return wrapper


def _get_tekla_object(_object):
    return object.__getattribute__(_object, _TEKLA_OBJECT_ATTR_NAME)


def _set_tekla_object(_object, value):
    return object.__setattr__(_object, _TEKLA_OBJECT_ATTR_NAME, value)


class BaseWrapper:
    """
    A base wrapper for Tekla Structures API objects.

    This class provides a more Pythonic interface for interacting with Tekla Structures software.

    When an attribute is accessed, the class uses the `__getattr__` and `__getattribute__` methods to convert the attribute to a more Pythonic format.

    This class also uses the [`wrap`][pytekla.wrappers.wrap] function to automatically convert wrapped objects to their internal Tekla.Structures format when they are set as attributes.

    When a C# IEnumerator instance is returned, this class converts it to a Python generator. Similarly, when an IDictionary subclass is returned, this class converts it to a Python dictionary.

    References
    ----------
        https://developer.tekla.com/tekla-structures/api/22/8180
    """

    def __init__(self, tekla_object):
        """Initializes the class using a Tekla API object

        Parameters
        ----------
        tekla_object : Tekla.Structures object
            The object to wrap.
        """
        _set_tekla_object(self, tekla_object)

    def __getattribute__(self, name):
        result = object.__getattribute__(self, name)

        if name == "unwrap":
            return result

        if callable(result):
            return _attrs_wrapper(result)

        return _process_attr(result)

    def __getattr__(self, attr):
        to = _get_tekla_object(self)

        returned_attr = getattr(to, to_pascal_case(attr))

        if callable(returned_attr):
            return _attrs_wrapper(returned_attr)

        return _process_attr(returned_attr)

    def __setattr__(self, attr, value):
        if isinstance(value, BaseWrapper):
            value = value.unwrap()

        if attr in object.__getattribute__(self, "__dict__"):
            return object.__setattr__(self, attr, value)
        try:
            to = _get_tekla_object(self)
            to.__setattr__(to_pascal_case(attr), value)
        except AttributeError:
            raise AttributeError(
                f"'{_get_tekla_object(self)}' has not attribute '{attr}'"
            )

    def unwrap(self):
        """
        Get the original Tekla Structures object that is wrapped by this class or subclass instance.

        Returns
        -------
        Tekla.Structures object
            The original Tekla Structures object.

        Examples
        -------
        >>> obj = BaseWrapper(tekla_object)
        >>> original_obj = obj.unwrap()
        """
        return _get_tekla_object(self)

    def __repr__(self):
        """Return a string representation of the class name of the wrapped Tekla object.

        Returns
        -------
        str
            The string representation of the class name of the wrapped Tekla object.

        Examples
        -------
        >>> obj = BaseWrapper(tekla_object)
        >>> str(obj)
        '<PyTekla> OriginalName'
        """
        class_name = "<PyTekla> " + _get_tekla_object(self).__class__.__name__
        return class_name


class WithUserPropertyMixin:
    def get_user_property(self, property_name, property_type):
        """Gets the value of a user property for the given `property_name`.

        Parameters
        ----------
        property_name : str
            The name of the user property.
        property_type : type
            The type of the user property, must be `str`, `int`, or `float`.

        Returns
        -------
        str, int, float or None
            The value of the user property. None if it was not found.

        Raises
        ------
        TypeError
            If `property_type` is not `str`, `int`, or `float`.

        Examples
        -------
        >>> model_object_wrapper = ModelObjectWrapper(some_tekla_object)
        >>> value = model_object_wrapper.get_user_property('property_name', str)
        """
        check_property_type(property_type)
        to = _get_tekla_object(self)
        was_found, value = to.GetUserProperty(property_name, property_type())
        if was_found:
            return value

    def set_user_property(self, property_name, value):
        """
        Sets the user property with the specified name to the specified value.

        Parameters
        ----------
        property_name : str
            The name of the user property.
        value : str, int or float
            The value to set the user property to.

        Returns
        -------
        bool
            Indicates if the property was set.

        Raises
        ------
        TypeError
            If the value type is not one of [str, int, float].

        Examples
        -------
        >>> model_object_wrapper = ModelObjectWrapper(some_tekla_object)
        >>> model_object_wrapper.set_user_property('property_name', value)
        """
        check_property_type(type(value))
        to = _get_tekla_object(self)
        return to.SetUserProperty(property_name, value)


class ModelObjectWrapper(BaseWrapper, WithUserPropertyMixin):
    """This class is a wrapper around Tekla.Structures.Model.ModelObject that provides helper methods
    for working with ModelObject's properties.

    Examples
    --------
    Instantiate a `ModelObjectWrapper` instance from a Tekla Structures object:

    >>> from Tekla.Structures.Model import Beam
    >>> from pytekla import ModelObjectWrapper
    >>> wrapped_beam = ModelObjectWrapper(Beam())

    Access the wrapped object's attributes using Python's preferred naming convention:

    >>> wrapped_beam.name
    'BEAM'
    >>> wrapped_beam.name = "MY BEAM"
    >>> wrapped_beam.modify()

    Retrieve the original Tekla Structures object from the `ModelObjectWrapper` instance:

    >>> unwrapped_beam = wrapped_beam.unwrap()

    References
    ----------
        https://developer.tekla.com/tekla-structures/api/22/14416
    """

    main_type = ModelObject

    def __init__(self, tekla_object):
        """Initializes the class using a Tekla API ModelObject object

        Parameters
        ----------
        tekla_object : Tekla.Structures object
            The object to wrap.
        """
        super().__init__(tekla_object)

    def get_report_property(self, property_name, property_type):
        """
        Gets the value of a report property for the given `property_name`.

        Parameters
        ----------
        property_name : str
            The name of the report property.
        property_type : type
            The type of the report property, must be `str`, `int`, or `float`.

        Returns
        -------
        str, int, float or None
            The value of the report property. None if it was not found.

        Raises
        ------
        TypeError
            If `property_type` is not `str`, `int`, or `float`.

        Examples
        -------
        >>> model_object_wrapper = ModelObjectWrapper(some_tekla_object)
        >>> value = model_object_wrapper.get_report_property('property_name', str)
        """
        check_property_type(property_type)
        to = _get_tekla_object(self)
        was_found, value = to.GetReportProperty(property_name, property_type())
        if was_found:
            return value

    def get_all_user_properties(self):
        """
        Get all user properties of the Tekla Model Object as a dictionary.

        Returns
        -------
        dict
            A dictionary containing the user properties and their values, with keys as property names and values as property values.

        Examples
        -------
        >>> model_object_wrapper = ModelObjectWrapper(some_tekla_object)
        >>> user_properties = model_object_wrapper.get_all_user_properties()
        """
        hash_table = Hashtable()
        to = _get_tekla_object(self)
        to.GetAllUserProperties(hash_table)
        return hash_table

    def get_multiple_report_properties(
        self, string_names=None, float_names=None, int_names=None
    ):
        """
        Get multiple report properties as a dictionary.

        Parameters
        ----------
        string_names : list of str, optional
            A list of string property names to retrieve.
        float_names : list of str, optional
            A list of float property names to retrieve.
        int_names : list of str, optional
            A list of integer property names to retrieve.

        Returns
        -------
        dict
            A dictionary containing the report properties and their values, with keys as property names and values as property values.

        Examples
        -------
        >>> model_object_wrapper = ModelObjectWrapper(some_model_object)
        >>> report_properties = model_object_wrapper.get_multiple_report_properties(
        ...     string_names=['Property1', 'Property2'],
        ...     float_names=['Property3', 'Property4'],
        ...     int_names=['Property5', 'Property6']
        ... )
        >>> report_properties
        {'Property1': 'value1', 'Property2': 'value2', 'Property3': 0.5, 'Property4': 2.0, 'Property5': 1, 'Property6': 3}
        """
        hash_table = Hashtable()
        to = _get_tekla_object(self)
        to.GetAllReportProperties(
            iterable_to_net_array_list(string_names or []),
            iterable_to_net_array_list(float_names or []),
            iterable_to_net_array_list(int_names or []),
            hash_table,
        )
        return hash_table

    def get_dynamic_string_property(self, property_name):
        """
        Get the value of a dynamic string property.

        Parameters
        ----------
        property_name : str
            The name of the property to retrieve.

        Returns
        -------
        str or None
            The value of the specified dynamic string property. None if the property was not found.

        Examples
        -------
        >>> model_object_wrapper = ModelObjectWrapper(some_model_object)
        >>> value = model_object_wrapper.get_dynamic_string_property('property_name')
        """
        to = _get_tekla_object(self)
        was_found, value = to.GetDynamicStringProperty(property_name, str())
        if was_found:
            return value

    def set_multiple_user_properties(self, **kwargs):
        """
        Sets multiple user properties with the specified names to the specified values.

        Parameters
        ----------
        kwargs : dict
            The names and values of the user properties to set.

        Returns
        -------
        bool
            Indicates if the properties were set.

        Examples
        --------
        >>> model_object_wrapper = ModelObjectWrapper(some_model_object)
        >>> model_object_wrapper.set_multiple_user_properties(prop1="value1", prop2=123, prop3=3.14)
        True
        """
        keys_str, values_str, keys_float, values_float, keys_int, values_int = [
            List[_type]() for _type in (str, str, str, float, str, int)
        ]

        for k, v in kwargs.items():
            match v:
                case str():
                    keys_str.Add(k)
                    values_str.Add(v)
                case int():
                    keys_int.Add(k)
                    values_int.Add(v)
                case float():
                    keys_float.Add(k)
                    values_float.Add(v)
        to = _get_tekla_object(self)
        return to.SetUserProperties(
            keys_str, values_str, keys_float, values_float, keys_int, values_int
        )

    def set_dynamic_string_property(self, property_name, value):
        """
        Sets the dynamic string property with the specified name to the specified value.

        Parameters
        ----------
        property_name : str
            The name of the dynamic string property.
        value : str
            The value to set the dynamic string property to.

        Returns
        -------
        bool
            Indicates if the property was set.

        Raises
        ------
        TypeError
            If the value type is not str.

        Examples
        -------
        >>> model_object_wrapper = ModelObjectWrapper(some_model_object)
        >>> model_object_wrapper.set_dynamic_string_property("my_property", "my_value")
        True
        """
        if type(value) != str:
            raise TypeError("'value' must be str")
        to = _get_tekla_object(self)
        return to.GetDynamicStringProperty(property_name, value)


class ModelWrapper(BaseWrapper):
    """Wrapper for the Tekla.Structures.Model.Model class.

    This class provides a convenient interface for interacting with the Tekla Structures Model.
    It has several methods to get objects from the model.

    References
    ----------
        https://developer.tekla.com/tekla-structures/api/22/14382
    """

    main_type = Model

    def __init__(self, tekla_object=None):
        """
        Create a new ModelWrapper instance.

        Examples
        --------
        >>> from pytekla import ModelWrapper
        >>> model = ModelWrapper()
        """
        if tekla_object is None:
            tekla_object = Model()
        super().__init__(tekla_object)
        object.__setattr__(self, "_picker", UI.Picker())
        to = _get_tekla_object(self)
        object.__setattr__(self, "_model_object_selector", to.GetModelObjectSelector())
        object.__setattr__(self, "_ui_model_object_selector", UI.ModelObjectSelector())

    def pick_objects(self, object_type="object", prompt=None):
        """Pick and element from the model.

        Parameters
        ----------
        object_type : str, optional
            The object type to select. Must be one of the following options:
            (object, part, weld, bolt group, reinforcement). By default "object".
        prompt : str, optional
            The string to display as user guidance. By default None.

        Raises
        ------
        ValueError
            If the object_type parameter is incorrect.

        Returns
        -------
        generator
            A generator of [`ModelObjectWrapper`][pytekla.wrappers.ModelObjectWrapper] objects with the selected objects.

        Examples
        -------
        >>> model = ModelWrapper()
        >>> picked_objects = model.pick_objects(object_type="part", prompt="Select parts from the model")
        >>> for obj in selected_element:
        >>>     print(obj)
        """
        try:
            tekla_obj_type = PICKER_OBJECT_TYPES[object_type.lower()]
        except KeyError:
            raise ValueError(
                f"'object_type' must be one of the following options: {list(PICKER_OBJECT_TYPES.keys())}"
            )

        prompt_str = prompt or f"Select one or multiple {object_type}"
        picker = object.__getattribute__(self, "_picker")
        return picker.PickObjects(tekla_obj_type, prompt_str)

    def get_all_objects(self):
        """Get all objects in the model.

        Returns
        -------
        generator
            A generator of [`ModelObjectWrapper`][pytekla.wrappers.ModelObjectWrapper] objects with all the model objects in the current model.

        Examples
        -------
        >>> model = ModelWrapper()
        >>> objects = model.get_all_objects()
        >>> for obj in objects:
        >>>     print(obj)
        """
        selector = object.__getattribute__(self, "_model_object_selector")
        return selector.GetAllObjects()

    def get_selected_objects(self):
        """Get the currently selected objects in the model.

        Returns
        -------
        generator
            A generator of [`ModelObjectWrapper`][pytekla.wrappers.ModelObjectWrapper] objects with the currently selected objects in the model.

        Examples
        -------
        >>> model = ModelWrapper()
        >>> selected_objects = model.get_model_selected_objects()
        >>> for obj in selected_objects:
        >>>     print(obj)
        """
        ms = object.__getattribute__(self, "_ui_model_object_selector")
        return ms.GetSelectedObjects()

    def get_objects_with_types(self, types):
        """Get all objects in the model with specified types.

        Parameters
        ----------
        types : iterable of str
            The object types to retrieve.

        Returns
        -------
        generator
            A generator of [`ModelObjectWrapper`][pytekla.wrappers.ModelObjectWrapper] objects with all the model objects with the specified types in the current model.

        Examples
        -------
        >>> model = ModelWrapper()
        >>> objects = model.get_objects_with_types(["Part", "Weld"])
        >>> for obj in objects:
        >>>     print(obj)
        """
        tekla_types = []
        for _type in types:
            tekla_type = _get_type_by_namespace("Model." + _type)
            tekla_types.append(clr.GetClrType(tekla_type))
        selector = object.__getattribute__(self, "_model_object_selector")
        return selector.GetAllObjectsWithType(tekla_types)

    def get_objects_by_filter(self, model_filter):
        """Get objects from model applying an existing filter.

        Parameters
        ----------
        model_filter : str or Tekla.Structures.Filtering.FilterExpression
            The filter to be applied to the model. It can be a string with the filter name, or a wrapped or unwrapped object of a FilterExpression subclass.

        Returns
        -------
        generator
            A generator of [`ModelObjectWrapper`][pytekla.wrappers.ModelObjectWrapper] objects with the filtered objects in the model.

        Examples
        -------
        >>> model = ModelWrapper()
        >>> filtered_objects = model.get_objects_by_filter("my filter")
        >>> for obj in filtered_objects:
        >>>     print(obj)
        """
        selector = object.__getattribute__(self, "_model_object_selector")
        match (model_filter):
            case str():
                return selector.GetObjectsByFilterName(model_filter)
            case BaseWrapper():
                return selector.GetObjectsByFilter(model_filter.unwrap())
            case _:
                return selector.GetObjectsByFilter(model_filter)

    def get_objects_by_bounding_box(self, min_point_coords, max_point_coords):
        """
        Get objects from the model that are inside a bounding box defined by two points.

        Parameters
        ----------
        min_point_coords : (x: float, y: float, z: float)
            The minimum point coordinates of the bounding box.

        max_point_coords : (x: float, y: float, z: float)
            The maximum point coordinates of the bounding box.

        Returns
        -------
        generator
            A generator of [`ModelObjectWrapper`][pytekla.wrappers.ModelObjectWrapper] objects with the filtered objects in the model.

        Examples
        -------
        >>> model = ModelWrapper()
        >>> min_point = (0.0, 0.0, 0.0)
        >>> max_point = (10.0, 10.0, 10.0)
        >>> filtered_objects = model.get_objects_by_bounding_box(min_point, max_point)
        >>> for obj in filtered_objects:
        >>>     print(obj)
        """
        selector = object.__getattribute__(self, "_model_object_selector")
        return selector.GetObjectsByBoundingBox(
            Point(*min_point_coords), Point(*max_point_coords)
        )


class DrawingDbObjectWrapper(BaseWrapper, WithUserPropertyMixin):
    """
    A wrapper class for Tekla.Structures.Drawing.DataBaseObject subclasses.

    Examples
    --------
    >>> from pytekla import DrawingDbOjectWrapper
    >>> drawing_wrapper = DrawingDbOjectWrapper("Drawing.GADrawing")
    >>> drawing_wrapper.set_user_property('property_name', 'property_value')

    References
    ----------
        https://developer.tekla.com/tekla-structures/api/22/10404
    """

    main_type = DatabaseObject

    def get_all_user_properties(self):
        """
        Return a dictionary containing all of the user-defined properties associated
        with this DatabaseObject object.

        Returns
        -------
        dict
            A dictionary containing the user-defined properties, where the keys are
            the names of the properties and the values are their corresponding values.

        Notes
        -----
        This method retrieves all of the user-defined properties associated with this
        DatabaseObject object, regardless of their data type. The properties are returned as a
        dictionary, where the keys are the property names and the values are their
        corresponding values.

        Examples
        --------
        >>> from pytekla import DrawingWrapper
        >>> drawing_wrapper = DrawingWrapper("GADrawing")
        >>> user_props = drawing_wrapper.get_all_user_properties()
        >>> user_props
        {'property1': 'value1', 'property2': 42, 'property3': 3.14}
        """
        to = _get_tekla_object(self)
        _, string_dict = to.GetStringUserProperties(Dictionary[String, String]())
        _, int_dict = to.GetIntegerUserProperties(Dictionary[String, Int32]())
        _, float_dict = to.GetDoubleUserProperties(Dictionary[String, Double]())

        # it's easier to process the result as a Python dict
        final_dict = {}

        for net_dict in (string_dict, int_dict, float_dict):
            final_dict |= net_idictionary_to_dict(net_dict)

        return final_dict


class DrawingHandlerWrapper(BaseWrapper):
    """
    A wrapper class for Tekla.Structures.Drawing.DrawingHandler.

    Examples
    --------
    >>> from pytekla import DrawingHandlerWrapper
    >>> drawing_handler = DrawingHandlerWrapper()
    >>> drawings = list(drawing_handler.get_drawings())
    >>> active_drawing = drawing_handler.get_active_drawing()

    References
    ----------
        https://developer.tekla.com/tekla-structures/api/22/10647
    """

    main_type = DrawingHandler

    def __init__(self, tekla_object=None):
        """
        Create a new DrawingHandlerWrapper instance.

        Examples
        --------
        >>> from pytekla import DrawingHandlerWrapper
        >>> drawing_handler = DrawingHandlerWrapper()
        """
        if tekla_object is None:
            tekla_object = DrawingHandler()
        super().__init__(tekla_object)

    def get_drawings(self):
        """
        Generate all of the drawing objects in the Tekla model.

        Returns
        -------
        generator
            A generator of [`DrawingDbObjectWrapper`][pytekla.wrappers.DrawingDbObjectWrapper] objects.

        Examples
        --------
        >>> from pytekla import DrawingHandlerWrapper
        >>> drawing_handler = DrawingHandlerWrapper()
        >>> drawings = list(drawing_handler.get_drawings())
        """
        to = _get_tekla_object(self)
        return to.GetDrawings()

    def get_active_drawing(self):
        """
        Return the active drawing object, if one is currently selected.

        Returns
        -------
        DrawingDbObjectWrapper or None
            A DrawingWrapper object for the currently active drawing, or None if
            no drawing is currently active.

        Examples
        --------
        >>> from pytekla import DrawingHandlerWrapper
        >>> drawing_handler = DrawingHandlerWrapper()
        >>> active_drawing = drawing_handler.get_active_drawing()
        """
        to = _get_tekla_object(self)
        active_drawing = to.GetActiveDrawing()
        if active_drawing is not None:
            return active_drawing


def _get_type_by_namespace(namespace):
    """
    Returns the type located at the specified namespace in the Tekla Structures API.

    Parameters
    ----------
    namespace : str
        The namespace of the type to retrieve, using dot notation.

    Returns
    -------
    type
        The type located at the specified namespace.

    Raises
    ------
    AttributeError
        If the type cannot be found at the specified namespace.

    Notes
    -----
    This function retrieves the type located at the specified namespace in the Tekla Structures API using the
    `getattr` built-in function. If the type cannot be found, an `AttributeError` is raised.

    Examples
    --------
    >>> type = get_type_by_namespace("Model.Beam")
    """
    return getattr(Tekla.Structures, namespace)


def wrap(some_object, *args, detect_types=True):
    """
    Wrap the given object with a suitable wrapper class.

    Parameters
    ----------
    some_object : object
        The object to wrap.
    args: object
        Any values that you want to pass to the wrapped object to instanciate it.
    detect_types : bool, optional
        Whether to automatically detect the type of the object and wrap it with an appropriate class.
        Defaults to True.

    Returns
    -------
    object
        The wrapped object.

    Notes
    -----
    This function checks if the given object is a class and returns it unchanged if so. Otherwise, if
    `detect_types` is True, it attempts to determine the type using the namescape path of the object and wrap it with an appropriate
    class. If the object is not a string will try to wrap it with an appropriate class. If the object is not of a known type, it is returned unchanged.

    The possible wrapper classes are:

    - [`BaseWrapper`][pytekla.wrappers.BaseWrapper]: The base wrapper class that other wrappers inherit from. Can wrap any object in the Tekla.Structures namespace.

    - [`ModelObjectWrapper`][pytekla.wrappers.ModelObjectWrapper]: A wrapper for Tekla.Structures.Model.ModelObject subclasses instances.

    - [`ModelWrapper`][pytekla.wrappers.ModelWrapper]: A wrapper for Tekla.Structures.Model.Model instances.

    - [`DrawingDbObjectWrapper`][pytekla.wrappers.DrawingDbObjectWrapper]: A wrapper for Tekla.Structures.Drawing.DatabaseObject subclasses instances.

    - [`DrawingHandlerWrapper`][pytekla.wrappers.DrawingHandlerWrapper]: A wrapper for Tekla.Structures.Drawing.DrawingHandler instances.

    Examples
    --------
    >>> wrapped_obj = wrap("Model.Model")
    >>> # ModelWrapper instance

    >>> wrapped_obj = wrap("Model.Beam")
    >>> # ModelObjectWrapper

    >>> from Tekla.Structures.Model import Beam
    >>> wrapped_obj = wrap(Beam())
    >>> # ModelObjectWrapper
    """
    unwrapped_args = [a.unwrap() if isinstance(a, BaseWrapper) else a for a in args]

    if inspect.isclass(some_object):
        return some_object

    if detect_types:
        if isinstance(some_object, str):
            if "Enum" in some_object:
                some_object_splitted = some_object.split(".")
                some_object = ".".join(some_object_splitted[:-1])
                some_object_type = _get_type_by_namespace(some_object)
                return BaseWrapper(getattr(some_object_type, some_object_splitted[-1]))

            some_object_type = _get_type_by_namespace(some_object)
            clr_type = clr.GetClrType(some_object_type)
            if clr_type.IsAbstract and clr_type.IsSealed:
                return BaseWrapper(some_object_type)
            some_object = some_object_type(*unwrapped_args)

    class_to_use = None

    for subclass in BaseWrapper.__subclasses__():
        if isinstance(some_object, subclass.main_type):
            class_to_use = subclass

    new_instance = None

    if class_to_use is not None:
        new_instance = class_to_use(some_object)
        return new_instance

    cls_name = str(some_object.__class__)

    if "Tekla.Structures" in cls_name:
        new_instance = BaseWrapper(some_object)
        return new_instance

    return some_object


__all__ = [
    "BaseWrapper",
    "ModelObjectWrapper",
    "ModelWrapper",
    "DrawingDbObjectWrapper",
    "DrawingHandlerWrapper",
    "wrap",
]
