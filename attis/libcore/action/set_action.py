# -*- coding: utf-8 -*-
from scake import SckLog

from .base_action import BaseAction

sck_log = SckLog()


# import subprocess
# output = subprocess.getoutput("ls -l")
# print(output)


class SetAction(BaseAction):
    def __init__(self, preset_manager):
        super().__init__(preset_manager=preset_manager)

    def __call__(self, args=[]):
        key = args[0]
        value = " ".join(args[1:])
        self.preset_manager.set_all_book(key=key, value=value)
        print("OK")


log_info = sck_log.register(obj_or_class=SetAction, is_info=True)
