# -*- coding: utf-8 -*-
# Author:Lu
# Date:2024/5/9 11:46 
# Description:
import json

from onceutils import parse_http_request
from onceutils.http import parse_http_response
from tests.resource import Res


def test_http_response_parser():
    httpRaw = parse_http_response(content=Res.read_text("data/http.resp.raw.txt"))
    assert httpRaw.status_code == 200
    assert json.loads(httpRaw.body).get("code") == "1"


def test_http_request_parser():
    httpRaw = parse_http_request(content=Res.read_text("data/http.req.raw.txt"))
    assert httpRaw.method == "GET"
    assert len(httpRaw.headers) > 0
