# -*- coding: utf-8 -*-
# @Date:2022/08/27 20:06
# @Author: Lu
# @Description quick set github project's url with a personal access token
import json
import os.path
import re

from onceutils._cmd import Shell, run_cmd
from onceutils.xjson.encoder import XJSONEncoder


class _Remote(object):
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
                    print(f'{user} is in config({list(self.config.keys())})')
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

    def parse_remote_url(self, project_path) -> {str: _Remote}:
        content = run_cmd(f'cd {project_path} && git remote -v')
        print(content)

        result: {str: [_Remote]} = {}
        for line in content.splitlines():
            name, url, flag = re.split(r'[\t ]', line)
            flag = flag[1:-1]
            index = ['fetch', 'push'].index(flag)
            if index == -1:
                raise Exception('git remote -v parse error')
            item: _Remote = result.get(name)
            if not item:
                item = _Remote(name)
                result[name] = item
            item[flag].add(url)
        # print(xjson.dumps(result, cls=XJSONEncoder))
        return result


class Nima(object):
    def __init__(self):
        pass


def test_personal_token_handler():
    PersonalTokenHandler({
        'Mingyueyixi': 'ghp_xxxxx'
    }).start(['xx'])
