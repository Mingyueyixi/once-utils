from ._convert import *
from ._pymodule import *
from ._cmd import *


def find(lst, fn):
    return next(x for x in lst if fn(x))
