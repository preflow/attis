# -*- coding: utf-8 -*-
from omegaconf import OmegaConf
from prettytable import PrettyTable
from scake import SckLog

from ..preset_manager import BOOK_PAGE_SPLIT_DELIMITER
from .base_action import BaseAction

sck_log = SckLog()


class ListAction(BaseAction):
    def __init__(self, preset_manager, is_quite=False):
        """
        is_quite: for Python usage
        """
        super().__init__(preset_manager=preset_manager, is_quite=is_quite)

    def get_pretty_table(self):
        res_table = PrettyTable()
        res_table.field_names = ["Key", "Value / Node"]
        res_table.align = "l"
        res_table.border = True  # False  #no_border
        res_table.header = True  # False  #no_header
        return res_table

    def _parse_value_for_display(self, values):
        result = []
        if isinstance(values, (list, tuple)):
            for idx, val in enumerate(values):
                if isinstance(val, (dict, list, tuple)):
                    if isinstance(val, dict):
                        result.append("-%d {%d}" % (idx, len(val)))
                    else:
                        result.append("-%d [%d]" % (idx, len(val)))
                else:
                    result.append("-%d %s" % (idx, val))
        elif isinstance(values, dict):
            keys_with_scalar = []
            keys_with_values = []
            for k, v in values.items():
                if isinstance(v, (dict, list, tuple)):
                    keys_with_values.append("%s (%d)" % (k, len(v)))
                else:
                    keys_with_scalar.append(k)
            result.append(", ".join(keys_with_scalar)) if keys_with_scalar else None
            result.append(", ".join(keys_with_values)) if keys_with_values else None
        return result

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

                        # parsing the "dict", "list" or "tuple"
                        childs = self._parse_value_for_display(v)
                        item_arr.append(
                            (
                                "%s (%d)" % (k, len(v)),
                                "\n".join(childs),
                                len(v),
                                "%s (%d)"
                                % (BOOK_PAGE_SPLIT_DELIMITER.join([path, k]), len(v))
                                if path
                                else "%s (%d)" % (k, len(v)),
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
                # table.add_rows([[item[0], item[1], item[3]] for item in item_arr])
                table.add_rows([[item[3], item[1]] for item in item_arr])
                res = table.get_string()
            # else: # list
            #     table.add_rows([[item, False] for item in res])
            #     res = table.get_string()
            # pass
        return res, is_leaf

    def __call__(self, args=[], is_quite=None):
        p_keys = []
        for arg in args:  # my_page/my_key
            if arg:
                p_keys += arg.split(BOOK_PAGE_SPLIT_DELIMITER)

        is_quite = self.is_quite if is_quite is None else is_quite

        # first, try direct key query my_page1/my_page2/my_key
        clone_keys = p_keys.copy()
        while len(clone_keys) >= 0:
            if len(clone_keys) == 0:
                res, is_leaf = self.resolve_query_result(
                    self.preset_manager.get(target=False, key=False)
                )  # self.preset_manager.book
                if not is_quite:
                    print(res)
                return False

            direct_key = ".".join(clone_keys)
            res = self.preset_manager.get(key=direct_key, default=False)
            if res:
                cmd, is_leaf = self.resolve_query_result(
                    res, path=BOOK_PAGE_SPLIT_DELIMITER.join(clone_keys)
                )
                if not is_quite:
                    print(cmd)
                return cmd if is_leaf else False
            else:
                attis_key = BOOK_PAGE_SPLIT_DELIMITER.join(clone_keys)
                clone_keys = clone_keys[:-1]
                new_attis_key = BOOK_PAGE_SPLIT_DELIMITER.join(clone_keys)
                if not is_quite:
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
