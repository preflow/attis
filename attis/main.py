# -*- coding: utf-8 -*-
import logging
import os
import sys

from scake import Scake, SckLog

sck_log = SckLog()


logging.addLevelName(
    logging.INFO, "\x1b[1;34m%s\x1b[0m" % logging.getLevelName(logging.INFO)
)
logging.addLevelName(
    logging.WARNING, "\x1b[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING)
)
logging.addLevelName(
    logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR)
)
_logger = logging.getLogger(__name__)

ATTIS_CONFIG_PATH = os.path.join(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"), "config.yml"
)


def run():
    pass


def main_entry():
    sck = Scake(ATTIS_CONFIG_PATH)

    my_args = list(sys.argv[1:])
    if not my_args:
        my_args = [
            "",
        ]
    else:
        my_args = [
            " ".join(my_args),
        ]  # list of 1 item

    sck._conf.get_config()["main_entry"] = my_args

    # setup logger
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.ERROR,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    sck()


def main():
    sck = Scake(ATTIS_CONFIG_PATH)
    # setup logger
    if sck.get("/config/attis/mode", "prod") != "debug":
        # Remove all handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(
            stream=sys.stderr,
            level=logging.ERROR,
            format="%(asctime)s.%(msecs)03d %(levelname)s %(funcName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        pass
    sck()


if __name__ == "__main__":
    # main_entry()
    main()
