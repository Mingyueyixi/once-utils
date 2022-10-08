from onceutils import Shell


def test_shell():
    shell = Shell('bash')
    res, err = shell.run("python --version", timeout=(5, 1))
    print(res)
    res, err = shell.run("gradle build", timeout=(5, 2))
    print(res)
    print(err)
    res, error = shell.run("git --version", timeout=(5, 3))
    print(res)
    shell.close()
