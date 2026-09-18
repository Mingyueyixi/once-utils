# -*- coding: utf-8 -*-
# Author:Lu
# Date:2022/9/19
# Description:
import builtins
from typing import List


def find(lst: List, fn) -> int:
    for index, ele in enumerate(lst):
        if fn(ele):
            return index


def have(iterable, fn) -> bool:
    for ele in iterable:
        if fn(ele):
            return True


def filter2list(iterable, fn) -> List:
    return [e for e in filter(fn, iterable)]
