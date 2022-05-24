#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 17:27
# @Author  : AIIT
# @File    : log_util.py
from loguru import logger

logger.add("../logs/all.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}/{file}:{function}:{line} - {message}",
           filter="", level="DEBUG", mode="w", encoding='utf-8')

logger.add("../logs/all_{time:YYYY-MM-DD}.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}/{file}:{function}:{line} - {message}",
           filter="", level="DEBUG", encoding='utf-8')

logger.add("../logs/error.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}/{file}:{function}:{line} - {message}",
           filter="", level="ERROR", mode="w", encoding='utf-8')

logger.add("../logs/error_{time:YYYY-MM-DD}.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}/{file}:{function}:{line} - {message}",
           filter="", level="ERROR", encoding='utf-8')

log = logger
