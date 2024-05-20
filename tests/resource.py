# -*- coding: utf-8 -*-
# Author:Lu
# Date:2024/5/9 12:18 
# Description:
from pathlib import Path

import onceutils

_that_dir_path = Path(__file__).parent


class _Resource(object):

    def get_data_path(self, file_name: str | Path):
        return _that_dir_path / "data" / file_name

    def read_text(self, file_name: str | Path):
        return onceutils.read_text(str(_that_dir_path / file_name))

    def read_bin(self, file_name: str | Path):
        return onceutils.read_bin(str(_that_dir_path / file_name))


Res = _Resource()
