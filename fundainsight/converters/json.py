import json


def json_to_tuples(json_string) -> tuple:
    try:
        json_string = json_string.replace("'", '"')
        data = json.loads(json_string)
        if isinstance(data, list):
            return tuple(data)
        elif isinstance(data, dict):
            return tuple(data.items())
        else:
            print("JSON data is not a list or dictionary, unable to convert to tuple.")
            return ()
    except Exception as e:
        print("Error converting from JSON:", e)
        raise e
