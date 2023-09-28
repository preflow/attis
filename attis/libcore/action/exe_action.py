# -*- coding: utf-8 -*-
import subprocess

from scake import SckLog

from .base_action import BaseAction

sck_log = SckLog()


class ExeAction(BaseAction):
    def __init__(self, preset_manager, list_action, run_line_split):
        super().__init__(
            preset_manager=preset_manager,
            list_action=list_action,
            run_line_split=run_line_split,
        )

    def __call__(self, args=[]):
        command_line = self.list_action(args)
        if command_line:
            output = subprocess.getoutput("ls -l")
            print(self.run_line_split) if self.run_line_split else None
            print(output)
        else:  # print with `attis ls` then do nothing!
            pass


log_info = sck_log.register(obj_or_class=ExeAction, is_info=True)
