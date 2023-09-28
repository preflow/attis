# -*- coding: utf-8 -*-
from omegaconf import OmegaConf
from prettytable import PrettyTable
from scake import SckLog

from ..preset_manager import BOOK_PAGE_SPLIT_DELIMITER
from .base_action import BaseAction

sck_log = SckLog()


class ListAction(BaseAction):
    def __init__(self, preset_manager):
        super().__init__(preset_manager=preset_manager)

    def get_pretty_table(self):
        res_table = PrettyTable()
        res_table.field_names = ["Name", "Cmd", "Path"]
        res_table.align = "l"
        res_table.border = True  # False  #no_border
        res_table.header = True  # False  #no_header
        return res_table

    def resolve_query_result(self, res, path=False):
        is_leaf = True
        if OmegaConf.is_config(res):
            is_leaf = False
            table = self.get_pretty_table()
            res = OmegaConf.to_object(res)  # dict or list
            if isinstance(res, dict):
                item_arr = []
                for k, v in res.items():
                    if isinstance(v, (dict, list, tuple)):
                        if len(v) == 0:
                            continue
                        item_arr.append(
                            (
                                "%s (%d)" % (k, len(v)),
                                "",
                                len(v),
                                BOOK_PAGE_SPLIT_DELIMITER.join([path, k])
                                if path
                                else k,
                            )
                        )  # key, value, weight, full_path
                    else:  # scalar
                        item_arr.append(
                            (
                                k,
                                v,
                                -1,
                                BOOK_PAGE_SPLIT_DELIMITER.join([path, k])
                                if path
                                else k,
                            )
                        )
                item_arr = sorted(item_arr, key=lambda tup: (tup[2], tup[0]))
                table.add_rows([[item[0], item[1], item[3]] for item in item_arr])
                res = table.get_string()
            # else: # list
            #     table.add_rows([[item, False] for item in res])
            #     res = table.get_string()
            # pass
        return res, is_leaf

    def __call__(self, args=[]):
        p_keys = []
        for arg in args:  # my_page/my_key
            if arg:
                p_keys += arg.split(BOOK_PAGE_SPLIT_DELIMITER)

        # first, try direct key query my_page1/my_page2/my_key
        clone_keys = p_keys.copy()
        while len(clone_keys) >= 0:
            if len(clone_keys) == 0:
                res, is_leaf = self.resolve_query_result(
                    self.preset_manager.get(target=False, key=False)
                )  # self.preset_manager.book
                print(res)
                return False

            direct_key = ".".join(clone_keys)
            res = self.preset_manager.get(key=direct_key, default=False)
            if res:
                cmd, is_leaf = self.resolve_query_result(
                    res, path=BOOK_PAGE_SPLIT_DELIMITER.join(clone_keys)
                )
                print(cmd)
                return cmd if is_leaf else False
            else:
                attis_key = BOOK_PAGE_SPLIT_DELIMITER.join(clone_keys)
                clone_keys = clone_keys[:-1]
                new_attis_key = BOOK_PAGE_SPLIT_DELIMITER.join(clone_keys)
                print(
                    "Attis cannot access '%s'. Try again with '%s'"
                    % (attis_key, new_attis_key)
                )

        # #TODO: ls with regex pattern, similar matching
        # res = self.preset_manager.get(target=False, key=False) # self.preset_manager.book
        # for idx, key in enumerate(p_keys):
        #     is_last_key = idx == len(p_keys)-1
        #     t_res = self.preset_manager.get(target=res, key=key)
        #     if t_res: # OK
        #         res = t_res
        #     else: # result not found, do advanced search
        #         pass
        # print(self.resolve_query_result(res))
        # pass


log_info = sck_log.register(obj_or_class=ListAction, is_info=True)
