# -*- coding: utf-8 -*-
# @Date:2022/09/24 13:45
# @Author: Lu
# @Description
import random
import re
import sys

import onceutils


def test_random_int_list():
    size, min_v, max_v = 1000, -100, 100
    lst = onceutils.random_int_list(size, min_v, max_v)
    print(lst)

    assert len(lst) == size
    for ele in lst:
        assert type(ele) is int
        assert ele <= max_v
        assert ele >= min_v


def test_random_float_list():
    size, min_v, max_v = 1000, -100, 100
    lst = onceutils.random_float_list(size, min_v, max_v)
    print(lst)

    assert len(lst) == size
    for ele in lst:
        assert type(ele) is float
        assert ele <= max_v
        assert ele >= min_v


def test_random_chinese_name():
    for i in range(1000):
        name = onceutils.random_chinese_full_name()
        print(name)
