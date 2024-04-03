from models.sablon_model import SablonModel
import pytest


@pytest.mark.parametrize("sablon_input, sablon_output", [
    ({"name": "Name_One",
      "age": 30,
      "gender": "Non_Binary"}, {"name": "Name_One",
                                "age": 30,
                                "gender": "Non_Binary"}),
    ({"name": "Name_Two",
      "age": 35}, {"name": "Name_Two",
                   "age": 35,
                   "gender": None
                   }),
    ({"name": "Name_Three",
      "gender": "Golden_Shower_Unicorn"}, {"name": "Name_Three",
                                           "age": None,
                                           "gender": "Golden_Shower_Unicorn"})
])
def test_sablon_model(sablon_input, sablon_output):
    sablon = SablonModel(**sablon_input)
    print(f"\n\033[94mModel: \033[92mSablon model: \033[96m{sablon}\033[0m\n")
    for key, value in sablon_output.items():
        assert getattr(sablon, key) == value

#     assert sablon.name == sablon_output["name"]
#     assert sablon.age == sablon_output["age"]
#     assert sablon.gender == sablon_output["gender"]
