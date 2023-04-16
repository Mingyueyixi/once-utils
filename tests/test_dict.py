# -*- coding: utf-8 -*-
# @Date:2023/04/16 13:49
# @Author: Lu
# @Description
from onceutils import got


def test_got():
    a = {}
    assert got(a, ["event"], "123") == "123"
    assert got(a, ["event", "commits"], "abc") == "abc"
