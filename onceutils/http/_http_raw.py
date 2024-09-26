# -*- coding: utf-8 -*-
# @Date:2022/05/19 15:34
# @Author: Lu
# @Description
from typing import Union

from onceutils import bin2text, text2bin


class HttpRaw(object):

    def __int__(self):
        self.bin: bytes = None
        self.headers: dict = None
        self.body: bytes = None

        self.first_line_bound: tuple = (0, 0)
        self.header_bound: tuple = (0, 0)
        self.body_bound: tuple = (0, 0)

    def __str__(self):
        return bin2text(self.bin)


class _CommonParse(object):

    def parse(self, raw: HttpRaw, binary: bytes):
        raw.bin = binary
        self.collect_bound(raw, binary)
        self.parse_header(raw)
        self.parse_body(raw)
        return raw

    def collect_bound(self, raw: HttpRaw, binary: bytes):
        first_line_end = binary.find(b'\n')
        if first_line_end == -1:
            return raw
        raw.first_line_bound = (0, first_line_end)

        # 提取取header end索引
        header_start = first_line_end + 1
        header_end = binary.find(b'\n\n', header_start)
        if header_end == -1:
            header_end = binary.find(b'\n\r', header_start)
        if header_end == -1:
            return raw

        raw.header_bound = (header_start, header_end)
        # body
        raw.body_bound = (header_end + 1, len(binary))

    def parse_body(self, raw: HttpRaw):
        start, end = raw.body_bound
        raw.body = raw.bin[start: end]

    def parse_header(self, raw: HttpRaw):
        headers = {}
        start, end = raw.header_bound
        header_bin = raw.bin[start: end]
        header_text = bin2text(header_bin)

        lines = header_text.splitlines(keepends=True)
        for i in range(len(lines)):
            line = lines[i]
            split_index = line.find(":")
            if split_index == -1:
                continue

            k: str = line[:split_index].strip()
            v: str = line[split_index + 1:].strip()
            headers[k] = v
        raw.headers = headers


class HttpRequestParse(HttpRaw):
    def __init__(self):
        super(HttpRequestParse, self).__init__()
        self.path = None
        self.method = None
        self.protool = None

    def parse(self, file_path=None, content=Union[str, bytes]):
        binary = None
        if file_path:
            with open(file_path, 'rb') as f:
                binary = f.read()
        elif type(content) == str:
            binary = text2bin(content)
        else:
            binary = content

        _CommonParse().parse(self, binary)
        self.parse_first_line()
        return self

    def parse_first_line(self):
        """
        parse first line
        """
        start, end = self.first_line_bound
        line: str = bin2text(self.bin[start: end])
        if not line:
            return
        infos = line.split(" ")
        self.method = infos[0]
        self.path = infos[1]
        self.protool = infos[2]


class HttpResponseParse(HttpRaw):
    def __init__(self):
        super(HttpResponseParse, self).__init__()
        self.protool = None
        self.code = None
        self.des = None

    def parse(self, file_path=None, content=Union[str, bytes]):
        binary = None
        if file_path:
            with open(file_path, 'rb') as f:
                binary = f.read()
        elif type(content) == str:
            binary = text2bin(content)
        else:
            binary = content
        _CommonParse().parse(self, binary)
        self.parse_first_line()
        return self

    def parse_first_line(self):
        """
        parse first line
        """
        start, end = self.first_line_bound
        line: str = bin2text(self.bin[start:end])
        if not line:
            return
        infos = line.split(" ")
        try:
            self.protool = infos[0]
            self.code = infos[1]
            self.des = infos[2]
        except Exception as e:
            pass

    @property
    def status_code(self):  # self.protool = infos[0]
        return int(self.code)


def parse_http_request(file_path=None, content=Union[str , bytes]) -> HttpRequestParse:
    return HttpRequestParse().parse(file_path, content)


def parse_http_response(file_path=None, content=Union[str , bytes]) -> HttpResponseParse:
    return HttpResponseParse().parse(file_path, content)
