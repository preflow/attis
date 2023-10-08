# -*- coding: utf-8 -*-
from scake import SckLog

from ..preset_manager import BOOK_PAGE_SPLIT_DELIMITER
from .base_action import BaseAction
from .term_style import TERM_MSG_OK

sck_log = SckLog()


class RemoveAction(BaseAction):
    def __init__(self, preset_manager):
        super().__init__(preset_manager=preset_manager)

    def __call__(self, args=[]):
        """
        attis rm <k1> <k2> <k3>
        attis rm <k1>/<k2>/<k3>
        """
        # print("Remove Action Arguments: %s" % str(args))
        key = BOOK_PAGE_SPLIT_DELIMITER.join(args)
        self.preset_manager.set_all_book(key=key, value="")
        print(TERM_MSG_OK)


log_info = sck_log.register(obj_or_class=RemoveAction, is_info=True)
