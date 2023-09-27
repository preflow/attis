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
            """|-------------------------------------------|
|                   ATTIS                   |
| A productivity tool for command line user |
|-------------------------------------------|
Usage:  attis OPTIONS / COMMAND
or:     a OPTIONS / COMMAND
"""
        )
        help_table = PrettyTable()
        help_table.field_names = ["OPTIONS / COMMAND", "Description"]
        help_table.align = "l"
        help_table.border = False  # no_border
        for action_name, action_help in self.action_manifest.items():
            alias_names = action_help.get("alias", [])
            action_names = (
                "  "
                + ", ".join([action_name, "--" + action_name])
                + "\n  "
                + ", ".join(["%s, -%s" % (an, an) for an in alias_names])
            )
            description = action_help.get("description", "")
            examples = "\n".join(action_help.get("example", []))
            #             print("""%(action_names)s: %(description)s
            # Examples:
            # %(examples)s """ % {
            #                 "action_names": action_names,
            #                 "description": description,
            #                 "examples": examples,
            #             })
            help_table.add_row(
                [
                    action_names,
                    "%s\n%s\n%s" % (description, "-" * len(description), examples),
                ]
            )
        print(help_table)


log_info = sck_log.register(obj_or_class=HelpAction, is_info=True)
