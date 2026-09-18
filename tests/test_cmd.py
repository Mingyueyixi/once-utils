import os.path
from pathlib import Path

import onceutils
from onceutils import SameProcessShell


def test_shell():
    shell = onceutils.Shell()
    text = "xxx"
    temp_f = Path(__file__).parent / "data/test_cmd_temp.txt"
    shell.run(f'echo {text} > {str(temp_f)}', cwd=Path(__file__).parent)
    assert text == temp_f.read_text().strip()


def test_same_process_shell():
    shell = SameProcessShell('sh')
    res, err = shell.run("python --version", timeout=(5, 1))
    pid = shell.proc.pid
    print(res, err)
    # res, err = shell.run("gradle build", timeout=(5, 2))
    # print(res, err)
    assert pid == shell.proc.pid
    res, err = shell.run("git --version", timeout=(5, 3))
    print(res, err)
    assert pid == shell.proc.pid
    shell.close()


def test_run_cmd():
    script_name = os.path.basename(__file__)
    fold = os.path.dirname(__file__)
    assert script_name in onceutils.run_cmd(f'ls {fold}')
