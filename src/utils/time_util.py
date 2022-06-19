#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 15:43
# @Author  : AIIT
# @File    : time_util.py

from datetime import datetime


def get_now_str(format: str = '%Y-%m-%d'):
    """
    获得当天时间的字符型格式
    :param format:
    :return:
    """
    return datetime.now().strftime(format)


def str_2_ts(time_str, format: str = '%Y-%m-%d'):
    """
    返回输入时间的字符型格式输出
    :param time_str:
    :param format:
    :return:
    """
    return datetime.strptime(time_str, format)
