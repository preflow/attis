# -*- coding: utf-8 -*-
import plazy
from scake import SckLog

sck_log = SckLog()


class BaseAction:
    @plazy.auto_assign
    def __init__(self):
        pass

    def __call__(self, args=[]):
        log_error("Not implemented method!")
        raise Exception()


log_error = sck_log.register(obj_or_class=BaseAction, is_error=True)
