import string
from time import sleep

def script(str):
    sleep(0.1)
    return foo(str)


def foo(str):
    return 'translated: ' + string.capwords(str)
