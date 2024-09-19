# -*- coding: utf-8 -*-
# @Date:2022/07/03 0:23
# @Author: Lu
# @Description convert utils
from os import PathLike
from typing import List

_global_encodes = [None, 'utf-8', 'gbk', 'gb18030', 'gb2312']


def read_bin(file_path: int|str|bytes|PathLike[bytes]|PathLike[str]) -> bytes:
    f = open(file_path, 'rb')
    binary = f.read()
    f.close()
    return binary


def read_text(file_path: int|str|bytes|PathLike[bytes]|PathLike[str]) -> str:
    f = open(file_path, 'rb')
    binary = f.read()
    f.close()
    return bin2text(binary)


def bin2text(binary: bytes, encodes: List = None) -> str:
    if type(binary) is str:
        return binary
    encodes = _global_encodes if not encodes else encodes
    for en in encodes:
        try:
            text = binary.decode(encoding=en)
            return text
        except Exception as e:
            pass


def text2bin(text: str, encodes: List = None) -> bytes:
    if type(text) is bytes:
        return text
    encodes = _global_encodes if not encodes else encodes
    for en in encodes:
        try:
            binary = text.encode(en)
            return binary
        except Exception as e:
            pass
