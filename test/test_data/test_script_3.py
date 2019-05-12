import json


def script(msg):
    d = json.loads(msg)
    d['test'] = 'test_data'
    return d
