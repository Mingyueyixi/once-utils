# -*- coding: utf-8 -*-
# @Date:2022/08/28 2:41
# @Author: Lu
# @Description json encoder util

import json
from json import JSONEncoder


class XJSONEncoder(JSONEncoder):
    """
    A ext JSONEncoder for support set, or an object who has '__dict__' attr
    """

    def default(self, o):
        if isinstance(o, set):
            return list(o)
        try:
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, o)
        except TypeError:
            pass
        if hasattr(o, '__dict__'):
            return o.__dict__
        raise TypeError(f'Object of type {o.__class__.__name__} '
                        f'is not JSON serializable')
