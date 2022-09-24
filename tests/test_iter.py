# -*- coding: utf-8 -*-
import random

import onceutils


def test_find():
    lst = []
    for i in range(10):
        lst.append({'name': i, 'value': f"value_{i}"})
    index = onceutils.find(lst, lambda e: e['name'] == 8)
    assert lst[index]['name'] == 8


def test_have():
    lst_size = 10
    lst = [random.randint(0, 1) for i in range(lst_size)]
    ret = onceutils.have(lst, lambda e: e == 1)
    assert ret


def test_filter():
    ele = onceutils.filter(['b', 2, 'b', 4], lambda e: e == 'b')
    arr = ['b', 'b']
    assert not id(ele) == id(arr)
    assert ele == arr
