# -*- coding: utf-8 -*-
import os

from omegaconf import OmegaConf
from scake import SckLog

sck_log = SckLog()

BOOK_PAGE_SPLIT_DELIMITER = "/"

SOURCE_KEY_TYPE = "type"
SOURCE_KEY_ENDPOINT = "endpoint"
SOURCE_KEY_BOOK = "book"

SOURCE_TYPE_LOCAL = "local"
SOURCE_TYPE_REMOTE = "remote"


class PresetManager:
    # @plazy.auto_assign
    def __init__(self, sources, local_preset_name="local.yml"):
        self.sources = sources
        self.local_preset_name = local_preset_name
        self.book = OmegaConf.create()
        self.source_dict = self.load(self.sources)

    def _remove_key(self, book, key):
        # mydict = book.__dict__
        mydict = OmegaConf.to_container(book)
        keys = key.split(BOOK_PAGE_SPLIT_DELIMITER)
        for kidx, kname in enumerate(keys):
            if kidx == len(keys) - 1:
                mydict.pop(kname, False)
                break
            mydict = mydict[kname]
        return OmegaConf.create(mydict)

    def load(self, sources):
        """
        sources: ['/etc/attis/preset/']
        """
        result = {}
        sources = (
            [
                sources,
            ]
            if not isinstance(sources, (list, tuple))
            else sources
        )
        for src in list(sources):
            result.setdefault(src, {})
            if src.startswith("http") or src.startswith("https"):
                result[src].update(
                    {
                        SOURCE_KEY_TYPE: SOURCE_TYPE_REMOTE,
                        SOURCE_KEY_ENDPOINT: False,  # TODO
                        SOURCE_KEY_BOOK: OmegaConf.create(),  # TODO
                    }
                )
                continue
            else:  # local folder
                # if not os.access(src, os.R_OK):
                #     raise Exception()

                os.makedirs(src, exist_ok=True)

                # try:
                #     os.chmod(src, 0o777)
                # except:
                #     # not enough permission
                #     pass

                local_endpoint_file = os.path.join(
                    src, self.local_preset_name
                )  # /etc/attis/preset/local.yml
                if not os.path.isfile(local_endpoint_file):
                    with open(local_endpoint_file, "w"):
                        pass
                src_book = OmegaConf.load(local_endpoint_file)
                self.book = OmegaConf.merge(self.book, src_book)
                result[src].update(
                    {
                        SOURCE_KEY_TYPE: SOURCE_TYPE_LOCAL,
                        SOURCE_KEY_ENDPOINT: local_endpoint_file,  # TODO
                        SOURCE_KEY_BOOK: src_book,
                    }
                )
        return result

    def set_all_book(self, key, value):
        for src in self.source_dict.keys():
            self.set_book(src=src, key=key, value=value)

    def set_book(self, src, key, value):
        book_type = self.source_dict.get(src, {}).get(
            SOURCE_KEY_TYPE, False
        )  # local file path or remote url
        book_endpoint = self.source_dict.get(src, {}).get(
            SOURCE_KEY_ENDPOINT, False
        )  # local file path or remote url
        if not book_endpoint:
            print(
                "Cannot set %s book (%s) at endpoint: %s"
                % (book_type, src, book_endpoint)
            )
        if book_type not in (SOURCE_TYPE_LOCAL, SOURCE_TYPE_REMOTE):
            print("Unsupported book type (%s)" % book_type)

        if book_type == SOURCE_TYPE_LOCAL:
            dot_list = [
                '%(key)s="%(value)s"'
                % {
                    "key": key.replace(BOOK_PAGE_SPLIT_DELIMITER, "."),
                    "value": value,
                }
            ]
            new_book = OmegaConf.from_dotlist(dot_list)

            check_value = self.get(
                target=self.book,
                key=key.replace(BOOK_PAGE_SPLIT_DELIMITER, "."),
                default=False,
                throw_on_missing=False,
            )

            if not value:
                if check_value:  # delete an existing node?!
                    if OmegaConf.is_config(check_value):  # verify user answer
                        try:
                            answer = input(
                                'Do you want to permanently remove the key "%s (%d)"? (y/n): '
                                % (key, len(check_value))
                            )
                        except KeyboardInterrupt:
                            answer = "n"
                            print()
                        if answer.lower() in ("y", "yes"):
                            self.book = self._remove_key(self.book, key)
                            self.source_dict[src][SOURCE_KEY_BOOK] = self._remove_key(
                                self.source_dict[src][SOURCE_KEY_BOOK], key
                            )
                    else:  # https://stackoverflow.com/a/75864957
                        self.book = self._remove_key(self.book, key)
                        self.source_dict[src][SOURCE_KEY_BOOK] = self._remove_key(
                            self.source_dict[src][SOURCE_KEY_BOOK], key
                        )
            else:
                if check_value and OmegaConf.is_config(check_value):
                    try:
                        answer = input(
                            'Do you want to overwrite the key "%s (%d)"? (y/n): '
                            % (key, len(check_value))
                        )
                    except KeyboardInterrupt:
                        answer = "n"
                        print()
                    if answer.lower() in ("y", "yes"):
                        self.book = OmegaConf.merge(self.book, new_book)
                        self.source_dict[src][SOURCE_KEY_BOOK] = OmegaConf.merge(
                            self.source_dict[src][SOURCE_KEY_BOOK], new_book
                        )
                else:
                    self.book = OmegaConf.merge(self.book, new_book)
                    self.source_dict[src][SOURCE_KEY_BOOK] = OmegaConf.merge(
                        self.source_dict[src][SOURCE_KEY_BOOK], new_book
                    )
        else:
            print("TODO")
            raise Exception()

        self.save_source(src)

    def save_source(self, src):
        src_type = self.source_dict[src][SOURCE_KEY_TYPE]
        src_endpoint = self.source_dict[src][SOURCE_KEY_ENDPOINT]
        if src_type == SOURCE_TYPE_LOCAL:  # local file => dump to yml file
            src_book = self.source_dict[src][SOURCE_KEY_BOOK]
            with open(src_endpoint, "w") as f:
                f.write(OmegaConf.to_yaml(src_book))

    def get(self, target=False, key=False, default=False, throw_on_missing=False):
        target = self.book if not target else target
        if not key:
            return target
        else:
            return OmegaConf.select(
                target,
                key.replace(BOOK_PAGE_SPLIT_DELIMITER, "."),
                default=default,
                throw_on_missing=False,
            )


log_info = sck_log.register(obj_or_class=PresetManager, is_info=True)
