# -*- coding: utf-8 -*-
# @Date:2023/04/16 13:48
# @Author: Lu
# @Description

def got(item: dict, keys: [], default=None):
    result = default
    ele = item
    try:
        for k in keys:
            result = ele[k]
            ele = result
    except Exception as e:
        pass
    return result


