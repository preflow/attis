# -*- coding: utf-8 -*-
import plazy
from scake import SckLog

sck_log = SckLog()


class ActionManager:
    @plazy.auto_assign
    def __init__(self, actions={}):
        pass

    def __call__(self, args=[]):
        p_args = []
        for a in args:
            if not a:
                continue
            item = a.strip()
            p_args.append(item)

        action_name = p_args[0]
        action_args = p_args[1:]

        action_name = action_name[2:] if action_name.startswith("--") else action_name
        action_name = action_name[1:] if action_name.startswith("-") else action_name

        action_object = self.actions.get(action_name, False)
        if action_object is not False:
            action_object(action_args)  # passing arguments to action resolver

    def test_main_entry(self, multiple_commands):
        multiple_commands = (
            [
                multiple_commands,
            ]
            if not isinstance(multiple_commands, (tuple, list))
            else multiple_commands
        )
        for cmd_args in multiple_commands:
            self.__call__(args=cmd_args.split(" "))
            print("-------------")


log_info = sck_log.register(obj_or_class=ActionManager, is_info=True)
