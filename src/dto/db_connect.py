#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 16:05
# @Author  : Tom
from pydantic import BaseModel


class DbConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str
