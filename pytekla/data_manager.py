import pandas as pd


def create_model_objects_dataframe(
    objects,
    report_properties=None,
    user_properties=None,
    attributes=None,
    use_all_user_properties=False,
):
    """
    Create a pandas DataFrame from objects based on provided properties and attributes.

    Parameters
    ----------
    objects : iterable of ModelObjectWrapper
        A iterable of objects to be transformed into a DataFrame.
    report_properties : dict, optional
        A dictionary of report properties to be extracted from each object, with key being the report property name and value being the report property type. Default is None.
    user_properties : dict, optional
        A dictionary of user properties to be extracted from each object, with key being the user property name and value being the user property type. Default is None.
    attributes : list, optional
        A list of object attributes to be extracted from each object. Default is None.
    use_all_user_properties : bool, optional
        A flag indicating if all user properties should be extracted from each object. If set to True, the `user_properties` parameter will be ignored. Default is False.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the extracted information.

    Examples
    --------
    >>> objects = [obj1, obj2, obj3]
    >>> report_properties = {'prop1': int, 'prop2': str}
    >>> user_properties = {'prop3': float, 'prop4': str}
    >>> attributes = ['attr1', 'attr2', 'attr2.attr3']
    >>> create_dataframe(objects, report_properties, user_properties, attributes)
        prop1 prop2  prop3 prop4  attr1  attr2  attr3
        0     1    A   3.14    B1   1.0   0.5   0.7
        1     2    C   6.28    B2   2.0   1.0   1.1
        2     3    E   9.42    B3   3.0   1.5   1.5
    """
    data = []
    for obj in objects:
        obj_data = {}

        if report_properties:
            for report_prop_name, report_prop_type in report_properties.items():
                obj_data[report_prop_name] = obj.get_report_property(
                    report_prop_name, report_prop_type
                )

        if user_properties or use_all_user_properties:
            if use_all_user_properties:
                obj_data |= obj.get_all_user_properties()
            else:
                for user_prop_name, user_prop_type in user_properties.items():
                    obj_data[user_prop_name] = obj.get_user_property(
                        user_prop_name, user_prop_type
                    )

        if attributes:
            for attr in attributes:
                attrs = attr.split(".")
                current_obj = obj
                for at in attrs:
                    current_obj = getattr(current_obj, at, None)
                    if callable(current_obj):
                        current_obj = current_obj()
                obj_data[attr] = current_obj

        data.append(obj_data)

    return pd.DataFrame(data)
