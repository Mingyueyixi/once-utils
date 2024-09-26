# -*- coding: utf-8 -*-
# @Date:2023/06/10 16:15
# @Author: Lu
# @Description
import json
from typing import Type, Union

from onceutils.xjson import XJSONEncoder


def from_json(s: Union[str , bytes], clazz: Type[object] = None, *,
              cls=None, object_hook=None, parse_float=None,
              parse_int=None, parse_constant=None,
              object_pairs_hook=None, **kwargs) -> Type:
    json_result = json.loads(s, cls=cls,
                             object_hook=object_hook, parse_float=parse_float,
                             parse_int=parse_int, parse_constant=parse_constant,
                             object_pairs_hook=object_pairs_hook, **kwargs)
    if not clazz:
        return json_result

    result = None
    if isinstance(json_result, dict):
        if issubclass(clazz, dict):
            # dict not have __dict__ attr
            result: dict = clazz(json_result)
        elif issubclass(clazz, set):
            result: set = clazz(json_result)
        elif issubclass(clazz, tuple):
            result: tuple = clazz(json_result)
        elif issubclass(clazz, list):
            raise Exception(f"json dict can't convert to list,{clazz}")
        else:
            # __new__ fuction not need fill __init__ func 's params
            result = clazz.__new__(clazz)
            for k, v in json_result.items():
                result.__dict__[k] = v

    else:
        result: clazz = clazz(json_result)
    return result


def to_json(obj, *, indent=2, ensure_ascii=False, **kwargs):
    json_text = json.dumps(obj, cls=XJSONEncoder, indent=indent, ensure_ascii=ensure_ascii, **kwargs)
    return json_text
