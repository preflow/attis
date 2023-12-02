# -*- coding: utf-8 -*-
from scake import SckLog

from ..preset_manager import BOOK_PAGE_SPLIT_DELIMITER
from .base_action import BaseAction
from .term_style import TERM_MSG_MISSING_KEY_OR_VALUE, TERM_MSG_OK, TermStyle

sck_log = SckLog()


class SetAction(BaseAction):
    def __init__(self, preset_manager):
        super().__init__(preset_manager=preset_manager)

    def __call__(self, args=[]):
        """
        attis set <k1> <k2> <k3> "<command>"
        attis set <k1> <k2> <k3> = "<command>"
        attis set <k1> "command"
        attis set <k1>/<k2>/<k3> "<command>"
        """
        # key = args[0]
        # value = " ".join(args[1:])
        # self.preset_manager.set_all_book(key=key, value=value)

        is_cancelled = False
        # split args into two parts: keys and command
        if args[-1] == "=":  # interactive mode
            key = BOOK_PAGE_SPLIT_DELIMITER.join(args[:-1])
            try:
                value = input(f"{TermStyle.BOLD}%s ={TermStyle.ENDC} " % key)
            except KeyboardInterrupt:
                value = False           # fix: finally block code raises "value" referenced before assignment
                is_cancelled = True
                print()
            finally:
                if not value:
                    is_cancelled = True
                    print(TERM_MSG_MISSING_KEY_OR_VALUE)
        else:
            if "=" in args:
                equal_char_index = args.index("=")
                key = BOOK_PAGE_SPLIT_DELIMITER.join(args[:equal_char_index])
                val_index = equal_char_index + 1
                value = " ".join(args[val_index:])
                if not key or not value:
                    print(TERM_MSG_MISSING_KEY_OR_VALUE)
                    is_cancelled = True
            else:  # missing "=" delimiter
                print(TERM_MSG_MISSING_KEY_OR_VALUE)
                is_cancelled = True
            # else: # attis set <k1> <k2> "<command>"
            #     key = BOOK_PAGE_SPLIT_DELIMITER.join(args[:-1])
            #     value = args[-1]
            #     if not key or not value:
            #         print(TERM_MSG_MISSING_KEY_OR_VALUE)
            #         is_cancelled = True

        if not is_cancelled:
            self.preset_manager.set_all_book(key=key, value=value)
            print(TERM_MSG_OK)


log_info = sck_log.register(obj_or_class=SetAction, is_info=True)
