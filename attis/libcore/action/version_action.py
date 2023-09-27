# -*- coding: utf-8 -*-
import os
import re

from scake import SckLog

from .base_action import BaseAction

sck_log = SckLog()


attis_init_file_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "__init__.py",
)


def get_property(file_python_path, prop):
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(file_python_path).read()
    )
    return result.group(1)


class VersionAction(BaseAction):
    def __init__(self):
        super().__init__()

    def __call__(self, args=[]):
        print(get_property(attis_init_file_path, "__version__"))


log_info = sck_log.register(obj_or_class=VersionAction, is_info=True)
