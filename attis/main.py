# -*- coding: utf-8 -*-
import logging
import os
import sys

import plazy
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


ATTIS_MODE_DEBUG = "debug"


def main_entry(argv=None):
    sck = Scake(ATTIS_CONFIG_PATH)

    my_args = argv if argv is not None else list(sys.argv[1:])
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
    plazy.tic("init sck")
    sck = Scake(ATTIS_CONFIG_PATH)
    plazy.toc("init sck")

    mode = sck.get("/config/attis/mode", "prod")
    # setup logger
    if mode != ATTIS_MODE_DEBUG:
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

    plazy.tic("exe sck")
    sck()
    plazy.toc("exe sck")

    # performance of Scake!
    print(plazy.get_tictoc())


if __name__ == "__main__":
    main_args = sys.argv[1:]
    if len(main_args) > 1 and main_args[0] == "cli":
        main_entry(argv=sys.argv[2:])  # exclue "cli" annotation
    else:
        main()
