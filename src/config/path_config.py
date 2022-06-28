#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/18 17:33
# @Author  : Tom
import os

PROJECT_DIR = os.path.abspath(os.path.join(__file__, "../../.."))
LOG_DIR = os.path.join(PROJECT_DIR, "logs")
TMP_DIR = os.path.join(PROJECT_DIR, "tmp")
NODE_REPO_PATH = os.path.join(PROJECT_DIR, "node.db")
Flow_REPO_PATH = os.path.join(PROJECT_DIR, "flow.db")
