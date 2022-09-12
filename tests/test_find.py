# -*- coding: utf-8 -*-
import onceutils


def test_find():
    lst = []
    for i in range(10):
        lst.append({'name': i, 'value': f"value_{i}"})
    ele = onceutils.find(lst, lambda e: e['name'] == 8)
    print(ele)
    assert ele['name'] == 8
