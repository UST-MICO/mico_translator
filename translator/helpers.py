import json
from pathlib import Path


def load_json(path):
    with open(str(path)) as file:
        params = json.load(file)
    return params


def get_project_root():
    import inspect, os
    return Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) / '..'


def load_test_data(filename):
    with open(Path(get_project_root()) / 'test' / 'test_data' / filename, 'r') as file:
        data = file.read()
    return data

