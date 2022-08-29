from onceutils import Shell


def test_shell():
    shell = Shell('bash')
    res = shell.run("python --version")
    print(res)
    res = shell.run("gradle build", timeout=5)
    print(res)
    res = shell.run("git --version", timeout=3)
    print(res)
    shell.close()
