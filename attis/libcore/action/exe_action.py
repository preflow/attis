# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time

from scake import SckLog

from .base_action import BaseAction

sck_log = SckLog()


def get_terminal_col_char():
    try:
        columns, _ = os.get_terminal_size(0)  # columns, rows
    except Exception:
        columns, _ = 0, 0
    return columns


TERMINAL_WIDTH = get_terminal_col_char()


def run_command_print_progressive(command, is_stdout=True):
    # https://stackoverflow.com/a/52091495
    process = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE)
    # replace "" with b"" for Python 3
    # for line in iter(process.stdout.readline, ""):
    #    sys.stdout.write(line)

    output_lines = []
    while process.stdout.readable():
        line = process.stdout.readline()
        if not line:
            break

        # print(line.strip())
        line_str = line.decode()  # convert byte string to string
        sys.stdout.write(line_str) if is_stdout else None
        output_lines.append(line_str)
    return output_lines


def get_splitter_line(
    line_char="+", center_char="Attis Output", max_chars=TERMINAL_WIDTH
):
    center_char = " %s " % center_char
    n_center = len(center_char)  # 9
    n_line_half = (max_chars - n_center) // 2  # (4-9)//2 = -2
    n_line_remaining = max_chars - (n_line_half * 2 + n_center)  # 4-(-4+9) = -1

    n_line_remaining = 0 if n_line_half <= 0 else n_line_remaining
    n_line_half = 1 if n_line_half <= 0 else n_line_half

    return "%(line)s%(center)s%(line)s%(remaining)s" % {
        "line": line_char * n_line_half,
        "center": center_char,
        "remaining": line_char * n_line_remaining,
    }


class ExeAction(BaseAction):
    def __init__(self, preset_manager, list_action, line_char="+", center_char="Attis"):
        super().__init__(
            preset_manager=preset_manager,
            list_action=list_action,
            line_char=line_char,
            center_char=center_char,
        )

    def __call__(self, args=[]):
        command_line = self.list_action(args, is_quite=False)  # "ls -la"
        if command_line:
            print(
                get_splitter_line(
                    line_char=self.line_char,
                    center_char=self.center_char,
                    max_chars=min(len(command_line), get_terminal_col_char()),
                )
            )

            time.time()
            _ = run_command_print_progressive(
                command_line, is_stdout=True
            )  # return array ["<line1>", "<line2>", ...]
            time.time()

            # print("Delta time: %.2fs" % (t_end - t_start,))
            # output = subprocess.getoutput(command_line)
            # print(self.run_line_split) if self.run_line_split else None # ========= Attis Output =========
            # print(output)
        else:  # print with `attis ls` then do nothing!
            pass


log_info = sck_log.register(obj_or_class=ExeAction, is_info=True)
