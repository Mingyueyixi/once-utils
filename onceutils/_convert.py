# -*- coding: utf-8 -*-
# @Date:2022/07/03 0:23
# @Author: Lu
# @Description convert utils
from os import PathLike
from pathlib import Path
from typing import List, Union

_global_encodes = [None, 'utf-8', 'gbk', 'gb18030', 'gb2312']


def read_bin(file_path: Union[int, str, bytes, PathLike]) -> bytes:
    """
    Read a file in binary mode.

    Args:
        file_path (Union[int, str, bytes, PathLike[bytes], PathLike[str]]):
            The path of the file to be read, which can be an integer (file descriptor),
            a string, a byte sequence, or an os.PathLike object.

    Returns:
        bytes:
            The binary data of the file content that has been read.

    Raises:
        FileNotFoundError:
            If the specified file does not exist.
        PermissionError:
            If there is not enough permission to access the file.
        IOError:
            If any other input/output error occurs.
    """
    # Open the file in binary reading mode
    f = open(file_path, 'rb')
    # Read the binary content of the file
    binary = f.read()
    # Close the file
    f.close()
    # Return the binary content
    return binary


def read_text(file_path: Union[int, str, bytes, PathLike]) -> str:
    """
    Read a file in text mode and convert its content to a string.

    Args:
        file_path (Union[int, str, bytes, PathLike[bytes], PathLike[str]]):
            The path of the file to be read, which can be an integer (file descriptor),
            a string, a byte sequence, or an os.PathLike object.

    Returns:
        str:
            The string representation of the file content that has been read.

    Raises:
        FileNotFoundError:
            If the specified file does not exist.
        PermissionError:
            If there is not enough permission to access the file.
        IOError:
            If any other input/output error occurs.
    """
    # Open the file in binary reading mode
    f = open(file_path, 'rb')
    # Read the binary content of the file
    binary = f.read()
    # Close the file
    f.close()
    # Convert the binary content to text using the bin2text function
    return bin2text(binary)


def bin2text(binary: bytes, encodes: List = None) -> str:
    """
    Convert binary data to text.

    Args:
        binary (bytes):
            The binary data to be converted to text.
        encodes (List, optional):
            A list of encodings to try when converting the binary data to text.
            If not provided, a default list of encodings will be used.

    Returns:
        str:
            The text representation of the binary data.

    Raises:
        UnicodeDecodeError:
            If the binary data cannot be decoded using any of the provided encodings.
    """
    # If the input is already a string, return it directly
    if type(binary) is str:
        return binary
    # If no encoding list is provided, use the default list
    encodes = _global_encodes if not encodes else encodes
    # Iterate through each encoding in the list
    for en in encodes:
        try:
            # Attempt to decode the binary data using the current encoding
            text = binary.decode(encoding=en)
            # If successful, return the decoded text
            return text
        except Exception as e:
            # If decoding fails, catch the exception and continue to the next encoding
            pass


def text2bin(text: str, encodes: List = None) -> bytes:
    """
    Convert text to binary data.

    Args:
        text (str):
            The text to be converted to binary data.
        encodes (List, optional):
            A list of encodings to try when converting the text to binary data.
            If not provided, a default list of encodings will be used.

    Returns:
        bytes:
            The binary representation of the text.

    Raises:
        UnicodeEncodeError:
            If the text cannot be encoded using any of the provided encodings.
    """
     # If the input is already a byte sequence, return it directly
    if type(text) is bytes:
        return text
    # If no encoding list is provided, use the default list
    encodes = _global_encodes if not encodes else encodes
    # Iterate through each encoding in the list
    for en in encodes:
        try:
            # Attempt to encode the text using the current encoding
            binary = text.encode(encoding=en)
            # If successful, return the encoded binary data
            return binary
        except Exception as e:
            # If encoding fails, catch the exception and continue to the next encoding
            pass
