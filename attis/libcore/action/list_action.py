# -*- coding: utf-8 -*-
from scake import SckLog

from .base_action import BaseAction

sck_log = SckLog()


class ListAction(BaseAction):
    def __init__(self, preset_manager):
        super().__init__(preset_manager=preset_manager)

    def __call__(self, args=[]):
        key = "/".join(args)
        print(self.preset_manager.get(key))


log_info = sck_log.register(obj_or_class=ListAction, is_info=True)
