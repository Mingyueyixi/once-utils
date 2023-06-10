# -*- coding: utf-8 -*-
# @Date:2023/06/10 15:09
# @Author: Lu
# @Description
import json

from onceutils.xjson import XJSONEncoder
from onceutils.xjson._common import from_json, to_json


class Meet(object):
    def __init__(self, a=123, b=1234):
        self.a = a
        self.b = b


def test_dumps_object():
    json_text = json.dumps(Meet(), cls=XJSONEncoder, indent=2)
    print(json_text)


def test_dumps_dict():
    result = {"a": set(), "b": set()}
    json_text = json.dumps(result, cls=XJSONEncoder, indent=2)
    print(json_text)


def dict_to_object(o: dict):
    result = object.__new__(Meet)
    for k, v in o.items():
        if isinstance(v, list):
            v = set(v)
        result.__dict__[k] = v
    return result


def test_load_as_set():
    json_dict = json.loads('{"a":[123, "a"]}', object_hook=dict_to_object)
    print(json_dict)


def test_from_json():
    obj = from_json('{"a":[123, "a"]}', Meet)
    assert isinstance(obj, Meet)
    assert obj.a[0] == 123
    assert obj.a[1] == "a"

    obj = from_json('{"a":[123, "a"]}')
    assert isinstance(obj, dict)
    assert isinstance(obj['a'], list)

    obj = from_json('[1,2,3]', list)
    assert isinstance(obj, list)
    assert len(obj) == 3
    assert obj[0] == 1

    obj = from_json('[1,2,3]', set)
    assert isinstance(obj, set)
    assert len(obj) == 3

    obj = from_json('[1,2,3]', tuple)
    assert len(obj) == 3
    assert obj[0] == 1


def test_to_json():
    meet = Meet("a", "b")
    json_text = to_json(meet)
    assert '"a"' in json_text
    assert '"b"' in json_text
    assert '\n' in json_text

    json_text = to_json(meet, indent=None)
    assert '"a"' in json_text
    assert '"b"' in json_text
    assert '\n' not in json_text