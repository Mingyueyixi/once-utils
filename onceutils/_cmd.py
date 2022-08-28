# -*- coding: utf-8 -*-
# @Date:2021/07/15 9:44
# @Author: Lu
# @Description
import io
import subprocess
import tempfile
import time
from concurrent.futures.thread import ThreadPoolExecutor

from onceutils import bin2text, text2bin


class Shell(object):
    def __init__(self, shell_args='sh'):
        self.proc: subprocess.Popen = None
        self.shell_args = shell_args
        self.pool = ThreadPoolExecutor(max_workers=6)

    def run(self, cmd: str, timeout=5):
        if not cmd:
            return
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
            content = Shell._read_std_io(proc.stdout, timeout)
        except TimeoutError as e:
            proc.stdout.close()
            try:
                error = Shell._read_std_io(proc.stderr, 0)
            except TimeoutError as e:
                proc.stdout.close()
                proc.terminate()
        # fu1 = self.pool.submit(self._read_std_io, proc.stdout, timeout)
        # fu2 = self.pool.submit(self._read_std_io, proc.stderr, timeout)
        # try:
        #     content = fu1.result(timeout)
        #     error = fu2.result(timeout)
        # except Exception as e:
        #     pass
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
                raise TimeoutError(f'read std_io timeout({timeout}/s)')
                break
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


def test_shell():
    shell = Shell('bash')
    res = shell.run("python --version")
    print(res)
    res = shell.run("gradle build", timeout=5)
    print(res)
    res = shell.run("git --version", timeout=3)
    print(res)
    shell.close()
