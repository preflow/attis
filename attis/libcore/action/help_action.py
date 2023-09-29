# -*- coding: utf-8 -*-
from prettytable import PrettyTable
from scake import SckLog

from .base_action import BaseAction

sck_log = SckLog()


class HelpAction(BaseAction):
    def __init__(self, action_manifest):
        super().__init__(action_manifest=action_manifest)

    def __call__(self, args=[]):
        """
        action_manifest:
            help:
                alias: ["h"]
                description: Listing available actions and examples
                example:
                - a --help
                - a -h
                - a help
                - a h
            version:
                alias: ["v"]
                description: Version of installed Attis
                example:
                - a --version
                - a -v
                - a version
                - a v
        """
        print(
            """|----------------------------------------|
|                 ATTIS                  |
| A productivity tool for linux terminal |
|----------------------------------------|

Set shortcut keys for commonly used commands in terminal.

Usage:  attis COMMAND [ARGUMENT]
or:     a COMMAND [ARGUMENT]

"""
        )
        help_table = PrettyTable()
        help_table.field_names = ["Commands", "Description & Examples"]
        help_table.align = "l"
        help_table.border = False  # no_border
        col_max_width = 75
        help_table._max_width = {
            "Commands": 30,
            "Description & Examples": col_max_width,
        }
        help_table._min_width = {"Commands": 30}
        for action_name, action_help in self.action_manifest.items():
            command = "\n".join(action_help.get("command", ""))
            description = action_help.get("description", "")
            examples = "\n".join(action_help.get("example", []))
            help_table.add_row(
                [
                    command,
                    "%s\n```bash\n%s\n```\n%s"
                    % (
                        description,
                        examples,
                        "-" * min(len(description), col_max_width),
                    ),
                ]
            )
        print(help_table)


log_info = sck_log.register(obj_or_class=HelpAction, is_info=True)
