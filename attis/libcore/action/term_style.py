# -*- coding: utf-8 -*-
class TermStyle:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\33[3m"


TERM_MSG_OK = "Attis/ OK"  # f"{TermStyle.BOLD}Attis/ OK{TermStyle.ENDC}"
TERM_MSG_MISSING_KEY_OR_VALUE = (
    f"{TermStyle.ITALIC}Attis/ Missing key or value!{TermStyle.ENDC}"
)


def get_bold(msg):
    return f"{TermStyle.BOLD}{msg}{TermStyle.ENDC}"
