# -*- coding: utf-8 -*-
import plazy
from scake import SckLog

sck_log = SckLog()


class ActionManager:
    @plazy.auto_assign
    def __init__(self, actions={}, preset_manager=False):
        pass

    def __call__(self, args=[]):
        p_args = []
        for a in args:
            if not a:
                continue
            item = a.strip()
            p_args.append(item)

        if p_args and len(p_args) > 0:
            action_name = p_args[0]
            action_args = p_args[1:]

            action_name = (
                action_name[2:] if action_name.startswith("--") else action_name
            )
            action_name = (
                action_name[1:] if action_name.startswith("-") else action_name
            )

            if "=" in p_args and action_name != "set":  # attris <k1> <k2> = <command>
                action_name = "set"
                action_args = p_args

            action_object = self.actions.get(action_name, False)
            if action_object is not False:
                action_object(
                    action_args.copy()
                )  # passing arguments to action resolver
            else:  # no action_name matched!
                run_action = self.actions.get("run", False)
                if run_action is not False:
                    run_action(p_args.copy())
                else:
                    log_error("Attis Internal Error: Run Action not found")
                    raise Exception()
        else:  # attis "without any params"
            if self.preset_manager is False or self.preset_manager is None:
                log_error("Attis Internal Error: Preset Manager not found")
                raise Exception()

            if (
                self.preset_manager.book and len(self.preset_manager.book) == 0
            ) or not self.preset_manager.book:
                # no data -> show help
                help_action = self.actions["help"]
                help_action()
            else:
                ls_action = self.actions["ls"]
                ls_action()

    def run_commands(self, multiple_commands):
        multiple_commands = (
            [
                multiple_commands,
            ]
            if not isinstance(multiple_commands, (tuple, list))
            else multiple_commands
        )
        for cmd_idx, cmd_args in enumerate(multiple_commands):
            self.__call__(args=cmd_args.split(" "))
            if cmd_idx != len(multiple_commands) - 1:
                print("-------------")


log_info = sck_log.register(obj_or_class=ActionManager, is_info=True)
log_error = sck_log.register(obj_or_class=ActionManager, is_error=True)
