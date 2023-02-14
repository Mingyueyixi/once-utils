# -*- coding: utf-8 -*-
# @Date:2021/07/15 9:44
# @Author: Lu
# @Description
import io
import os
import subprocess
import tempfile
import time
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union

import httpx
import requests

from onceutils import bin2text, text2bin


def run_cmd(cmd, prt=True):
    if prt:
        print(cmd)
    p = os.popen(cmd)
    result = p.read()
    p.close()
    return result


class Shell(object):
    def __init__(self, shell_args='sh'):
        self.proc: subprocess.Popen = None
        self.shell_args = shell_args
        self.pool = ThreadPoolExecutor(max_workers=6)

    def run(self, cmd: str, timeout: Union[set, list, int] = (5, 5)):
        """
        Run cmd by the same process.
        The result is only use on develop, because it was not unreliable
        :param cmd: command line
        :param timeout: read break when it timeout
        :return: command's output
        """
        if not cmd:
            return
        if type(timeout) is int:
            timeout = (timeout, timeout)
        if not self.proc or self.proc.stdout.closed:
            std_out = self.stdout_io()
            std_err = self.stderr_io()
            self.proc = subprocess.Popen(args=self.shell_args,
                                         shell=True,
                                         text=False,
                                         start_new_session=True,
                                         stdin=subprocess.PIPE,
                                         stdout=std_out,
                                         stderr=std_err)
            # print('>>> init Popen')
            self.proc.stdout = std_out
            self.proc.stderr = std_err

        proc: subprocess.Popen = self.proc
        # exec command line
        b_cmd = text2bin(cmd)
        proc.stdin.write(b_cmd + b'\n')
        proc.stdin.flush()

        # read result
        content = b''
        error = None
        try:
            content = Shell._read_std_io(proc.stdout, timeout[0])
        except TimeoutError as e:
            # traceback.print_exc()
            pass
        finally:
            proc.stdout.close()
        try:
            error = Shell._read_std_io(proc.stderr, timeout[1])
        except TimeoutError as e:
            # traceback.print_exc()
            pass
        finally:
            proc.stderr.close()
        proc.terminate()
        return bin2text(content), bin2text(error)

    @classmethod
    def _read_std_io(cls, std_io: io.FileIO, timeout: int):
        content = b''
        if not std_io:
            return content
        curr_time = time.time()
        while True:
            std_io.seek(0)
            rc = std_io.read()
            if rc:
                content = rc
                break
            if time.time() - curr_time > timeout:
                raise TimeoutError(f'read std_io timeout > {timeout}s')
            time.sleep(0.1)
        std_io.seek(0)
        std_io.truncate()
        return content

    def close(self):
        proc = self.proc
        proc.terminate()
        if not proc.stdout: proc.stdout.close()
        if not proc.stderr: proc.stderr.close()

    def stdout_io(self):
        # close时自动删除临时文件
        return tempfile.NamedTemporaryFile(mode='w+b', suffix='.txt', delete=True)
        # return io.open('stdout.txt', mode='wb+')

    def stderr_io(self):
        # close时自动删除临时文件
        return tempfile.NamedTemporaryFile(mode='w+b', suffix='.txt', delete=True)
        # return io.open('stdout.txt', mode='wb+')
