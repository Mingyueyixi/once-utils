# -*- coding: utf-8 -*-
# @Date:2022/08/27 20:06
# @Author: Lu
# @Description: Quick set github project's url with a personal access token.
# Different from normal login,
# the token with url will be stored in the project git file which path is .git/config,
# so you should only run the program in a trusted environment.
# Example: python -m onceutils.github.personal_token -u xxxUser -t xxxToken

import argparse
import os.path
import re
from typing import List

from onceutils import run_cmd


class _RemoteEntity(object):
    def __init__(self, name: str):
        self.name: str = name
        self.push: set = set()
        self.fetch: set = set()

    def __getitem__(self, key):
        return self.__dict__.get(key)


class PersonalTokenHandler(object):
    def __init__(self, config: dict = None):
        self.config: dict = config

    def start(self, projects: str):
        for p in projects:
            self.handle(p)

    def handle(self, project_path):
        cwd_bak = os.getcwd()
        print(project_path)
        remote = self.parse_remote_url(project_path)

        for name, remote, in remote.items():
            if not remote.fetch == remote.push:
                print(f"{remote.name} fetch and push urls is not match !!")
                continue
            for fetch_url in remote.fetch:
                fetch_url: str
                m = re.search(r'^https://github.com/([^/]*)/', fetch_url)
                if not m:
                    print(f'fetch url({fetch_url}) is not start with https://github.com')
                    continue
                user = m.group(1)
                if user not in self.config.keys():
                    print(f'{user} is not in config({list(self.config.keys())})')
                    continue
                p_token = self.config.get(user)
                if not p_token:
                    print(f'config is empty')
                    continue
                fetch_url_new = re.sub(r'https://', f'https://{p_token}@', fetch_url)
                os.chdir(project_path)
                run_cmd(f'git remote set-url {remote.name} {fetch_url_new}')
                # print(f'{fetch_url} >>> {fetch_url_new}')

        os.chdir(cwd_bak)

    def parse_remote_url(self, project_path) -> {str: _RemoteEntity}:
        content = run_cmd(f'cd {project_path} && git remote -v')
        print(content)

        result: {str: [_RemoteEntity]} = {}
        for line in content.splitlines():
            name, url, flag = re.split(r'[\t ]', line)
            flag = flag[1:-1]
            index = ['fetch', 'push'].index(flag)
            if index == -1:
                raise Exception('git remote -v parse error')
            item: _RemoteEntity = result.get(name)
            if not item:
                item = _RemoteEntity(name)
                result[name] = item
            item[flag].add(url)
        # print(xjson.dumps(result, cls=XJSONEncoder))
        return result


class Nima(object):
    def __init__(self):
        pass


def test_personal_token_handler():
    PersonalTokenHandler({
        'Mingyueyixi': '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'
    }).start(['xx'])


def find_git_project_paths(work_path: str) -> List:
    if not work_path:
        work_path = './'

    result = []
    abs_work_path = os.path.abspath(work_path)
    for child in os.listdir(work_path):
        abs_child_path = os.path.join(abs_work_path, child)
        if not os.path.isdir(abs_child_path):
            continue
        if child == '.git':
            result.append(abs_work_path)
            continue

        for cp in os.listdir(abs_child_path):
            abs_cp = os.path.join(abs_child_path, cp)
            if not os.path.isdir(abs_cp):
                continue
            if cp == '.git':
                result.append(abs_cp)
    return result


def main():
    parser = argparse.ArgumentParser(description="""Quick set github project's url with a personal access token.""",
                                     add_help=True)
    parser.add_argument('-p', '--path', dest='path', action='store', help='set work patch to find projects')
    parser.add_argument('-u', '--user', dest='user', action='store', help='set user', required=True)
    parser.add_argument('-t', '--token', dest='token', action='store', help='set token', required=True)
    args = parser.parse_args()
    work_path = args.path
    projects = find_git_project_paths(work_path)
    print(projects)
    user = args.user
    token = args.token

    print(user)

    PersonalTokenHandler({
        user: token
    }).start(projects)


if __name__ == '__main__':
    main()
