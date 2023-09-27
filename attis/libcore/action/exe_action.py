# -*- coding: utf-8 -*-
from scake import SckLog

from .base_action import BaseAction

sck_log = SckLog()


class ExeAction(BaseAction):
    def __init__(self, preset_manager):
        super().__init__(preset_manager=preset_manager)

    def __call__(self, args=[]):
        log_info(args)


log_info = sck_log.register(obj_or_class=ExeAction, is_info=True)
