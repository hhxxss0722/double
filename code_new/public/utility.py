__author__ = 'yanshaowei'
# -*- coding: utf-8 -*-

"""utility module"""

import sys
import os

def print_cur_info():
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    print(__file__.split(r'/')[-1], f.f_code.co_name, f.f_lineno)

def test_print():
    print_cur_info()


if __name__ == '__main__':
    test_print()