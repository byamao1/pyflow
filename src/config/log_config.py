#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 17:27
# @Author  : AIIT
# @File    : log_util.py
import os
from loguru import logger

from config.path_config import LOG_DIR

logger.add(os.path.join(LOG_DIR, "all.log"),
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}/{file}:{function}:{line} - {message}",
           filter="", level="DEBUG", mode="w", encoding='utf-8')

logger.add(os.path.join(LOG_DIR, "all_{time:YYYY-MM-DD}.log"),
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}/{file}:{function}:{line} - {message}",
           filter="", level="DEBUG", encoding='utf-8')

logger.add(os.path.join(LOG_DIR, "error.log"),
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}/{file}:{function}:{line} - {message}",
           filter="", level="ERROR", mode="w", encoding='utf-8')

logger.add(os.path.join(LOG_DIR, "error_{time:YYYY-MM-DD}.log"),
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}/{file}:{function}:{line} - {message}",
           filter="", level="ERROR", encoding='utf-8')

log = logger
