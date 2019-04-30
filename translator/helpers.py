import json
from pathlib import Path
from copy import deepcopy


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


def element_from_path(dictionary, list_path):
    l = deepcopy(list_path)
    key = l.pop(0)
    if len(l) > 0:
        return element_from_path(dictionary[key], l)
    else:
        return dictionary[key]


def set_element_from_path(dictionary, list_path, value):
    def recursion(d, l):
        key = l.pop(0)
        if len(l) > 0:
            return recursion(d[key], l)
        else:
            d[key] = value

    l_aux = deepcopy(list_path)
    d_aux = deepcopy(dictionary)
    recursion(d_aux, l_aux)
    return d_aux


