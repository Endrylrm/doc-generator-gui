import json


class JsonReader:
    """
    This class is responsible for loading the company
    data to our State.
    """

    @staticmethod
    def Load(path: str):
        with open(path, "r", encoding="utf-8") as file:
            json_data = json.loads(file.read())

        return json_data
