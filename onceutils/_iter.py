# -*- coding: utf-8 -*-
# Author:Lu
# Date:2022/9/19
# Description:
from typing import List


def find(lst: List, fn) -> int:
    for index, ele in enumerate(lst):
        if fn(ele):
            return index


def have(lst: List, fn) -> bool:
    for ele in lst:
        if fn(ele):
            return True


def filter(it: list | dict, fn):
    index = find(it, fn)
    if index >= 0:
        return list[index]
