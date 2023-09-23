# -*- coding: utf-8 -*-
import attis


def test_main_entry_call():
    try:
        attis.main_entry()
        assert True
    except Exception as e:
        print(e)
        assert False
