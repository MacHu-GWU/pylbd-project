# -*- coding: utf-8 -*-

import attr
from .pkg.pathlib_mate import PathCls as Path


class Service(object):
    project_dir = attr.ib()

    @project_dir.validator
    def check_project_dir(self, attribute, value):
        project_dir = Path(value)
        if not Path(project_dir, "setup.py").exists():
            raise ValueError
