## Dataframes

Retrieve elements from the model using an existing filter, create a Pandas dataframe, group the elements by Material, Profile and Name, calculate the total weight for each group, and export the result to an Excel file.

```python
from pytekla import wrap
from pytekla.data_manager import create_model_objects_dataframe

model = wrap("Model.Model")

steel_parts = model.get_objects_by_filter("Steel_Main_Part-All")

report_properties = { 
    "PROFILE": str,
    "MATERIAL": str,
    "WEIGHT_NET": float,
}

attributes = ["name"]

dataframe = create_model_objects_dataframe(steel_parts, report_properties=report_properties, attributes=attributes)

dataframe = dataframe.rename(columns={"PROFILE": "PROFILE", "MATERIAL": "MATERIAL", "name": "NAME", "WEIGHT_NET": "WEIGHT [kG]"})

grouped_dataframe = dataframe.groupby(["MATERIAL", "PROFILE", "NAME"]).agg({"WEIGHT [kG]": "sum"})

grouped_dataframe.to_excel("dataframe.xlsx")
```